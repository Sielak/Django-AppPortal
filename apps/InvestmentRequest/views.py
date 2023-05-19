from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from .models import CashFlowNames, Companies, CashFlowGroupNames, InvestmentHeader, InvestmentRow, ApprovalData, Attachments
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from collections import defaultdict
from datetime import date
from django.conf import settings
import os
# authenticate imports
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail


def approval_level_checker(request_amount):
    """Function used to check how many levels of approval is needed on request
    Right now exist 6 levels of approval based on request amount.

    Args:
        request_amount (int): Investment amount

    Returns:
        list: List of levels that are not needed (list of int)
    """    
    try:
        request_amount = int(request_amount)
    except ValueError:
        return []

    if request_amount <= 25000:
        return [9, 8, 7, 6, 5, 4, 3]
    elif request_amount <= 100000:
        return [9, 8, 7, 6, 5, 4]
    elif request_amount <= 200000:
        return [9, 8, 7, 6, 5]
    elif request_amount <= 500000:
        return [9, 8, 7, 6]
    elif request_amount > 500000:
        return [9, 8, 7]
    else:
        return [9, 8]

@login_required(login_url='/InvestmentRequest/login')
def main(request): 
    if request.method == 'POST':
        if request.POST.get('Submit') == 'Add':
            if request.POST.get('modal_add_header_depreciation_date') == '':
                depreciation_date = None
            else:
                depreciation_date = request.POST.get('modal_add_header_depreciation_date')
            company_info = Companies.objects.get(pk=int(request.POST.get('modal_add_header_company')))
            investment_name = request.POST.get('modal_add_header_investment_name')
            requested_amount = request.POST.get('modal_add_header_requested_amount')
            new_header = InvestmentHeader(
                name=investment_name, 
                company=company_info,
                project=request.POST.get('modal_add_header_project_number'),
                requested_amount=requested_amount,
                why=request.POST.get('modal_add_header_why'),
                what=request.POST.get('modal_add_header_what'),
                how=request.POST.get('modal_add_header_how'),
                comments=request.POST.get('modal_add_comments'),
                alternative=request.POST.get('modal_add_header_alternative'),
                env_impact=request.POST.get('modal_add_header_alternative'),
                depreciation_date=depreciation_date,
                created_by=request.user,
                updated_by=request.user
            )
            new_header.save()
            approval_levels = approval_level_checker(requested_amount)
            approval_object = ApprovalData(
                header = InvestmentHeader.objects.get(pk=new_header.id)
            )
            for item in approval_levels:
                setattr(approval_object, 'level_{0}_status'.format(item), 'not_used')
            approval_object.save()
            result = defaultdict(dict)
            for key, value in request.POST.items():
                if "modal_add_row" in key:
                    group = key.rsplit("_", 2)[1].replace("#", "_")
                    year = key.rsplit("_", 2)[2]
                    type_number = key.split("_", 5)[3]
                    type_group = key.split("_", 5)[4].replace("#", "_")
                    group_final = "{0}#{1}#{2}".format(group, type_number, type_group)
                    if value == '':
                        value = None
                    result[group_final].update({year: value}                    )
            for data, year_list in result.items():
                raw_data = data.split("#")
                new_row = InvestmentRow(
                    header  = InvestmentHeader.objects.get(pk=new_header.id),
                    type = raw_data[0],
                    type_number = int(raw_data[1]),
                    type_group = raw_data[2],
                    year_01 = year_list['year1'],
                    year_02 = year_list['year2'],
                    year_03 = year_list['year3'],
                    year_04 = year_list['year4'],
                    year_05 = year_list['year5']
                )
                new_row.save()
            send_email_to_user(company_info.approval_level_1.email, investment_name, item=new_header.id)
            return HttpResponseRedirect('main')
    companies_data = Companies.objects.all()
    group_list = CashFlowGroupNames.objects.all()
    cash_flow_name_data = []
    for item in group_list:
        res = CashFlowNames.objects.filter(cash_flow_group=item.id)
        res_data = [{"row_number": item.row_number, "name": item.name} for item in res]
        cash_flow_name_data.append({"name": item.group_name, "rows": res_data})
    
    context = {
        'cash_flow_name_data': cash_flow_name_data,
        'companies_data': companies_data,
        'investment_data': InvestmentHeader.objects.all()
    }

    return render(request, 'InvestmentRequest/index.html', context)


@login_required(login_url='/InvestmentRequest/login')
def details(request):
    item_id = request.GET.get('item')
    if request.method == 'POST':
        if request.POST.get('Submit') == 'Update CashFlow':
            # check if some approval already exists
            update_header = InvestmentHeader.objects.get(id=int(item_id))
            if update_header.approval_status() == 'Open':
                # convert form data to dict object
                result = defaultdict(dict)
                for item in request.POST.items():
                    if "rowID" in item[0]:
                        row_id = item[0].split("_")[1]
                        row_year = item[0].split("_")[2]
                        row_value = item[1]
                        if row_value == '':
                            row_value = None
                        result[row_id].update({row_year: row_value})
                # update every investment row in database
                for key, value in result.items():
                    update_object = InvestmentRow.objects.get(id=int(key))
                    update_object.year_01 = value['year1']
                    update_object.year_02 = value['year2']
                    update_object.year_03 = value['year3']
                    update_object.year_04 = value['year4']
                    update_object.year_05 = value['year5']
                    update_object.save()
                # update modified by on header
                
                update_header.updated_by = request.user
                update_header.save()
            return HttpResponseRedirect('details?item={0}'.format(item_id))
        elif request.POST.get('Submit') == 'Update':
            # check if some approval already exists
            update_object = InvestmentHeader.objects.get(id=int(item_id))
            if update_object.approval_status() == 'Open':
                # update header data
                if request.POST.get('modal_update_header_depreciation_date') == '':
                    depreciation_date = None
                else:
                    depreciation_date = request.POST.get('modal_update_header_depreciation_date')
                if request.POST.get('modal_update_header_requested_amount') == '':
                    requested_amount = None
                else:
                    requested_amount = request.POST.get('modal_update_header_requested_amount')
                
                update_object.name = request.POST.get('modal_update_header_investment_name')
                update_object.project = request.POST.get('modal_update_header_project_number')
                update_object.requested_amount = requested_amount
                update_object.why = request.POST.get('modal_update_header_why')
                update_object.what = request.POST.get('modal_update_header_what')
                update_object.how = request.POST.get('modal_update_header_how')
                update_object.alternative = request.POST.get('modal_update_header_alternative')
                update_object.env_impact = request.POST.get('modal_update_header_env_impact')
                update_object.comments = request.POST.get('modal_update_header_comments')
                update_object.depreciation_date = depreciation_date
                update_object.updated_by = request.user
                update_object.save()
                # change approval levels
                approval_data = ApprovalData.objects.get(header=int(item_id))
                approval_data.truncate_data()
                approval_data.save()
                approval_data = ApprovalData.objects.get(header=int(item_id))
                approval_levels = approval_level_checker(requested_amount)
                for item in approval_levels:
                    setattr(approval_data, 'level_{0}_status'.format(item), 'not_used')
                approval_data.save()
            return HttpResponseRedirect('details?item={0}'.format(item_id))
        elif request.POST.get('Submit') == 'Update Approval':
            update_status = request.POST.get('modal_update_status')
            level = request.POST.get('level')
            if update_status is not None:
                approval_data = ApprovalData.objects.get(header=int(item_id))
                setattr(approval_data, 'level_{0}_status'.format(level), update_status)
                setattr(approval_data, 'level_{0}_date'.format(level), date.today())
                approval_data.save()
                header_object = InvestmentHeader.objects.get(pk=int(item_id))
                if update_status == 'Rejected':
                    send_email_to_user(header_object.created_by.email, header_object.name, type="request_rejected", item=item_id)
                elif header_object.approval_status() == "Completed":
                    send_email_to_user(header_object.created_by.email, header_object.name, type="request_completed", item=item_id)
                else:
                    approver = header_object.company
                    try:
                        next_approver = getattr(approver, 'approval_level_{0}'.format(int(level) + 1)).email
                        send_email_to_user(next_approver, header_object.name, item=item_id)
                    except AttributeError:
                        pass
            return HttpResponseRedirect('details?item={0}'.format(item_id))
        elif request.POST.get('Submit') == 'Upload':
            files_list = request.FILES.getlist('attachments')
            for file in files_list:
                if settings.ENV == 'Prod':
                    location = '/media/InvestmentRequest/PROD/'
                else:
                    location = '/media/InvestmentRequest/TEST/'
                fs = FileSystemStorage(location=location)
                fs.save(file.name, file)
                update_object = Attachments(
                    header=InvestmentHeader.objects.get(pk=int(item_id)),
                    name=file.name,
                    path=location
                ).save()
            return HttpResponseRedirect('details?item={0}'.format(item_id))
        elif request.POST.get('Submit') == 'Delete Attachment':
            file_id  = request.POST.get('file_id')
            if file_id is not None:
                file_object = Attachments.objects.get(pk=int(file_id))
                if os.path.exists(file_object.path + file_object.name):
                    os.remove(file_object.path + file_object.name)
                file_object.delete()                
            return HttpResponseRedirect('details?item={0}'.format(item_id))
    else: 
        if item_id != '' and item_id is not None:
            item_data = InvestmentHeader.objects.get(pk=int(item_id))
            cash_flow_data = item_data.cash_flow()
            row_data = InvestmentRow.objects.filter(header=int(item_id))
            grouped_row_data = dict()
            for obj in row_data:
                grouped_row_data.setdefault(obj.type_group, []).append(obj)
            attachment_data = Attachments.objects.filter(header=int(item_id))
            approval_data = item_data.approval_data()
        else:
            item_data = None
            grouped_row_data = None
            approval_data = []
            attachment_data = []
            cash_flow_data = {}
        companies_data = Companies.objects.all()
        if settings.ENV == 'Prod':
            location = 'PROD'
        else:
            location = 'TEST'
        context = {
            'item_id': item_id,
            'item_data': item_data,
            'row_data': grouped_row_data,
            'companies_data': companies_data,
            'approval_data': approval_data,
            'attachment_data': attachment_data,
            'location': location,
            'cash_flow_data': cash_flow_data
        }

        return render(request, 'InvestmentRequest/details.html', context)

def update_payback(request):
    if request.method == 'POST':
        year1_positive = 0
        year2_positive = 0
        year3_positive = 0
        year4_positive = 0
        year5_positive = 0
        total_negative = 0
        for key, value in request.POST.items():
            if 'modal_add_row' in key:
                value_int = int(value) if value != '' else 0
                if value_int < 0:
                    total_negative += value_int
                else:
                    if '_year1' in key:
                        year1_positive += value_int
                    elif '_year2' in key:
                        year2_positive += value_int
                    elif '_year3' in key:
                        year3_positive += value_int
                    elif '_year4' in key:
                        year4_positive += value_int
                    elif '_year5' in key:
                        year5_positive += value_int
        try:
            total_year_1 = year1_positive - (total_negative * -1)
            if total_year_1 < 0:
                total_year_2 = year2_positive - (total_year_1 * -1)
                if total_year_2 < 0:
                    total_year_3 = year3_positive - (total_year_2 * -1)
                    if total_year_3 < 0:
                        total_year_4 = year4_positive - (total_year_3 * -1)
                        if total_year_4 < 0:
                            ratio = ((total_year_4 * -1) / year5_positive) + 4
                        else:
                            ratio = ((total_year_3 * -1) / year4_positive) + 3
                    else:
                        ratio = ((total_year_2 * -1) / year3_positive) + 2
                else:
                    ratio = ((total_year_1 * -1) / year2_positive) + 1
            else:
                ratio = ((total_negative * -1) / year1_positive)
        except ZeroDivisionError:
            ratio = 0 

        res = {'data': round(ratio, 2)}
        return JsonResponse(res)
    else:
        return JsonResponse({'info': 'Works only with POST'})


def login_InvestmentRequest(request):
    if request.method == 'POST':
        username = request.POST['inputEmail']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            checker = user.groups.filter(name='Investment Request users').exists()
            if checker is True:
                login(request, user)
                return HttpResponseRedirect('main')
            else:
                messages.add_message(request, messages.INFO, 'You dont have access to this app')
                return HttpResponseRedirect('login')
        else:
            messages.add_message(request, messages.INFO, 'Bad user or pass')
            return HttpResponseRedirect('login')
    else:

        return render(request, 'InvestmentRequest/login.html')


def logout_InvestmentRequest(request):
    logout(request)

    return HttpResponseRedirect('login')

def send_email_to_user(recipant: str, investment_name: str, type: str = 'new_request', item: str = None) -> None:
    """Function used to inform user by email about change on request

    Args:
        recipant (string): user email
        investment_name (string): name of investment
    """    
    if recipant is None or recipant == '':
        recipant = User.objects.get(username='admin').email
    root_url = "http://bma-dev-704:8300/InvestmentRequest/"
    if settings.ENV == 'Prod':
        root_url = "http://tools.hl-display.com/InvestmentRequest/"
    app_url = root_url + 'main'
    if item is not None:
        app_url = root_url + "details?item={0}".format(item)
    message = '{0} is waiting for your approval<br>Login to app to approve it > <a href="{1}">Link</a>'.format(investment_name, app_url)
    subject = 'New Investment Approval'
    if type == 'request_rejected':
        message = '{0} was rejected<br>Login to app to see details > <a href="{1}">Link</a>'.format(investment_name, app_url)
        subject = 'Your Investment Request was rejected'
    elif type == 'request_completed':
        message = '{0} was approved.<br>Login to app to see details > <a href="{1}">Link</a>'.format(investment_name, app_url)
        subject = 'Your Investment Request was approved'
    send_mail(
        subject,
        message,
        'Investment.Request@hl-display.com',
        [recipant],
        fail_silently=False,
        html_message=message
    )
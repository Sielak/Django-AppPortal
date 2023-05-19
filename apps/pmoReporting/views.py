from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from .models import Profile, PmoData, Category, SubCategory
from datetime import date
# authenticate imports
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


@login_required(login_url='/pmoReporting/login')
def pmoReporting(request):
    if request.method == 'POST':
        if request.POST.get('Submit') == 'Update':
            # print("DEBUG Update ", request.POST)
            yearly_savings = request.POST.get('yearly_savings')
            if yearly_savings != '':
                print("yearly is NOT EMPTY")
                month_saving = round(float(yearly_savings) / 12, 2)
                update_row = PmoData.objects.get(id=int(request.POST.get('row_id')))
                update_row.budget_01 = month_saving
                update_row.budget_02 = month_saving
                update_row.budget_03 = month_saving
                update_row.budget_04 = month_saving
                update_row.budget_05 = month_saving
                update_row.budget_06 = month_saving
                update_row.budget_07 = month_saving
                update_row.budget_08 = month_saving
                update_row.budget_09 = month_saving
                update_row.budget_10 = month_saving
                update_row.budget_11 = month_saving
                update_row.budget_12 = month_saving
                update_row.save()
            else:
                print("yearly is empty")
                update_row = PmoData.objects.get(id=int(request.POST.get('row_id')))
                update_row.location = request.POST.get('modal_Location')
                update_row.location_type = request.POST.get('modal_Location_type')
                update_row.initiative_type = request.POST.get('modal_initiative_type')
                update_row.category = Category.objects.get(pk=int(request.POST.get('modal_category')))
                update_row.subcategory = SubCategory.objects.get(pk=int(request.POST.get('modal_sub_category')))
                update_row.initiative_product = request.POST.get('modal_initiative_product')
                update_row.status = request.POST.get('modal_status')
                new_date = request.POST.get('modal_deadline')
                if new_date != "":
                    update_row.implementation_deadline = request.POST.get('modal_deadline')
                update_row.actual_01 = request.POST.get('actual_01')
                update_row.actual_02 = request.POST.get('actual_02')
                update_row.actual_03 = request.POST.get('actual_03')
                update_row.actual_04 = request.POST.get('actual_04')
                update_row.actual_05 = request.POST.get('actual_05')
                update_row.actual_06 = request.POST.get('actual_06')
                update_row.actual_07 = request.POST.get('actual_07')
                update_row.actual_08 = request.POST.get('actual_08')
                update_row.actual_09 = request.POST.get('actual_09')
                update_row.actual_10 = request.POST.get('actual_10')
                update_row.actual_11 = request.POST.get('actual_11')
                update_row.actual_12 = request.POST.get('actual_12')
                update_row.budget_01 = request.POST.get('budget_01')
                update_row.budget_02 = request.POST.get('budget_02')
                update_row.budget_03 = request.POST.get('budget_03')
                update_row.budget_04 = request.POST.get('budget_04')
                update_row.budget_05 = request.POST.get('budget_05')
                update_row.budget_06 = request.POST.get('budget_06')
                update_row.budget_07 = request.POST.get('budget_07')
                update_row.budget_08 = request.POST.get('budget_08')
                update_row.budget_09 = request.POST.get('budget_09')
                update_row.budget_10 = request.POST.get('budget_10')
                update_row.budget_11 = request.POST.get('budget_11')
                update_row.budget_12 = request.POST.get('budget_12')
                update_row.save()
            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Copy':
            copy_row = PmoData.objects.get(id=int(request.POST.get('row_id')))
            copy_row.pk = None
            copy_row.save()
            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Add':
            if request.POST.get('deadline') == '':
                deadline = None
            else:
                deadline = request.POST.get('deadline')
            new_row = PmoData(
                location=request.POST.get('Location'), 
                location_type=request.POST.get('Location_type'), 
                initiative_type=request.POST.get('initiative_type'), 
                category=Category.objects.get(pk=int(request.POST.get('category'))),
                subcategory=SubCategory.objects.get(pk=int(request.POST.get('sub_category'))),
                initiative_product=request.POST.get('initiative_product'), 
                status=request.POST.get('status'), 
                implementation_deadline=deadline,
                initiative_year=request.POST.get('initiative_year')
            )
            new_row.save()
            return HttpResponseRedirect('main')

    else:
        print('reload 1')
        this_year = date.today().year
        choosed_year = request.GET.get('year', this_year)
        user_profile = Profile.objects.get(user=request.user)
        user_group_list = []
        for choice in user_profile.user_group.all():
            user_group_list.append(choice)
        context = {
            'pmo_data': PmoData.objects.filter(initiative_year=choosed_year).filter(location__in=user_group_list),
            'user_group_list': user_group_list,
            'category_list': Category.objects.all(),
            'subcategory_list': SubCategory.objects.all(),
            'choosed_year': choosed_year
        }

        return render(request, 'pmoReporting/index.html', context)


def login_pmoReporting(request):
    if request.method == 'POST':
        username = request.POST['inputEmail']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_profile = Profile.objects.filter(user=user) 
            if user_profile.exists() is False:
                messages.add_message(request, messages.INFO, 'No Profile for this user')
                return redirect('login_pmoReporting')
            else:
                login(request, user)
                return redirect('main_pmoReporting')
        else:
            messages.add_message(request, messages.INFO, 'Bad user or pass')
            return redirect('login_pmoReporting')
    else:

        return render(request, 'pmoReporting/login.html')


def logout_pmoReporting(request):
    logout(request)

    return redirect('login_pmoReporting')

from django.core.files.storage import FileSystemStorage
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import FileResponse
from django.core.exceptions import ObjectDoesNotExist
import pyodbc
from datetime import datetime, date, timedelta
from .models import CrossDockingLogs, CrossDockingParams
from .helpers import create_cmr_file
# authenticate imports
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required

def refresh_data():
    config_database_name = CrossDockingParams.objects.filter(Param_Name='database_name')

    if len(config_database_name) == 0:
        database_name = "ErpTst001"
        database_server = "EW1-SQL-711"
    elif config_database_name[0].Param_Value_string is None:
        database_name = "ErpTst001"
        database_server = "EW1-SQL-711"
    else:
        database_name = config_database_name[0].Param_Value_string
        if database_name == "ErpJvs001":
            database_server = "EW1-SQL-113"
        elif database_name == "ErpTst001":
            database_server = "EW1-SQL-711"
        else:
            database_server = "EW1-SQL-716"

    uid = 'AppPortal'
    if database_name == "ErpJvs001":
        pwd = 'rpWBjoM*V$5QAKi9'
    else:
        pwd = 'H&k5jc44^pC!f4^&'
    cnxn = pyodbc.connect(driver='{ODBC Driver 17 for SQL Server}', server=database_server, database=database_name, uid=uid, pwd=pwd)
    sql_cmd = """
    SELECT bestnr
        ,beststatbeskr
        ,FtgNamn
        ,bestberlevdat
    FROM CrossDocking
    """
    cursor = cnxn.cursor()
    cursor.execute(sql_cmd)
    po_info = cursor.fetchall()
    for row in po_info:
        po_checker = CrossDockingLogs.objects.filter(po_number=row.bestnr)
        if po_checker:
            if 'Delivered' in row.beststatbeskr:
                po_checker.update(po_status=row.beststatbeskr, confirmation_date=row.bestberlevdat, row_status='Delivered to SDL RDC')
            else:
                po_checker.update(po_status=row.beststatbeskr, confirmation_date=row.bestberlevdat)
        else:
            CrossDockingLogs.objects.create(po_number=row.bestnr, \
                                        po_status=row.beststatbeskr, \
                                        po_supplier=row.FtgNamn, \
                                        confirmation_date=row.bestberlevdat, \
                                        delivery_number="", \
                                        row_status="Waiting for delivery")


@login_required(login_url='/CrossDocking/login')
def cross_docking(request):
    if request.method == 'POST':
        if request.POST.get('Submit') == 'Refresh':
            refresh_data()
            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Create':
            try:
                last_cmr_number = CrossDockingParams.objects.get(Param_Name='Last CRM Number')
            except ObjectDoesNotExist:
                new_param = CrossDockingParams(Param_Name='Last CRM Number', Param_Value_int=0)
                new_param.save()
                last_cmr_number = CrossDockingParams.objects.get(Param_Name='Last CRM Number')
            delivery_number = f"{datetime.today().strftime('%Y%m')}{int(last_cmr_number.Param_Value_int)}"
            last_cmr_number.Param_Value_int += 1
            last_cmr_number.save()
            carrier_name = request.POST.get('modal2_name')
            carrier_address = request.POST.get('modal2_address')
            carrier_country = request.POST.get('modal2_country')
            vehicle_number = request.POST.get('modal2_vehicle_number')
            trailer_number = request.POST.get('modal2_trailer_number')
            load_date = request.POST.get('modal2_load_date')
            modal2_po_list = request.POST.getlist('modal2_po_list')
            cmr_data = []
            for item in modal2_po_list:
                po_from_db = CrossDockingLogs.objects.get(po_number=item)
                an_item = dict(po_number=po_from_db.po_number,
                           po_supplier=po_from_db.po_supplier,
                           pallet_count=po_from_db.pallet_count,
                           packages_count=po_from_db.packages,
                           weight=po_from_db.weight,
                           pallet_location=po_from_db.pallet_location
                )
                cmr_data.append(an_item)
                po_from_db.delivery_number = delivery_number
                po_from_db.shipment_date = load_date
                po_from_db.row_status = "Sent to SDL RDC"
                po_from_db.save()
            cmr_file = create_cmr_file(cmr_data, carrier_name, carrier_address, carrier_country, vehicle_number, trailer_number, load_date, delivery_number)
            return FileResponse(cmr_file, as_attachment=True, filename=f'cmr_{delivery_number}.pdf')
        elif request.POST.get('Submit') == 'Update':
            if request.POST.get('modal_pallet_count') == '':
                pallet_count = None
            else:
                pallet_count = request.POST.get('modal_pallet_count')
            if request.POST.get('modal_packages_count') == '':
                packages = None
            else:
                packages = request.POST.get('modal_packages_count')
            if request.POST.get('delivery_date') == '':
                delivery_date = None
            else:
                delivery_date = request.POST.get('delivery_date')
            if request.POST.get('shipment_date') == '':
                shipment_date = None
            else:
                shipment_date = request.POST.get('shipment_date')
            if request.POST.get('modal_weight') == '':
                weight = None
            else:
                weight = request.POST.get('modal_weight')
            update_object = CrossDockingLogs.objects.get(id=int(request.POST.get('row_id')))
            update_object.delivery_number = request.POST.get('modal_delivery_number')
            update_object.pallet_count = pallet_count
            update_object.row_status = request.POST.get('modal_Status')
            update_object.delivery_date = delivery_date
            update_object.shipment_date = shipment_date
            update_object.packages = packages
            update_object.weight = weight
            update_object.pallet_location = request.POST.get('modal_pallet_location')
            update_object.save()
            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Upload':
            try:
                delivery_number = request.POST.get('modal3_delivery_list')
                myfile = request.FILES['myfile']
                try:
                    environment = CrossDockingParams.objects.get(Param_Name='database_name').Param_Value_string
                except ObjectDoesNotExist:
                    environment = "ErpTst001"
                if environment == 'ErpJvs001':
                    location='/media/CrossDocking/PROD/'
                else:
                    location='/media/CrossDocking/TEST/'
                fs = FileSystemStorage(location=location)
                file_name = f'CMR_{delivery_number}.pdf'
                fs.save(file_name, myfile)
                update_object = CrossDockingLogs.objects.filter(delivery_number=delivery_number)
                update_object.update(file_uploaded=True)
            except KeyError:
                myfile = ''
                delivery_number = ''

            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Split':
            backorder_number = request.POST.get('backorder_number')
            if backorder_number != '':
                original_object = CrossDockingLogs.objects.get(id=int(request.POST.get('row_id')))
                new_po_number = original_object.po_number + "-" + backorder_number
                CrossDockingLogs.objects.create(po_number=new_po_number, \
                                                po_status="Added manually", \
                                                po_supplier=original_object.po_supplier, \
                                                delivery_number="", \
                                                row_status=original_object.row_status)
            return HttpResponseRedirect('main')
        else:
            print("[DEBUG]!")
            return HttpResponseRedirect('main')
    else:
        po_numbers_list = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').values_list('po_number', flat=True)
        po_list = CrossDockingLogs.objects.all()  # TODO add filter
        price_multiplication = CrossDockingParams.objects.filter(Param_Name='Price Multiplication')
        delivery_list = CrossDockingLogs.objects.filter(file_uploaded=False).filter(delivery_number__isnull=False).exclude(delivery_number__exact='').values_list('delivery_number', flat=True).distinct()
        sum_pallet_count = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('pallet_count'))
        sum_packages = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('packages'))
        sum_weight = CrossDockingLogs.objects.filter(row_status='Delivered to GLI RDC').aggregate(Sum('weight'))
        today = date.today()
        first = today.replace(day=1)
        lastMonth = first - timedelta(days=1)
        last_month_rows = CrossDockingLogs.objects.filter(shipment_date__startswith=lastMonth.strftime("%Y-%m"))
        last_month_price = 0
        for item in last_month_rows:
            last_month_price = last_month_price + item.calculate_price()
        try:
            if last_month_price > 0:
                last_month_price += CrossDockingParams.objects.get(Param_Name='Fixed fee').Param_Value_int
        except TypeError:
            pass
        try:
            environment = CrossDockingParams.objects.get(Param_Name='database_name').Param_Value_string
        except ObjectDoesNotExist:
            environment = "ErpTst001"
        if environment == 'ErpJvs001':
            location='PROD'
        else:
            location='TEST'
        context = {
            'po_list': po_list,
            'delivery_list': delivery_list,
            'po_numbers_list': po_numbers_list,
            'price_multiplication': price_multiplication,
            'sum_pallet_count': sum_pallet_count['pallet_count__sum'],
            'sum_packages': sum_packages['packages__sum'],
            'sum_weight': sum_weight['weight__sum'],
            'date_now': datetime.now(),
            'last_month_price': round(last_month_price, 2),
            'location': location
        }

        return render(request, 'CrossDocking/cross_docking.html', context)

def login_crossDocking(request):
    if request.method == 'POST':
        username = request.POST['inputEmail']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            checker = user.groups.filter(name='Cross docking users').exists()
            if checker is True:
                login(request, user)
                return redirect('main_crossDocking')
            else:
                messages.add_message(request, messages.INFO, 'You dont have access to this app')
                return redirect('login_crossDocking')
        else:
            messages.add_message(request, messages.INFO, 'Bad user or pass')
            return redirect('login_crossDocking')
    else:

        return render(request, 'CrossDocking/login.html')


def logout_crossDocking(request):
    logout(request)

    return redirect('login_crossDocking')

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .helpers.qr_bill import CreateQrBill
from .helpers.track_and_trace import TrackAndTrace
from apps.HighlightTracker.models import highlight_data, Profile
from apps.pmoReporting.models import PmoData
from .models import ApiLogs
import re
from apps.CrossDocking.views import refresh_data
from apps.CrossDocking.helpers import send_summary_email
from apps.cab.helpers import FreshServiceAPI


@csrf_exempt
def get_pmoReporting_data(request):
    if request.method == 'POST':
        return JsonResponse({'Data': [{'info': 'Works only with GET', 'Endpoint': 'get_pmoReporting_data'}]}, status=200)
    else:
        rows = PmoData.objects.all()
        data = {
            'Data': [
            ]
        }
        for row in rows:
            an_item = {
                'row_id': row.id,
                'location': row.location,
                'location_type': row.location_type,
                'initiative_type': row.initiative_type,
                'category': row.category.Name,
                'subcategory': row.subcategory.Name,
                'initiative_product': row.initiative_product,
                'status': row.status,
                'implementation_deadline': row.implementation_deadline,
                'total_savings_actual': row.total_savings_actual(),
                'total_savings_budget': row.total_savings_budget()                
            }
            data['Data'].append(an_item)
            
        return JsonResponse(data, status=200)


@csrf_exempt
def get_highlight_data(request):
    if request.method == 'POST':
        return JsonResponse({'Data': [{'info': 'Works only with GET', 'Endpoint': 'get_highlight_data'}]}, status=200)
    else:
        rows = highlight_data.objects.all()
        data = {
            'Data': [
            ]
        }
        for row in rows:
            an_item = {
                'row_id': row.id,
                'Subject_Group': row.Subject_Group,
                'Improvement_Identified': row.Improvement_Identified,
                'Action_description': row.Action_description,
                'Responsible_person': row.Responsible_person,
                'Completion_Date': row.Completion_Date,
                'Action_status': row.Action_status,
                'Comments': row.Comments,
                'row_Group': row.row_Group.Name,
                'row_Area': row.row_Area.Name,
                'row_country': row.row_country.Name,
                'row_Year': row.row_Year
            }
            data['Data'].append(an_item)
            
        return JsonResponse(data, status=200)


@csrf_exempt
def get_user_data(request):
    if request.method == 'POST':
        return JsonResponse({'Data': [{'info': 'Works only with GET', 'Endpoint': 'get_user_data'}]}, status=200)
    else:
        profiles = Profile.objects.all()
        data = {
            'Data': [
            ]
        }
        for profile in profiles:
            user_group_list = []
            user_area_list = []
            user_country_list = []
            for choice in profile.user_group.all():
                user_group_list.append(str(choice))
            for choice in profile.user_area.all():
                user_area_list.append(str(choice))
            for choice in profile.user_country.all():
                user_country_list.append(str(choice))
            an_item = {
                'email': profile.user.email,
                'groups': user_group_list,
                'areas': user_area_list,
                'countrys': user_country_list
            }
            data['Data'].append(an_item)
            
        return JsonResponse(data, status=200)

@csrf_exempt
def qr_bill(request):
    if request.method == 'POST':
        in_type = request.GET.get('input_type', 'xml')
        config = CreateQrBill(request.body, in_type)
        results = config.create_qr_file()
        return results
    else:
        return JsonResponse({'Data': [{'info': 'Works only with POST', 'Endpoint': 'qr_bill'}]}, status=200)

@csrf_exempt
def api_logs(request):
    if request.method == 'POST':
        return JsonResponse({'Data': [{'info': 'Works only with GET', 'Endpoint': 'data2jeeves_stats'}]}, status=200)
    else:
        all_logs = list(ApiLogs.objects.values())
        return JsonResponse({'Data': all_logs}, status=200)

@csrf_exempt
def crossDockingRefresh(request):
    if request.method == 'POST':
        refresh_data()
        return JsonResponse({'Data': [{'info': 'Cross Docking data refreshed', 'Endpoint': 'crossDockingRefresh'}]}, status=200)
    else:
        return JsonResponse({'Data': [{'info': 'Works only with POST', 'Endpoint': 'crossDockingRefresh'}]}, status=200)

@csrf_exempt
def crossDockingSummaryEmail(request):
    if request.method == 'POST':
        results = send_summary_email()
        return JsonResponse({'Data': [{'info': results, 'Endpoint': 'crossDockingSummaryEmail'}]}, status=200)
    else:
        return JsonResponse({'Data': [{'info': 'Works only with POST', 'Endpoint': 'crossDockingSummaryEmail'}]}, status=200)

@csrf_exempt
def cab_refresh(request):
    if request.method == 'POST':
        results = FreshServiceAPI().fetch_changes()
        return JsonResponse({'Data': {'info': results, 'Endpoint': 'cab_refresh'}}, status=200)
    else:
        return JsonResponse({'Data': {'info': 'Works only with POST', 'Endpoint': 'cab_refresh'}}, status=200)

@csrf_exempt
def track_and_trace(request):
    if request.method == 'POST':
        results = TrackAndTrace(request.body).download_files()
        return results
    else:
        return JsonResponse({'Data': [{'info': 'Works only with POST', 'Endpoint': 'track_and_trace'}]}, status=200)
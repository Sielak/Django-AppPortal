from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import highlight_data, SubjectGroup, Profile, Area, Group, Country, highlight_tracker_settings
from datetime import date
# authenticate imports
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required


@login_required(login_url='/HighlightTracker/login')
def highlight_tracker(request):
    if request.method == 'POST':
        if request.POST.get('Submit') == 'Update':
            update_object = highlight_data.objects.get(id=int(request.POST.get('row_id')))
            update_object.Subject_Group = request.POST.get('modal_Subject_Group')
            update_object.Improvement_Identified = request.POST.get('modal_Improvement_identified')
            update_object.Action_description = request.POST.get('modal_Action_description')
            update_object.Responsible_person = request.POST.get('modal_Responsible_person')
            new_date = request.POST.get('modal_Completion_Date')
            if new_date != "":
                update_object.Completion_Date = request.POST.get('modal_Completion_Date')
            update_object.Action_status = request.POST.get('modal_Status')
            update_object.Comments = request.POST.get('modal_Comments')
            update_object.save()
            return HttpResponseRedirect('main')
        elif request.POST.get('Submit') == 'Add':
            if request.POST.get('Completion_Date') == '':
                completion_date = None
            else:
                completion_date = request.POST.get('Completion_Date')
            new_row = highlight_data(Subject_Group=request.POST.get('Subject_Group'), 
                    Improvement_Identified=request.POST.get('Improvement_identified'),
                    Action_description=request.POST.get('Action_description'),
                    Responsible_person=request.POST.get('Responsible_person'),
                    Completion_Date=completion_date,
                    Action_status=request.POST.get('Status'),
                    Comments=request.POST.get('Comments'),
                    row_Group=Group.objects.get(pk=int(request.POST.get('Group'))),
                    row_Area=Area.objects.get(pk=int(request.POST.get('Area'))),
                    row_country=Country.objects.get(pk=int(request.POST.get('Country'))),
                    row_Year=request.POST.get('row_year')
                    )
            new_row.save()
            return HttpResponseRedirect('main')
        else:
            print("[DEBUG].")
            return HttpResponseRedirect('main') 
    else:
        try:
            last_year = highlight_tracker_settings.objects.get(Name = "last_year").Value
            this_year = highlight_tracker_settings.objects.get(Name = "this_year").Value
        except ObjectDoesNotExist:
            this_year = date.today().year
            last_year = int(this_year) - 1
        choosed_year = request.GET.get('year', this_year)
        subject_group = SubjectGroup.objects.all()
        user_profile = Profile.objects.get(user=request.user)
        user_group_list = []
        user_area_list = []
        user_country_list = []
        for choice in user_profile.user_group.all():
            user_group_list.append(choice)
        for choice in user_profile.user_area.all():
            user_area_list.append(choice)
        for choice in user_profile.user_country.all():
            user_country_list.append(choice)
        action_list_data = highlight_data.objects \
                                        .filter(row_Year=choosed_year) \
                                        .filter(row_Group__in=user_group_list) \
                                        .filter(row_Area__in=user_area_list) \
                                        .filter(row_country__in=user_country_list)
        context = {
            'var1': 'variable1',
            'subject_group': subject_group,
            'action_list_data': action_list_data,
            'user_group_list': user_group_list,
            'user_area_list': user_area_list,
            'user_country_list': user_country_list,
            'last_year': last_year,
            'this_year': this_year,
            'choosed_year': choosed_year
        }

        return render(request, 'tools/highlight_tracker.html', context)

def login_HighlightTracker(request):
    if request.method == 'POST':
        username = request.POST['inputEmail']
        password = request.POST['inputPassword']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user_profile = Profile.objects.filter(user=user) 
            if user_profile.exists() is False:
                messages.add_message(request, messages.INFO, 'No Profile for this user')
                return redirect('login_HighlightTracker')
            else:
                login(request, user)
                return redirect('main_HighlightTracker')
        else:
            messages.add_message(request, messages.INFO, 'Bad user or pass')
            return redirect('login_HighlightTracker')
    else:

        return render(request, 'tools/login.html')


def logout_HighlightTracker(request):
    logout(request)

    return redirect('login_HighlightTracker')

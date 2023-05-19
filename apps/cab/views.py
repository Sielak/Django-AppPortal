from django.shortcuts import render
from .models import CabData


def cab_list(request): 
    context = {
        'cab_data': CabData.objects.all()
    }

    return render(request, 'cab/index.html', context)

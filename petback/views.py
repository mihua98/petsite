

from petback.models import *
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

def petbacklist(request):
    lostpet_list = LostPet.objects.all().order_by('-created_time')
    return render(request,'petback/petbacklist.html',context={"lost_pet_list":lostpet_list})

def petbackDetail(request,pk):
    lostpet = get_object_or_404(LostPet,pk=pk)
    return render(request,'petback/petback-details.html',context={"lost_pet":lostpet})
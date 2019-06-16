from django.shortcuts import render
from django.http import JsonResponse
from .models import Zone

def some_report(request):
    from django.core import serializers
    data = serializers.serialize("json", Zone.objects.all())
    return JsonResponse(data, safe=False)

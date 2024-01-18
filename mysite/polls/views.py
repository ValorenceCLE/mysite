from django.shortcuts import render, redirect
from django.http import HttpResponse, request
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import random
import inspect
from .scripts.relay import turn_fan_on, turn_fan_off, run_fan_for_5_minutes


def home(request):
    return render(request, 'home.html')


def pwr(request):
    return render(request, 'pwr.html')


def storage(request):
    return render(request, 'storage.html')


def connectivity(request):
    return render(request, 'connectivity.html')


def support(request):
    return render(request, 'support.html')


def thanks(request):
    return render(request, 'thanks.html')


def fan_on(request):
    turn_fan_on()
    return JsonResponse({"message": "Fan turned on"})


def fan_off(request):
    turn_fan_off()
    return JsonResponse({"message": "Fan turned off"})


def fan_run_for_5_minutes(request):
    run_fan_for_5_minutes()
    return JsonResponse({"message": "Fan ran for 5 minutes"})
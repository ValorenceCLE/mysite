from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django import forms
from django.http import JsonResponse
import random


def index(request):
    if request.method == 'POST':
        name = request.POST.get('full-name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {
            'name': name,
            'email': email,
            'subject': subject,
            'message': message

        }
        message = '''
        New message: {}
        
        From: {}
        '''.format(data['message'], data['email'])
        send_mail(data['subject'], message, 'supportticket@valorence.com', ['supportticket@valorence.com'])
    return render(request, 'support.html', {})




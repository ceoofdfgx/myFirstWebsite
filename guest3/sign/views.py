# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from sign.models import Event, Guest


def index(request):
    return render(request, "index.html")


def login_action(request):
    if request.method == 'POST':
        username = request.POST.get('username', 'admin')
        password = request.POST.get('password', 'admin')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            request.session['user'] = username
            response = HttpResponseRedirect('/event_manage/')
            return response
        else:
            return render(request, 'index.html', {'error': 'username or password error!'})


@login_required
def event_manage(request):
    event_list = Event.objects.all()
    username = request.session.get('user', '')
    # username = request.COOKIES.get('user', '')
    # username = request.session.get('user', '')
    return render(request, "event_manage.html", {'user': username, 'events': event_list})


@login_required
def search_name(request):
    username = request.session.get('user', '')
    search_name = request.GET.get('name', '')
    event_list = Event.objects.filter(name__contains=search_name)
    return render(request, 'event_manage.html', {'user': username, 'events': event_list})


@login_required
def guest_manage(request):
    username = request.session.get('user', '')
    guest_list = Guest.objects.all()
    paginator = Paginator(guest_list, 2)
    page = request.GET.get('page')
    try:
        contacts = paginator.page(page)
    except PageNotAnInteger:
        contacts = paginator.page(1)
    except EmptyPage:
        contacts = paginator.page(paginator.num_pages)
    return render(request, 'guest_manage.html', {'user': username, 'guests': guest_list})


@login_required
def sign_index(request, eid):
    event = get_object_or_404(Event, id=eid)
    return render(request, 'sign_index.html', {'event': event})


@login_required
def sign_index_action(request, eid):
    event = get_object_or_404(Event, id=eid)
    phone = request.POST.get('phone', '')
    print (phone)
    result = Guest.objects.filter(phone=phone)
    if not result:
        return render(request, 'sign_index.html', {'event': event, 'hint': 'phone erorr.'})
    result = Guest.objects.get(phone=phone, event_id=eid)
    if result.sign:
        return render(request, 'sign_index.html', {'event': event, 'hint': "user has sign in."})
    else:
        Guest.objects.filter(phone=phone, event_id=eid).update(sign='1')
        return render(request, 'sign_index.html', {'event': event, 'hint': 'sign in success!', 'guest': result})


@login_required
def logout(request):
    auth.logout(request)
    response = HttpResponseRedirect('/index/')
    return response

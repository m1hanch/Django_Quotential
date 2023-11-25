from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, template_name='quotes/base.html', context={})

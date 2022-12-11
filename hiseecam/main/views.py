from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import *


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found</h1>')


def home(request):
    if request.method == 'POST':
        name = request.POST['name']
        surname = request.POST['surname']
        print(name, surname)
    return render(request, 'main/index.html')


def search(request):
    q = request.GET.get('q')
    if q is not None and q != '':
        results = Cameras.objects.filter(title__iregex=q)
    elif q == '':
        results = ''
    context = {
        'results': results,
    }
    return render(request, 'main/search-results.html', context)

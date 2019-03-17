from django.shortcuts import render


def frontpage(request):
    return render(request, 'frontpage/index.html')

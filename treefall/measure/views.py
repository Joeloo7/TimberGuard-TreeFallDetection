from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def init(request):
    
    if len(request.GET)==1:
        a,=request.GET.items()
        return render(request,'main_new.html')
    else:
        return render(request,'main_new.html')

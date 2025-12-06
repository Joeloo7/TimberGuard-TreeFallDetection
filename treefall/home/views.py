from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import tensorflow as tf
from keras import models
from .models import usruploads
from PIL import Image
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry
import pickle

fp=open("home/svm_risk.pkl","rb")

risk_model=pickle.load(fp)

dis_model=models.load_model('home/disease_GPU_V5.keras')
@csrf_exempt
def main_view(request):
    n=usruploads.objects.all()
    for i in n:
            i.flnm.delete()
            i.delete()
    
    if len(request.POST)==1:
        d,=request.POST.items()
        print(d)
        if d[0]=="name":
            if d[1]=="disease":
                 return render(request,"disease.html")
            elif d[1]=="aboutus":
                 return render(request,"about.html")
                 
        a=usruploads()
        f=dict(request.FILES.items())
        a.flnm=f['infile']
        a.save()
        
        img=Image.open('media/'+a.flnm.name)
        img=img.convert('RGB')
        img=img.resize((224,224))
        imgarr=np.array(img)
        imgarr=imgarr/255
        imgarr=imgarr.reshape(1,224,224,3)
        
        output=dis_model.predict(imgarr)
        score=tf.nn.softmax(output[0])
        if score[0]>score[1]:
            flag="Healthy Tree Trunk"
        else:
            flag="Stem Bleed disease detected"
        
        return render(request,"disease.html",{"flag":flag,"url":"/media/"+a.flnm.name})
    elif len(request.POST)==2:
         a,b=request.POST.items()
         if a[0]=="result":
            print("disease site")
            print("disease:",a[1])
            return render(request,"main_new.html",{"flag":a[1]})
         
         return render(request,"disease.html")
    
    elif len(request.POST)==3:
         a,b,c=request.POST.items()
         print("estimator")
         print("moment:",b[1])
         print("disease:",a[1])
         if a[0]=="disease":
              return render(request,"weather.html",{"rain":0.0,"wind":0.0,"moment":b[1],"disease":a[1]})
         """if a[0]=="latitude":
            lat=float(a[1])
            long=float(b[1])
            cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
            retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
            openmeteo = openmeteo_requests.Client(session = retry_session)

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": 11.2622,
                "longitude": 75.865,
                "current": ["rain", "wind_speed_10m", "wind_direction_10m"],
                "timezone": "auto",
                "forecast_days": 1
            }
            responses = openmeteo.weather_api(url, params=params)

            # Process first location. Add a for-loop for multiple locations or weather models
            response = responses[0]
            print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevation {response.Elevation()} m asl")
            print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


            # Current values. The order of variables needs to be the same as requested.
            current = response.Current()

            current_rain = current.Variables(0).Value()

            current_wind_speed_10m = current.Variables(1).Value()

            current_wind_direction_10m = current.Variables(2).Value()

            print(f"Current time {current.Time()}")

            print(f"Current rain {current_rain}")
            print(f"Current wind_speed_10m {current_wind_speed_10m}")
            print(f"Current wind_direction_10m {current_wind_direction_10m}")
            return render(request,"weather.html",{"rain":current_rain,"wind":current_wind_speed_10m,"moment":b[1],"disease":a[1],"output":""})  """

    elif(len(request.POST)==5):
        a,b,c,d,e=request.POST.items()
        if a[0]=="latitude":
            lat=float(a[1])
            long=float(b[1])
            cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
            retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
            openmeteo = openmeteo_requests.Client(session = retry_session)

            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": 11.2622,
                "longitude": 75.865,
                "current": ["rain", "wind_speed_10m", "wind_direction_10m"],
                "timezone": "auto",
                "forecast_days": 1
            }
            responses = openmeteo.weather_api(url, params=params)

            # Process first location. Add a for-loop for multiple locations or weather models
            response = responses[0]
            print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
            print(f"Elevation {response.Elevation()} m asl")
            print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
            print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")


            # Current values. The order of variables needs to be the same as requested.
            current = response.Current()

            current_rain = current.Variables(0).Value()

            current_wind_speed_10m = current.Variables(1).Value()

            current_wind_direction_10m = current.Variables(2).Value()

            print(f"Current time {current.Time()}")

            print(f"Current rain {current_rain}")
            print(f"Current wind_speed_10m {current_wind_speed_10m}")
            print(f"Current wind_direction_10m {current_wind_direction_10m}")
            return render(request,"weather.html",{"rain":current_rain,"wind":current_wind_speed_10m,"moment":b[1],"disease":a[1],"output":""})
        
        elif a[0]=="disease":
            a,b,c,d,e=request.POST.items()
            #a dis, b moment, c windspeed, d rain
            print(a[1],b[1],c[1],d[1])
            if a[1]=="Healthy Tree Trunk": 
                if float(b[1])>=40000:
                    if float(d[1])>=5:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"high risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                    else:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"low risk"})
                else:
                    if float(d[1])>=5:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"low risk"})
                    else:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"low risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"low risk"})
            else:
                if float(b[1])>=40000:
                    if float(d[1])>=5:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"high risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"high risk"})
                    else:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"high risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                else:
                    if float(d[1])>=5:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                    else:
                        if float(c[1])>=38:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"medium risk"})
                        else:
                            return render(request,"weather.html",{"rain":0,"wind":0,"output":"low risk"})


    else:
        n=usruploads.objects.all()
        for i in n:
            i.flnm.delete()
            i.delete()
        return render(request,'homepage2.html')
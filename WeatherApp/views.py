from django.shortcuts import render,redirect
from .forms import CityForm
from .models import City
from django.contrib import messages
import requests
# Create your views here.
def home(request):
    url='https://api.openweathermap.org/data/2.5/weather?q={},&appid=bca7091cab8ab9799f363494b39c600f&units=metric'

    if request.method=="POST":
        form=CityForm(request.POST)
        if form.is_valid():
            Ncity=form.cleaned_data['name']
            CCity=City.objects.filter(name=Ncity).count()
            if CCity==0:
                res=requests.get(url.format(Ncity)).json()
                print(res)
                if res['cod']==200:
                    form.save()
                    messages.success(request," "+Ncity+"Added Successfully..")
                else:
                    messages.error(request,"City Does Not Exists..")
            else:
                messages.error(request,"City Already Exists...")

    form=CityForm()
    cities=City.objects.all()
    data=[]
    for city in cities:
        res=requests.get(url.format(city)).json()
        city_weather={
            'city':city,
            'temperature':res['main']['temp'],
            'description':res['weather'][0]['description'],
            'country':res['sys']['country'],
            'icon':res['weather'][0]['icon'],
        }
        data.append(city_weather)
    context={'data':data,'form':form}
    return render(request,"weatherapp.html",context)

def delete_city(request,CName):
    City.objects.get(name=CName).delete()
    messages.success(request," "+CName+"Removed Successfully...")
    return redirect('Home')

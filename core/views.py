from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
import csv
from tkinter import Tk
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
@login_required
def export_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    fieldnames = [ 'Email', 'First Name', 'Last Name']
    writer = csv.DictWriter(response, fieldnames=fieldnames)
    writer.writeheader()
    User = get_user_model()
    all_users = User.objects.all()
    for user in all_users:
        writer.writerow({
                         'Email': user.email,
                         'First Name': user.first_name,
                         'Last Name': user.last_name})

    return response
@login_required
def import_csv(request):
    csv_file = request.FILES.get('csv_file')
    try:
        if csv_file is not None:
            User = get_user_model()
            
            decoded_file = csv_file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
            next(reader)
            for i in reader:
                print(i)
                user=User(
                email = i[0],
                first_name = i[1],
                last_name = i[2]
                )
                user.save()
            messages.success(request,"Data ImportSuccessfully.........!!")     
            return redirect('home')
    except:
        return HttpResponse("Data Is alredy exits in this model....")
    return render(request,'import_csv.html')
@login_required
def home(request):
    User = get_user_model()
    all_usr=User.objects.all().values()
    return render(request,"home.html",{'all_usr':all_usr})

@login_required
def register(request):
    User = get_user_model()
    if request.method=="POST":
        email=request.POST['email']
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        password=request.POST['password']

        usr=User(email=email,first_name=firstname,last_name=lastname)
        usr.set_password(password)
        usr.save()
        return redirect('home')
    return render(request,"register.html")


def login1(request):
    if request.method=="POST":
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email,password=password)
        if user:
            login(request, user)
            messages.success(request,"login Successfully....")
            return redirect("home")
        else:
            messages.info(request,"Please enter valid information.........!!!")
            return redirect("/")        
    return render(request,"login.html")

def logout1(request):
    logout(request)
    return redirect('/')



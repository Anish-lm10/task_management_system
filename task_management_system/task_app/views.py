from django.shortcuts import render,redirect

from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from django.contrib import messages

from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime,timedelta

# Create your views here.

# AUTHENTICATION LOGIC
def log_in(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,"Username is not registered")
            return redirect('log_in')

        user=authenticate(username=username,password=password)
        
        if user is None:
            messages.error(request,"Incorrect Password!!")
            return redirect('log_in')
        
        if user is not None: 
            login(request,user)
            messages.success(request,"Login Successfully!!")
            return redirect('home')
    return render(request,'myhtml/auth/login.html')

def sign_up(request):
    if request.method == 'POST':
        firstname=request.POST.get('fname')
        lastname=request.POST.get('lname')
        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        cpassword=request.POST.get('cpassword')

        try:
            if not re.search(r'[A-Z]',password):
                messages.error(request,"Password must contain atleast one capital letter")
                return redirect('sign_up')
            if not re.search(r'\d',password):
                messages.error(request,"Password must contain atleast one digit")
                return redirect('sign_up')
            if not re.search(r'[!@#$%^&*()]',password):
                messages.error(request,"Password must contain atleast one special character")
                return redirect('sign_up')
            
            validate_password(password)

            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.error(request,"Username Already Exists!! Try different username!!")
                    return redirect('sign_up')
                
                elif User.objects.filter(email=email).exists():
                    messages.error(request,"Email Already Exists")
                    return redirect('sign_up')
                
                else:
                    User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                    messages.success(request,"User has been Successfully Registered")
                    return redirect('log_in')
            else:
                messages.error(request,"Password must be same!!")
                return redirect('sign_up')
        
        except ValidationError as e:
            for error in e.messages:
                messages.error(request,error)
                return redirect('sign_up')

    return render(request,'myhtml/auth/register.html')

def log_out(request):
    logout(request)
    return redirect('log_in')

def change_password(request):
    form=PasswordChangeForm(user=request.user)
    return render (request,'myhtml/auth/change_password.html',{'form':form})

#AUTHENTICATION LOGIC ENDS



# MAIN-PAGE logic starts

#dashboard page logic starts
@login_required(login_url='log_in')
def home(request):   
    current_user=request.user #gets current user login username

    create_completed=Create_task.objects.filter(is_completed=True,user=request.user).count()
    assigned_completed=Assign_task.objects.filter(is_completed=True,assigned_by=request.user).count()

    completed=create_completed + assigned_completed

    current=Create_task.objects.filter(is_completed=False,user=request.user,is_deleted=False).count()
    assigned_count=Assign_task.objects.filter(assign_to=request.user,is_completed=False).count()

    if request.user.is_authenticated:
        data=Create_task.objects.filter(is_completed=False,user=request.user,is_deleted=False).values()

        if request.method == 'POST':
            searched= request.POST.get('searched')
            if searched:
                data=data.filter(Q(title__icontains=searched) | Q(status__icontains=searched))
                if not data.exists():
                    messages.error(request,"No such task found!!")
                    return redirect('home')
    else:
        data=[]
    return render(request,'myhtml/home.html',{'data':data,'count':current,'completed_no':completed,'username':current_user,'assigned_count':assigned_count}) 
#dashboard page logic ends


#create a task logic starts
def create(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        status=request.POST.get('status')
        sdate=request.POST.get('sdate')
        edate=request.POST.get('edate')
        user=request.user

        create=Create_task.objects.create(title=title,description=description,status=status,start_date=sdate,end_date=edate,user=user)
        create.save()
        messages.success(request,"Task has been successfully created")
        return redirect('home')

    return render (request,'myhtml/create.html')
#create a task logic ends


# view task logic starts
def view(request):
    data=Create_task.objects.filter(is_completed=False,is_deleted=False,user=request.user)
    return render (request,'myhtml/view.html',{'data':data})
# view task logic ends


# assign a task logic starts
def assign(request):
    if request.method == 'POST':
        title=request.POST.get('title')
        description=request.POST.get('description')
        username=request.POST.get('user')
        deadline=request.POST.get('edate')
        assigned_by=request.user

        if User.objects.filter(username=username).exists():

            user_instance=User.objects.get(username=username)
            user_instance2=User.objects.get(username=assigned_by)

            assigned=Assign_task.objects.create(title=title,description=description,assign_to=user_instance,deadline=deadline,assigned_by=user_instance2)
            assigned.save()
            messages.success(request,"Task has been successfully assigned!!")
            return redirect('assign')
        else:
            messages.error(request,"No such username exists")
            return redirect('assign')
        
    return render (request,'myhtml/assign.html')
# assign a task logic 


# Assigned task logic starts
def assigned(request):
    tasks=Assign_task.objects.filter(assign_to=request.user,is_completed=False)
    return render (request,'myhtml/assigned.html',{'data':tasks})
# Assigned task logic ends

#completed tasks logic starts
def completed_task(request):
    data=Create_task.objects.filter(is_completed=True,user=request.user)
    datas=Assign_task.objects.filter(is_completed=True,assigned_by=request.user)
    return render(request,'myhtml/completed_tasks.html',{'data':data,'datas':datas})
#completed tasks logic ends

# trash/recycle logic starts
def trash(request):
    removed=Create_task.objects.filter(is_deleted=True,user=request.user)
    time=datetime.now()-timedelta(days=29)
    time1=Create_task.objects.filter(clear_datetime__lt=time)
    time1.delete()
    return render (request,'myhtml/recycle.html',{'data':removed})
# trash/recycle logic ends

# Three btn in views.html starts
def completed(request,id):
    complete=Create_task.objects.get(id=id)
    complete.is_completed=True
    complete.save()
    messages.success(request,"Task has been marked completed!!")
    return redirect('view')

def deleted(request,id):
    remove=Create_task.objects.get(id=id)
    remove.delete()
    remove.is_deleted=True
    remove.save()
    messages.success(request,"Task has been deleted sucessfully!!")
    return redirect('view')

def edit(request,id):
    edits=Create_task.objects.get(id=id)
    if request.method == 'POST':
        edits.title=request.POST.get('title')
        edits.description=request.POST.get('description')
        edits.status=request.POST.get('status')
        edits.start_date=request.POST.get('sdate')
        edits.end_date=request.POST.get('edate')

        edits.save()
        messages.success(request,"Data has been edited successfully!!")
        return redirect('view')
    return render(request,'myhtml/edit.html',{'data':edits})

#three btn in views.html ends


# for assigned.html complete btn starts
def acompleted(request,id):
    complete=Assign_task.objects.get(id=id)
    complete.is_completed=True
    complete.save()
    messages.success(request,"Task has been marked completed!!")
    return redirect('assigned')
# for assigned.html complete btn ends


# for completed_task delete_all btn starts
def my_delete_all(request):
    data=Create_task.objects.filter(is_completed=True,user=request.user)
    data.delete()
    messages.success(request,"All completed tasks has been deleted!!")
    return redirect('completed_task')

def assign_delete_all(request):
    datas=Assign_task.objects.filter(is_completed=True,assigned_by=request.user)
    datas.delete()
    messages.success(request,"All assigned completed tasks has been deleted!!")
    return redirect('completed_task')

# for completed_task delete_all btn ends


#in recycle.html restore btn logic starts
def recycle(request,id):
    restore=Create_task.objects.get(id=id)
    restore.is_deleted=False
    restore.save()
    messages.success(request,"Data Successfully Restored")
    return redirect('view')
#in recycle.html restore btn logic ends


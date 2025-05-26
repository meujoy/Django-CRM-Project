from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

def home(request):
    records = Record.objects.all() #retreiving all the records
    #check to see if user is logged in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #Authenticate
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            messages.success(request,"You Have Been Logged In")
            return redirect('home')
        else:
            messages.success(request,"There Was An Error Logging In, Please Try Again...")
            return redirect('home')
    else:
        return render(request,'home.html',{'records':records})

def logout_user(request):
    logout(request)
    messages.success(request,"You Have Been logged Out")
    return redirect('home')

def register_user(request):
    if request.method == 'POST':
        form  = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,"You Have Successfully Registered")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request,'register.html',{'form':form})
    
    return render(request,'register.html',{'form':form})

def customer_record(request,pk):
    if request.user.is_authenticated:
        #look up records
        customer_record = Record.objects.get(id=pk) #getting the record from the record class we created earlier with key as ID
        return render(request,'record.html',{'customer_record':customer_record})
    else:
        messages.success(request,"You must be logged in to view this page")
        return redirect('home')
    
def delete_record(request,pk):
    if request.user.is_authenticated:
        deleted_record = Record.objects.get(id=pk)
        deleted_record.delete()
        messages.success(request,"Record Deleted Successfully")
        return redirect('home')
    else:
        messages.success(request,"You Must Be Logged In To Delete")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid:
                add_record = form.save()
                messages.success(request,"Record Added Successfully")
                return redirect('home')
        return render(request,'add_record.html',{'form':form})
    else:
        messages.success(request,"You Must Be Logged In To Add Record")
        return redirect('home')

def update_record(request,pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None,instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request,"Record Updated Successfully")
            return redirect('home')
        return render(request,'update_record.html',{'form':form})
    else:
        messages.success(request,"You Must Be Logged In To Add Record")
        return redirect('home')
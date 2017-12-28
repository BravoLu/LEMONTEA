from django.shortcuts import render, redirect
from LemonApp.forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login, logout 
import os

# Create your views here.
def home(request):
	return render(request, 'login.html', locals())

def loginORsignup(request):
	if request.method == 'POST':
		if 'email' in request.POST:
			signupform = SignupForm(data=request.POST,auto_id="%s")
			loginform = LoginForm(auto_id="%s")
			if signupform.is_valid():
				UserModel = get_user_model()
				username = signupform.cleaned_data['username']
				email = signupform.cleaned_data['email']
				password = signupform.cleaned_data['password']
				user = UserModel.objects.create_user(username=username,email=email,password=password)
				user.save()
				auth_user = authenticate(username=username,password=password)
				auth_login(request, user)
				return redirect("home")
		else:
			loginform = LoginForm(data=request.POST, auto_id="%s")
			signupform = SignupForm(auto_id="%s")			
			if loginform.is_valid():		
				user = authenticate(username=loginform.cleaned_data['username'], password=loginform.cleaned_data['password'])			
				auth_login(request, user)
				return redirect("home")
	else:
		loginform = LoginForm(auto_id="%s")
		signupform = SignupForm(auto_id="%s")
	return render(request, 'loginORsignup.html', locals())

def signup(request):
	if request.method == 'POST':
		form = SignupForm(data=request.POST,auto_id="%s")
		if form.is_valid():
			UserModel = get_user_model()
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password = form.cleaned_data['password']
			user = UserModel.objects.create_user(username=username,email=email,password=password)
			user.save()
			auth_user = authenticate(username=username,password=password)
			auth_login(request,auth_user)
			return redirect("login")
		else:
			return redirect("loginORsignup")

def login(request):
	if request.method =='POST':
		form = LoginForm(data=request.POST, auto_id="%s")			
		if form.is_valid():		
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])			
			auth_login(request,user)
			return redirect("home")
		else:
			return redirect("loginORsignup")

def elements(request):
	return render(request,'elements.html')

def generic(request):
	return render(request,'generic.html')
	
# def home(request):
# 	return render(request,'index.html')

def create(request):
	return render(request,'create.html')

def identity(request):
	context = {}
	return render(request, 'personal-info.html', context)

def shop(request):
	context = {}
	return render(request,'shopcpy.html',context)

def course(request):
	context = {}
	return render(request,'courseui.html',context)

def study(request):
	context = {}
	return render(request,'study.html',context)

def share(request):
	context = {}
	return render(request,'share.html',context)	

def logout_view(request):
	logout(request)
	return redirect('home')

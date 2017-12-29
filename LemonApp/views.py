from django.shortcuts import render, redirect
from LemonApp.forms import SignupForm, LoginForm, CourseForm, ChapterForm, PPTForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login, logout 
from LemonApp.models import Course, ChapterList, PPTList
import os

# Create your views here.
def home(request):
	#return render(request, 'login.html', locals())
	return render(request, 'index.html')

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
			return redirect("home")
	else:
		form = SignupForm(auto_id="%s")
	return render(request, "logup.html", locals())

def login(request):
	if request.method =='POST':
		form = LoginForm(data=request.POST, auto_id="%s")			
		if form.is_valid():		
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])			
			auth_login(request,user)
			return redirect("home")
		else:
			print(form.errors)
	else:
		form = LoginForm(auto_id="%s")
	return render(request, "login.html", locals())

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
	return render(request,'shop.html',context)

def course(request):
	context = {}
	return render(request,'course.html',context)

def study(request):
	context = {}
	return render(request,'study.html',context)

def share(request):
	context = {}
	return render(request,'share.html',context)	

def logout_view(request):
	logout(request)
	return redirect('home')

def school(request):
	CourseList = Course.objects.all()
	return render(request,'school.html', locals())

def community(request):
	context = {}
	return render(request,'community.html',context)

def page(request):
	context = {}
	return render(request,'page.html',context)

def create_course(request):
	if request.method == 'POST':
		form = CourseForm(request.POST, request.FILES, auto_id="%s")
		if form.is_valid():
			course_identifier = form.cleaned_data["course_identifier"]
			title = form.cleaned_data["title"]
			image = form.cleaned_data["image"]
			description = form.cleaned_data["description"]
			teacher = form.cleaned_data["teacher"]
			if(image):
				course = Course(course_identifier=course_identifier,title=title,image=image,description=description,teacher=teacher)
			else:
				course = Course(course_identifier=course_identifier,title=title,description=description,teacher=teacher)
			course.save()
			return redirect("school")
	else:
		form = CourseForm(auto_id="%s")
	return render(request, "create_course.html", locals())

def add_chapter(request):
	pass

def add_ppt(request):
	pass

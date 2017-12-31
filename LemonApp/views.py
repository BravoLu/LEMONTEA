from django.shortcuts import render, redirect
from LemonApp.forms import SignupForm, LoginForm, CourseForm, ChapterForm, PPTForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login, logout 
from LemonApp.models import College, Course, ChapterList, PPTList
import os

# Create your views here.
def testpage(request):
	college_list = College.objects.all()
	return render(request,'personal-setting.html', locals())

def home(request):
	college_list = College.objects.all()
	#return render(request, 'login.html', locals())
	return render(request, 'index.html', locals())

def signup(request):
	path = request.path
	college_list = College.objects.all()
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
			old_path = path[0:path.find('signup')]
			return redirect(old_path)
	else:
		form = SignupForm(auto_id="%s")
	return render(request, "logup.html", locals())

def login(request):
	path = request.path
	college_list = College.objects.all()
	if request.method =='POST':
		form = LoginForm(data=request.POST, auto_id="%s")			
		if form.is_valid():		
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])			
			auth_login(request,user)
			old_path = path[0:path.find('login')]
			return redirect(old_path)
	else:
		form = LoginForm(auto_id="%s")
	return render(request, "login.html", locals())


def logout_view(request):
	logout(request)
	path = request.path
	old_path = path[0:path.find('logout')]
	return redirect(old_path)

def identity(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	return render(request, 'personal-info.html', locals())

def shop(request):
	college_list = College.objects.all()
	return render(request,'shop.html',locals())

def study(request):
	college_list = College.objects.all()
	return render(request,'study.html',locals())

def share(request):
	college_list = College.objects.all()
	return render(request,'share.html',locals())	




def page(request):
	college_list = College.objects.all()
	return render(request,'page.html',locals())

def colleges(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	return render(request,'colleges.html', locals())
	
def courses(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	college_id = int(URL_list[2])
	college = College.objects.filter(id=college_id)[0]
	CourseList = Course.objects.filter(college_id=college)
	return render(request,'courses.html', locals())

def course(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	college_id = int(URL_list[2])
	college = College.objects.filter(id=college_id)[0]
	course_id = int(URL_list[4])
	course = Course.objects.filter(id=course_id)[0]
	chapter_list = ChapterList.objects.filter(course_id=course).order_by("chapter_order")
	chapter_id_list = [chapter.id for chapter in chapter_list]
	ppt_list = []
	for charter_id in chapter_id_list:
		temp_list = PPTList.objects.filter(chapter_id=charter_id).order_by("ppt_order")
		ppt_list.extend(temp_list)
	return render(request,'course.html', locals())

def create_course(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	if request.method == 'POST':
		form = CourseForm(request.POST, request.FILES, auto_id="%s")
		if form.is_valid():
			UserModel = get_user_model()
			URL_list = path.split('/')
			college_id = int(URL_list[2])
			creator_id = request.user.id
			college = College.objects.filter(id=college_id)[0]
			creator = UserModel.objects.filter(id=creator_id)[0]
			course_identifier = form.cleaned_data["course_identifier"]
			title = form.cleaned_data["title"]
			image = form.cleaned_data["image"]
			description = form.cleaned_data["description"]
			teacher = form.cleaned_data["teacher"]
			if image:
				course = Course(college_id=college,creator_id=creator,course_identifier=course_identifier,title=title,image=image,description=description,teacher=teacher)
			else:
				course = Course(college_id=college,creator_id=creator,course_identifier=course_identifier,title=title,description=description,teacher=teacher)
			course.save()
			old_path = path[0:path.find('create_course')]
			return redirect(old_path)
	else:
		form = CourseForm(auto_id="%s")
	return render(request, "create_course.html", locals())

def add_chapter(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	if request.method == 'POST':
		form = ChapterForm(data=request.POST, auto_id="%s")
		if form.is_valid():
			URL_list = path.split('/')
			course_id = int(URL_list[4])
			course = Course.objects.filter(id=course_id)[0]
			chapter_order = ChapterList.objects.filter(course_id=course).count() + 1
			title = form.cleaned_data["title"]
			description = form.cleaned_data["description"]
			chapter = ChapterList(course_id=course, chapter_order=chapter_order, title=title, description=description)
			chapter.save()
			old_path = path[0:path.find('add_chapter')]
			return redirect(old_path)
	else:
		form = ChapterForm(auto_id="%s")
	return render(request, "add_chapter.html", locals())

def add_ppt(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	if request.method == 'POST':
		form = PPTForm(request.POST, request.FILES, auto_id="%s")
		if form.is_valid():
			URL_list = path.split('/')
			chapter_id = int(URL_list[6])
			chapter = ChapterList.objects.filter(id=chapter_id)[0]
			ppt_order = PPTList.objects.filter(chapter_id=chapter).count() + 1
			title = str(form.cleaned_data["file"])
			file = form.cleaned_data["file"]
			ppt = PPTList(chapter_id=chapter, ppt_order=ppt_order, title=title, file=file)
			ppt.save()
			old_path = path[0:path.find('chapter')]
			return redirect(old_path)
	else:
		form = PPTForm(auto_id="%s")
	return render(request, "add_ppt.html", locals())

def show_ppt(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	pass

def download(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	else:
		path = request.path
		URL_list = path.split('/')
		download_path = str(PPTList.objects.get(id=int(URL_list[4])).file)
		download_path = "/LemonApp/media/" + download_path
		return redirect(download_path)

def goback(request):
	pass

def tips(request): #验证权限
	path = request.path
	URL_list = path.split('/')
	if not request.user.id:
		return 1 #1-未登录

	if "identity" in path:
		return 0 #0-通过验证

	if "colleges" in path:
		# if request.user.permission <= 1:
		# 	return 2 #2-不是学生/老师
		# else:
		return 0 #0-通过验证

	if "college" in path:
		if request.user.permission < 10: #非管理员
			if request.user.permission <= 1:
				return 2 #2-不是学生/老师
			if College.objects.filter(id=int(URL_list[2])).count() == 0: #没有这个院校
				return 3 #3-没有这个院校
			if int(URL_list[2]) != request.user.college_id: #自己不属于此院校
				return 4 #4-自己不属于此院校

			if "create_course" in path:
				if request.user.permission <= 2:
					return 5 #5-没权限创建课程
				else:
					return 0 #0-通过验证	

			if "course" in path:
				if Course.objects.filter(id=int(URL_list[4])).count() == 0: #没有这个课程
					return 6 #6-没有这个课程

				if "add_chapter" in path:
					if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id: #课程不属于自己
						return 7 #7-没权限添加章节
					else:
						return 0 #0-通过验证

				if "chapter" in path:
					if ChapterList.objects.filter(id=int(URL_list[6])).count == 0: #没有这个章节
						return 8 #8-没有这个章节

					if "add_ppt" in path:
						if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id:#课程不属于自己
							return 9 #9-没权限添加ppt
						else:
							return 0 #0-通过验证

					if "ppt" in path:
						if PPTList.objects.filter(id=int(URL_list[8])).count == 0: #没有这个PPT
							return 10 #10-没有这个PPT
						else:
							return 0 #0-通过验证
					else:
						return 0 #0-通过验证
				else:
					return 0 #0-通过验证

			if "LemonApp" in path:
				if PPTList.objects.filter(id=int(URL_list[3])).count == 0: #没有这个PPT
					return 10 #10-没有这个PPT
				else:
					return 0 #0-通过验证
			
			return 0 #0-通过验证

		else: #管理员
			if College.objects.filter(id=int(URL_list[2])).count() == 0: #没有这个院校
				return 3 #3-没有这个院校

			if "create_course" in path:
				return 0 #0-通过验证	

			if "course" in path:
				if Course.objects.filter(id=int(URL_list[4])).count() == 0: #没有这个课程
					return 6 #6-没有这个课程

				if "add_chapter" in path:
					return 0 #0-通过验证

				if "chapter" in path:
					if ChapterList.objects.filter(id=int(URL_list[6])).count == 0: #没有这个章节
						return 8 #8-没有这个章节

					if "add_ppt" in path:
						return 0 #0-通过验证

					if "ppt" in path:
						if PPTList.objects.filter(id=int(URL_list[8])).count == 0: #没有这个PPT
							return 10 #10-没有这个PPT
						else:
							return 0 #0-通过验证
					else:
						return 0 #0-通过验证
				else:
					return 0 #0-通过验证

			if "downloadppt" in path:
				if PPTList.objects.filter(id=int(URL_list[4])).count() == 0: #没有这个PPT
					return 10 #10-没有这个PPT
				else:
					return 0 #0-通过验证
			
			return 0 #0-通过验证


				






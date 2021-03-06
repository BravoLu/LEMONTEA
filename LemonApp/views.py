from django.shortcuts import render, redirect
from LemonApp.forms import SignupForm, LoginForm, CourseForm, ChapterForm, PPTForm, ModifyInfoForm, BindForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate,login as auth_login, logout 
from LemonApp.models import College, TeacherInformation, StudentInformation, Course, ChapterList, PPTList, CourseComment, PPTComment
import os

from LemonTea.settings import DEBUG

if not DEBUG:
	from .tasks import ppt_to_img

# Create your views here.
def identity(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.user.college_id != -1:
		college = College.objects.filter(id=request.user.college_id)[0]
		college_name = college.name
	else:
		college_name = "未绑定"
	return render(request, 'personal-info.html', locals())

def modify_info(request):
	path = request.path
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.method == 'POST':
		form = ModifyInfoForm(data=request.POST,auto_id="%s")
		if form.is_valid():
			UserModel = get_user_model()
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			user = UserModel._default_manager.get(id=request.user.id)
			user.username = username
			user.email = email
			user.save()
			old_path = path[0:path.find('modify_info')]
			return redirect(old_path)
	else:
		form = ModifyInfoForm(auto_id="%s")
	return render(request, "personal-setting.html", locals())

def bind_college(request):
	path = request.path
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.method == 'POST':
		form = BindForm(data=request.POST,auto_id="%s")
		if form.is_valid():
			UserModel = get_user_model()
			college = form.cleaned_data['college']
			status = form.cleaned_data['status']
			card_number = form.cleaned_data['card_number']
			user = UserModel._default_manager.get(id=request.user.id)
			user.college_id = college.id
			user.permission = int(status) + 1
			user.card_number = card_number
			user.save()
			if status == '1':
				information = StudentInformation.objects.filter(college_id=college.id, StudentID=card_number).update(is_bind=True)
			else:
				information = TeacherInformation.objects.filter(college_id=college.id, TeacherID=card_number).update(is_bind=True)
			old_path = path[0:path.find('bind_college')]
			return redirect(old_path)
	else:
		form = BindForm(auto_id="%s")
		if request.user.college_id != -1:
			college = College.objects.filter(id=request.user.college_id)[0]
			college_name = college.name
		else:
			college_name = "未绑定"
	return render(request, "personal-binding.html", locals())

def change_face(request):
	path = request.path
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.method == 'POST':
		image = request.FILES['face']
		UserModel = get_user_model()
		account = UserModel.objects.filter(id=request.user.id)[0]
		account.face = image
		account.save()
	old_path = path[0:path.find('change_face')]
	return redirect(old_path)

def home(request):
	college_list = College.objects.all()
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
	return redirect("home")

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
	ppt_list = []
	for chapter in chapter_list:
		temp_list = PPTList.objects.filter(chapter_id=chapter).order_by("ppt_order")
		ppt_list.extend(temp_list)

	comment_list = CourseComment.objects.filter(course_id=course).order_by("comment_order")

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

def add_comment(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.method == 'POST':
		path = request.path
		URL_list = path.split('/')

		course_id = int(URL_list[4])
		course = Course.objects.filter(id=course_id)[0]
		account_id = request.user.id
		UserModel = get_user_model()
		account = UserModel.objects.filter(id=account_id)[0]

		comment_order = CourseComment.objects.filter(course_id=course).count() + 1
		content = request.POST['content']
		comment = CourseComment(course_id=course, account_id=account, comment_order=comment_order, content=content)
		comment.save()
	old_path = path[0:path.find('add_comment')]
	return redirect(old_path)

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
			
			os.mkdir(os.path.join(os.path.split(ppt.file.path)[0], os.path.splitext(os.path.split(ppt.file.path)[1])[0]))
			# TODO: split
			# 目前ppt切图只能在生产环境（linux）下使用，开发环境关闭
			if not DEBUG:
				ppt_to_img.delay(ppt.file.path, ppt.pk)
			print(ppt.file.path)
	old_path = path[0:path.find('chapter')]
	return redirect(old_path)

def show_ppt(request):
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
	chapter_id = int(URL_list[6])
	chapter = ChapterList.objects.filter(id=chapter_id)[0]
	ppt_id = int(URL_list[8])
	ppt = PPTList.objects.filter(id=ppt_id)[0]
	#ppt_page_list = PPTImage.objects.filter(ppt_id=ppt)
	img_base_url = '/LemonApp/media/PPT/' + os.path.splitext(os.path.split(ppt.file.path)[1])[0] + '/'
	ppt_page_pair = [("%s.jpg" % page,  PPTComment.objects.filter(ppt=ppt, page_num=page).count()) for page in range(0, ppt.page_count)]
	#print(ppt_page_pair)
	#print(img_base_dir)
	return render(request, 'ppt_preview.html', locals())

def show_ppt_page(request):
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	college_id = int(URL_list[2])
	college = College.objects.filter(id=college_id)[0]
	course_id = int(URL_list[4])
	course = Course.objects.filter(id=course_id)[0]
	chapter_id = int(URL_list[6])
	chapter = ChapterList.objects.filter(id=chapter_id)[0]
	ppt_id = int(URL_list[8])
	ppt = PPTList.objects.filter(id=ppt_id)[0]
	print(ppt.page_count)
	page_num = int(URL_list[9])
	page_num = page_num+1
	img_base_url = '/LemonApp/media/PPT/' + os.path.splitext(os.path.split(ppt.file.path)[1])[0] + '/'
	ppt_comment_list = PPTComment.objects.filter(ppt=ppt, page_num=page_num-1)
	#assert(False)
	return render(request, "ppt_page.html", locals())

def ppt_comment_commit(request):
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	if request.method == 'POST':
		path = request.path
		URL_list = path.split('/')
		ppt_id = int(URL_list[8])
		ppt = PPTList.objects.filter(id=ppt_id)[0]
		
		account_id = request.user.id
		UserModel = get_user_model()
		account = UserModel.objects.filter(id=account_id)[0]
		page_num = int(URL_list[9])
		comment_order = PPTComment.objects.filter(ppt=ppt, page_num=page_num).count() + 1
		content = request.POST['content']
		comment = PPTComment(ppt=ppt, account_id=account, comment_order=comment_order, content=content, page_num=page_num)
		comment.save()
	old_path = path[0:path.find('add_comment')]
	return redirect(old_path)

def download(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	else:
		path = request.path
		URL_list = path.split('/')
		download_path = str(PPTList.objects.get(id=int(URL_list[8])).file)
		download_path = "/LemonApp/media/" + download_path
		return redirect(download_path)

def delete_course(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	course_id = int(URL_list[4])
	Course.objects.filter(id=course_id).delete()
	old_path = path[0:path.find('course')]
	return redirect(old_path)

def delete_chapter(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	course_id = int(URL_list[4])
	course = Course.objects.filter(id=course_id)[0]
	chapter_id = int(URL_list[6])
	ChapterList.objects.filter(id=chapter_id).delete()
	chapter_list = ChapterList.objects.filter(course_id=course).order_by("chapter_order")
	count = 1
	for chapter in chapter_list: #重新排序
		chapter.chapter_order = count
		chapter.save()
		count += 1

	old_path = path[0:path.find('chapter')]
	return redirect(old_path)


def delete_ppt(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	chapter_id = int(URL_list[6])
	chapter = ChapterList.objects.filter(id=chapter_id)[0]
	ppt_id = int(URL_list[8])
	PPTList.objects.filter(id=ppt_id).delete()
	ppt_list = PPTList.objects.filter(chapter_id=chapter).order_by("ppt_order")
	count = 1
	for ppt in ppt_list: #重新排序
		ppt.ppt_order = count
		ppt.save()
		count += 1

	old_path = path[0:path.find('chapter')]
	return redirect(old_path)

def delete_comment(request):
	college_list = College.objects.all()
	error_type = tips(request)
	if error_type > 0:
		return render(request,'tips.html', locals())
	path = request.path
	URL_list = path.split('/')
	course_id = int(URL_list[4])
	course = Course.objects.filter(id=course_id)[0]
	comment_id = int(URL_list[6])
	CourseComment.objects.filter(id=comment_id).delete()
	comment_list = CourseComment.objects.filter(course_id=course).order_by("comment_order")
	count = 1
	for comment in comment_list: #重新排序
		comment.comment_order = count
		comment.save()
		count += 1

	old_path = path[0:path.find('comment')]
	return redirect(old_path)

def goback(request):
	path = request.path
	index = path.rfind('/')
	if path.rfind('/', 0, index) != -1:
		old_path = path[0:path.rfind('/', 0, index)+1]
	return redirect(old_path)



def testpage(request):
	pass

def tips(request): #验证权限
	path = request.path
	URL_list = path.split('/')
	if not request.user.id:
		return 1 #1-未登录

	if "/identity/" in path:
		return 0 #0-通过验证

	if "/colleges/" in path:
		# if request.user.permission <= 1:
		# 	return 2 #2-不是学生/老师
		# else:
		return 0 #0-通过验证

	if "/college/" in path:
		if request.user.permission < 10: #非管理员
			if request.user.permission <= 1:
				return 2 #2-不是学生/老师
			if College.objects.filter(id=int(URL_list[2])).count() == 0: #没有这个院校
				return 3 #3-没有这个院校
			if int(URL_list[2]) != request.user.college_id: #自己不属于此院校
				return 4 #4-自己不属于此院校

			if "/create_course/" in path:
				if request.user.permission <= 2:
					return 5 #5-没权限创建课程
				else:
					return 0 #0-通过验证	

			if "/course/" in path:
				if Course.objects.filter(id=int(URL_list[4])).count() == 0: #没有这个课程
					return 6 #6-没有这个课程

				if "/delete_course/" in path:
					if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id: #课程不属于自己
						return 11 #11-没权限删除课程
					else:
						return 0 #0-通过验证

				if "/add_chapter/" in path:
					if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id: #课程不属于自己
						return 7 #7-没权限添加章节
					else:
						return 0 #0-通过验证

				if "/add_comment/" in path:
					return 0 #0-通过验证

				if "/delete_comment/" in path:
					if CourseComment.objects.filter(id=int(URL_list[6])).count() == 0:
						return 12 #12-没有这条评论
					elif CourseComment.objects.get(id=int(URL_list[6])).account_id.id != request.user.id:
						return 13 #13-评论不属于自己
					else:
						return 0 #0-通过验证

				if "/chapter/" in path:
					if ChapterList.objects.filter(id=int(URL_list[6])).count == 0: #没有这个章节
						return 8 #8-没有这个章节

					if "/delete_chapter/" in path:
						if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id: #课程不属于自己
							return 14 #14-没权限删除章节
						else:
							return 0 #0-通过验证

					if "/add_ppt/" in path:
						if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id:#课程不属于自己
							return 9 #9-没权限添加ppt
						else:
							return 0 #0-通过验证

					if "/ppt/" in path:
						if PPTList.objects.filter(id=int(URL_list[8])).count == 0: #没有这个PPT
							return 10 #10-没有这个PPT

						if "/delete_ppt/" in path:
							if Course.objects.get(id=int(URL_list[4])).creator_id.id != request.user.id:#课程不属于自己
								return 15 #15-没权限删除ppt
							else:
								return 0 #0-通过验证

						if "/downloadppt/" in path:
							return 0

						return 0 #0-通过验证

					return 0 #0-通过验证

				return 0 #0-通过验证

			return 0 #0-通过验证

		else: #管理员
			if College.objects.filter(id=int(URL_list[2])).count() == 0: #没有这个院校
				return 3 #3-没有这个院校

			if "/create_course/" in path:
				return 0 #0-通过验证	

			if "/course/" in path:
				if Course.objects.filter(id=int(URL_list[4])).count() == 0: #没有这个课程
					return 6 #6-没有这个课程

				if "/delete_course/" in path:
					return 0 #0-通过验证

				if "/add_chapter/" in path:
					return 0 #0-通过验证

				if "/add_comment/" in path:
					return 0 #0-通过验证

				if "/delete_comment/" in path:
					if CourseComment.objects.filter(id=int(URL_list[6])).count() == 0:
						return 12 #12-没有这条评论
					else:
						return 0 #0-通过验证

				if "/chapter/" in path:
					if ChapterList.objects.filter(id=int(URL_list[6])).count == 0: #没有这个章节
						return 8 #8-没有这个章节

					if "/delete_chapter/" in path:
						return 0 #0-通过验证

					if "/add_ppt/" in path:
						return 0 #0-通过验证

					if "/ppt/" in path:
						if PPTList.objects.filter(id=int(URL_list[8])).count == 0: #没有这个PPT
							return 10 #10-没有这个PPT

						if "/delete_ppt/" in path:
							return 0 #0-通过验证

						if "/downloadppt/" in path:
							return 0

			return 0 #0-通过验证
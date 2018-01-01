from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from LemonApp.models import College, TeacherInformation, StudentInformation, Course, ChapterList, PPTList

STATUS_CHOICES = [
	('','---------'),
	('1', '学生'),
	('2', '老师')
]

class SignupForm (forms.Form):
	username = forms.CharField(
		required=True, min_length=3, max_length=20, widget=forms.TextInput(attrs={'placeholder':'用户名'}))

	email = forms.EmailField(
		required=True, widget=forms.EmailInput(attrs={'placeholder':'邮箱'}))

	password = forms.CharField(
		required=True, min_length=6, max_length=20, widget = forms.PasswordInput(attrs={'placeholder':'密码'}))

	confirm_password = forms.CharField(
		required=True, min_length=6, max_length=20, widget = forms.PasswordInput(attrs={'placeholder':'确认密码'}))

	def clean_username(self):
		UserModel = get_user_model()
		username = self.cleaned_data["username"]
		try:
			UserModel._default_manager.get(username = username)
		except UserModel.DoesNotExist:
			return username
		raise forms.ValidationError("This username has been registered")

class  LoginForm (forms.Form):
	username = forms.CharField(
		required=True, min_length=3, max_length=20, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
	password = forms.CharField(
		required=True, min_length=6, max_length=20, widget=forms.PasswordInput(attrs={'placeholder':'密码'}))
	
	def clean_password(self):
		username = self.cleaned_data["username"]
		password = self.cleaned_data["password"]
		user = authenticate(username=username,password= password)
		if user is None:
			raise forms.ValidationError("Usename or password is wrong")
		return password

class CourseForm (forms.Form):
	course_identifier = forms.CharField(
		required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'课程号'}))

	title = forms.CharField(
		required=True, max_length=50, widget=forms.TextInput(attrs={'placeholder':'课程名称'}))

	image = forms.ImageField(
		required=False, widget=forms.ClearableFileInput(attrs={'placeholder':'选择课程图片'}))

	description = forms.CharField(
		required=True, max_length=200, widget=forms.Textarea(attrs={'placeholder':'课程描述'}))

	teacher = forms.CharField(
		required=True, max_length=20, widget = forms.TextInput(attrs={'placeholder':'授课老师'}))

	def clean_course_identifier(self):
		course_identifier = self.cleaned_data["course_identifier"]
		List = Course.objects.filter(course_identifier=course_identifier)
		if(len(List)):
			raise forms.ValidationError("This course exists")
		return course_identifier

class ChapterForm (forms.Form):
	title = forms.CharField(
		required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'章节标题'}))

	description = forms.CharField(
		required=True, max_length=200, widget=forms.Textarea(attrs={'placeholder':'章节描述'}))

class PPTForm (forms.Form):
	file = forms.FileField(
		required=True, widget=forms.FileInput(attrs={'placeholder':'选择ppt文件'}))

class ModifyInfoForm (forms.Form):
	username = forms.CharField(
		required=True, min_length=3, max_length=20, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
	email = forms.EmailField(
		required=True, widget=forms.EmailInput(attrs={'placeholder':'邮箱'}))

	def clean_username(self):
		UserModel = get_user_model()
		username = self.cleaned_data["username"]
		try:
			UserModel._default_manager.get(username = username)
		except UserModel.DoesNotExist:
			return username
		raise forms.ValidationError("This username has been registered")

class BindForm (forms.Form):
	college = forms.ModelChoiceField(
		required=True, queryset=College.objects.all())

	status = forms.ChoiceField(
		required=True, choices=STATUS_CHOICES)

	card_number = forms.CharField(
		required=True, max_length=20, widget=forms.TextInput(attrs={'placeholder':'请输入学号或教师证号'}))

	def clean_card_number(self):
		college = self.cleaned_data["college"]
		status = self.cleaned_data["status"]
		card_number = self.cleaned_data["card_number"]
		
		if status == '1':
			list1 = StudentInformation.objects.filter(college_id=college.id, StudentID=card_number)
			if list1.count() == 0:
				raise forms.ValidationError("This ID doesn't exists")
			elif list1[0].is_bind == True:
				raise forms.ValidationError("This ID has been binded")
		else:
			list1 = TeacherInformation.objects.filter(college_id=college.id, TeacherID=card_number)
			if list1.count() == 0:
				raise forms.ValidationError("This ID doesn't exists")
			elif list1[0].is_bind == True:
				raise forms.ValidationError("This ID has been binded")
		return card_number

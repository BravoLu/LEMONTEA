from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from LemonApp.models import Course, ChapterList, PPTList

class SignupForm (forms.Form):
	username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'用户名'}))

	email = forms.EmailField(required=False, widget=forms.TextInput(attrs={'placeholder':'邮箱'}))

	password = forms.CharField(required=False, widget = forms.PasswordInput(attrs={'placeholder':'密码'}))

	confirm_password = forms.CharField(required=False, widget = forms.PasswordInput(attrs={'placeholder':'确认密码'}))

	def clean_username(self):
		UserModel = get_user_model()
		username = self.cleaned_data["username"]
		try:
			UserModel._default_manager.get(username = username)
		except UserModel.DoesNotExist:
			return username
		raise forms.ValidationError("This username has been registered")

class  LoginForm (forms.Form):
	username = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
	password = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'placeholder':'密码'}))
	
	def clean_password(self):
		username = self.cleaned_data["username"]
		password = self.cleaned_data["password"]
		user = authenticate(username=username,password= password)
		if user is None:
			raise forms.ValidationError("Usename or password is wrong")
		return password

class CourseForm (forms.Form):
	course_identifier = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'课程号'}))

	title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'课程名称'}))

	image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'placeholder':'选择课程图片'}))

	description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'课程描述'}))

	teacher = forms.CharField(required=False, widget = forms.TextInput(attrs={'placeholder':'授课老师'}))

	def clean_course_identifier(self):
		course_identifier = self.cleaned_data["course_identifier"]
		List = Course.objects.filter(course_identifier=course_identifier)
		if(len(List)):
			raise forms.ValidationError("This course exists")
		return course_identifier

class ChapterForm (forms.Form):
	title = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder':'章节标题'}))

	description = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder':'章节描述'}))

class PPTForm (forms.Form):
	file = forms.FileField(required=False, widget=forms.FileInput(attrs={'placeholder':'选择ppt文件'}))

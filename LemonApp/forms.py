from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

class SignupForm (forms.ModelForm):
	username = forms.CharField( 
		label='用户名', required=True, error_messages={'required': '请填写你的用户名','max_length':'最多只能输入20个字符','min_length':'至少输入3个字符'}, max_length=20, min_length=3, widget=forms.TextInput(attrs={'placeholder':'用户名'}))

	email = forms.EmailField( error_messages={'required': '请填写你的email','invalid':'email格式不正确'},
		label='邮箱', required=True, widget=forms.TextInput(attrs={'placeholder':'邮箱'}))

	password = forms.CharField( error_messages={'required': '请输入密码','max_length':'最多只能输入20个字符','min_length':'至少输入6个字符'},
		label='密码', required=True, max_length=20, min_length=5, widget = forms.PasswordInput(attrs={'placeholder':'密码'}))

	confirm_password = forms.CharField(error_messages={'required': '请输入确认密码','max_length':'最多只能输入20个字符','min_length':'至少输入6个字符'},
		label='确认密码', required=True, max_length=20, min_length=5, widget = forms.PasswordInput(attrs={'placeholder':'确认密码'}))

	class Meta:
		model = get_user_model()
		fields = ("username","email","password",)

	def clean_username(self):
		UserModel = get_user_model()
		username = self.cleaned_data["username"]
		try:
			UserModel._default_manager.get(username = username)
		except UserModel.DoesNotExist:
			return username
		raise forms.ValidationError("有人已经注册了这个用户名")

	def clean_confirm_password(self):
		password = self.cleaned_data.get("password",False)
		confirm_password = self.cleaned_data["confirm_password"]
		if  not( password == confirm_password):
			raise forms.ValidationError("确认密码和密码不一致")
		return confirm_password

class  LoginForm (forms.Form):

	username = forms.CharField( 
		label='用户名', required=True, min_length=3, widget=forms.TextInput(attrs={'placeholder':'用户名'}))
	password = forms.CharField( 
		label='密码', required=True, min_length=5, widget=forms.PasswordInput(attrs={'placeholder':'密码'}))
	
	def clean_password(self):
		username = self.cleaned_data["username"]
		password = self.cleaned_data["password"]
		user = authenticate(username=username,password= password)

		if user is None:
			raise forms.ValidationError("用户名或密码错误")
		return password
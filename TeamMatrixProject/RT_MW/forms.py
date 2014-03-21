import datetime

from django import forms
from django.forms import extras
from django.contrib.auth.models import User
from RT_MW.models import UserProfile,Project,Category,Specification,Lead,Join

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password: ")
    username = forms.CharField(max_length=128, help_text="Username: ")
    first_name = forms.CharField(max_length=128, help_text="First Name: ")
    last_name = forms.CharField(max_length=128, help_text="Second Name: ")
    email = forms.CharField(max_length=128, help_text="Email: ")

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password')

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture',)

class ProjectForm(forms.ModelForm):
    projName = forms.CharField(max_length=128, help_text="Project Title")
    description = forms.CharField(widget=forms.Textarea, help_text="Project Description")
    enrollmentKey = forms.CharField(max_length=128,help_text="Project EnrollmentKey")

    class Meta:
        model = Project
        fields = ('projName','description','enrollmentKey')
        
class CategoryForm(forms.ModelForm):
    class Meta:
	model = Category
	fields = ('cateName',)

class AttributeForm(forms.ModelForm):
    CHOICES = (('1', '1',), ('2', '2',), ('3', '3',), ('4', '4',), ('5', '5',))
    attrTitle = forms.CharField(max_length=128, help_text="TODO Attribute Title")
    attrDate = forms.DateField(widget=extras.SelectDateWidget, help_text="Deadline")
    priority = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, help_text="Priority")
    cateID = forms.ModelChoiceField(queryset=Category.objects.all())
    attrDesc = forms.CharField(widget=forms.Textarea, help_text="Description")
    
    class Meta:
	model = Specification
	fields = ('attrTitle', 'attrDate', 'priority', 'attrDesc', 'cateID')

class LeadForm(forms.ModelForm):
    class Meta:
	model = Lead

class JoinForm(forms.ModelForm):
    class Meta:
	model = Join

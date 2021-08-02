from django import forms
from django.contrib.auth.forms import UserCreationForm

from app.models import User, Course


class UserForm(UserCreationForm):
    """

    """
    gender_choices = (('Male', 'male'), ('Female', 'female'),)

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Type your first name", "required": "True"}), max_length=300,
        required=True,
        label="Firstname", )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Type your last name", "required": "True"}), max_length=300,
        required=True,
        label="Lastname", )

    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Type your preferred username"}),
                               max_length=300, required=True,
                               label="Username", )

    gender = forms.ChoiceField(choices=User.Gender.choices, )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Type your active phone number", "required": "True"}),
        max_length=300,
        required=True,
        label="PhoneNumber", )

    mat_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Type your matriculation number"}),
                                 max_length=300,
                                 required=True,
                                 label="Matriculation Number", )

    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Type your email", "required": "True"}),
                            max_length=300,
                            required=True,
                            label="Email", )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "required": "True"}),
                                max_length=20,
                                label="Password1")

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Type Password again", "required": "True"}), max_length=20,
        label="Password2")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "gender", "phone_number", "phone_number", "email", "password1",
                  "password2", "username", "mat_number", 'image']


class StaffUserForm(UserCreationForm):
    """

    """
    title_choices = (
        ('Mr', 'mr'), ('Mrs', 'mrs'), ('Dr(Mrs)', 'dr(mrs)'), ('Dr', 'dr'), ('Prof(Mrs)', 'prof(mrs)'),
        ('Prof', 'prof'),)

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "First name", "class": "form-control"}), max_length=300,
        required=True,
        label="Firstname", )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Last name", "class": "form-control"}), max_length=300,
        required=True,
        label="Lastname", )

    username = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Username", "class": "form-control"}),
        max_length=300, required=True,
        label="Username", )

    title = forms.ChoiceField(choices=User.Title.choices)
    is_student = forms.BooleanField(
        widget=forms.HiddenInput(attrs={"placeholder": "Type your active phone number", "value": False}),
        required=False,
        label="Student", )

    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={"placeholder": "Phone number", "class": "form-control"}),
        max_length=300,
        required=True,
        label="PhoneNumber", )

    email = forms.CharField(widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"}),
                            max_length=300,
                            required=True,
                            label="Email", )

    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder": "Password", "class": "form-control"}),
                                max_length=20,
                                label="Password1")

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={"placeholder": "Password again", "class": "form-control"}), max_length=20,
        label="Password2")

    class Meta:
        model = User
        fields = ["first_name", "last_name", "phone_number", "phone_number", "email", "password1",
                  "password2", "username", 'is_student', 'title']


class LoginUserForm(forms.Form):
    username = forms.CharField(max_length=30, required=True,
                               widget=forms.TextInput(
                                   attrs={'name': "demo", "class": "form-control", "placeholder": "Username"}),
                               label="Username")
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'name': "demo", "class": "form-control", "placeholder": "Password"}), label="Password")


class AddCourseForm(forms.ModelForm):
    title = forms.CharField(max_length=30, required=True,
                            widget=forms.TextInput(attrs={'name': "demo"}),
                            label="Username")
    course_code = forms.CharField(max_length=30, required=True,
                                  widget=forms.TextInput(attrs={'name': "demo"}),
                                  label="Username")

    class Meta:
        model = Course
        fields = ["title", "course_code", "lecturer"]


class CourseRegForm(forms.Form):
    """

    """
    mat_number = forms.CharField(max_length=30, required=True,
                                 widget=forms.TextInput(attrs={"placeholder": "MAT NUMBER", "class": "form-control"}),
                                 label="MAT NUMBER")


class GenerateLinkForm(forms.Form):
    """

    """
    start_time = forms.DateTimeField(required=True,
                                     widget=forms.DateTimeInput(attrs={'name': "start_time", "class": "form-control",
                                                                       'type': 'datetime-local'}),
                                     label="START TIME")

    end_time = forms.DateTimeField(required=True,
                                   widget=forms.DateTimeInput(
                                       attrs={'name': "end_time", "class": "form-control", 'type': 'datetime-local'}),
                                   label="END TIME")


class OTPForm(forms.Form):
    """

    """
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(
        attrs={'name': "password", "class": "form-control", "placeholder": "OTP"}), label="Password")

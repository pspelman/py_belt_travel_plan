from django import forms
from django.contrib.auth import (
    authenticate,
    get_user_model,
)

from models import *

User = get_user_model()


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('alias', 'birth_date')
        widgets = {
            'birth_date': forms.SelectDateWidget(years=range(2018, 1970, -1))
        }

    def clean_birth_date(self, *args, **kwargs):
        birth_date = self.cleaned_data.get('birth_date')
        if not birth_date:
            raise forms.ValidationError("You must enter your birthday")
        return birth_date


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Email address')
    email_confirm = forms.EmailField(label='Confirm Email')
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name',
                  'last_name',
                  'email',
                  'email_confirm',
                  'password',
                  'password_confirm',
                  ]

    # # if the order of my fields caused processing errors, could override clean method like this
    # # this will make the error messages come up ON TOP of the form
    # def clean(self, *args, **kwargs):
    #     email_confirm = self.cleaned_data.get('email_confirm')
    #     email = self.cleaned_data.get('email')
    #     # print "cleaned data {}, {}".format(email_confirm, email)
    #     if email != email_confirm:
    #         raise forms.ValidationError("Emails must match")
    #     ## if NOT using custom user model, then use this check to make sure email is unique
    #     # email_qs = User.objects.filter(email=email)
    #     # if email_qs.exists():
    #     #     raise forms.ValidationError("That email is already in use")
    #     return super(UserRegisterForm, self).clean(*args, **kwargs)

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(password) < 8:
    #         raise forms.ValidationError("Password must be at least 8 characters in length")
    #     return password

    def clean_password_confirm(self, *args, **kwargs):
        password_confirm = self.cleaned_data.get('password_confirm')
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters in length")
            # return password
        elif password_confirm != password:
            raise forms.ValidationError("Passwords must match")

        return password

    def clean_email_confirm(self):
        email_confirm = self.cleaned_data.get('email_confirm')
        email = self.cleaned_data.get('email')
        # print "cleaned data {}, {}".format(email_confirm, email)
        if email != email_confirm:
            raise forms.ValidationError("Emails must match")

        ## if NOT using custom user model, then use this check to make sure email is unique
        # email_qs = User.objects.filter(email=email)
        # if email_qs.exists():
        #     raise forms.ValidationError("That email is already in use")

        return email


class UserLoginForm(forms.Form):
    # class Meta:
    #     model = get_user_model()
    #     fields = ('first_name','last_name','email','password')
    #     exclude = ()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        # User authentication with Django admin's authenticate() method

        # could write different authentication method, start by checking if user exists
        # user_qs = User.objects.filter(email=email)
        # if user_qs.count() == 1:
        #     user = user_qs.first()

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError("invalid email and password combination")
            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)

from django import forms
from main.models import *
from django.forms import extras

# This form is used in /registration/forms.py
# This is just a reference
class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.widget.TextInput,label="Email")
    password1 = forms.CharField(widget=forms.widget.PasswordInput,
                                label="Password")
    password2 = forms.CharField(widget=forms.widget.PasswordInput,
                                label="Password (again)")

    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError("Passwords don't match. Please enter both fields again.")

        if 'email' in self.cleaned_data:
            domain = self.cleaned_data['email'].split('@')[1]
            found = False
            for uni in University.objects.all():
                if uni.domain in domain:
                    self.cleaned_data['university'] = uni
                    found = True
                    break
            if found == False:
                raise forms.ValidationError("Please use your university email.")
        return self.cleaned_data

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
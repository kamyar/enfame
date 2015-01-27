from django import forms
from .models import Post, UrlEntry
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)


class UrlForm(forms.ModelForm):

    class Meta:
        model = UrlEntry
        fields = ('title', 'address', 'extension')

class UpdateProfile(forms.ModelForm):
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(id=self.instance.id).count():
            raise forms.ValidationError('This email address is already in use. Please supply a different email address.')
        return email

    # def save(self, commit=True):
    #     user = super(RegistrationForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']

    #     if commit:
    #         user.save()

    #     return user
from django import forms
from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):

    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1' ,'password2' )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:   
            return email
        raise forms.ValidationError('This email address is already in use.')
    
class UpdateProfile(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)

    def __init__(self, *args, **kw):
        super(UpdateProfile, self).__init__(*args, **kw)
        self.fields['first_name'].initial = self.instance.first_name
        self.fields['last_name'].initial = self.instance.last_name

        # self.fields.keyOrder = [
        #     'first_name',
        #     'last_name',
        #     ]
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name')





from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from registro.models import *
#from flatpickr import DateTimePickerInput

class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Nome"

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Nome"
        self.fields['description'].label = "Descrizione"

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'code', 'company']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = "Nome"
        self.fields['description'].label = "Descrizione"
        self.fields['code'].label = "Codice"
        self.fields['company'].label = "Cliente"

class WorkedHoursForm(forms.ModelForm):
    class Meta:
        model = WorkedHours
        fields = ['from_time', 'to_time', 'description', 'category', 'project']
        localized_fields = ('from_time', 'to_time')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['from_time'].input_formats = ['%d/%m/%Y %H:%M']
        self.fields['from_time'].label = "Dalle"
        self.fields['to_time'].input_formats = ['%d/%m/%Y %H:%M']
        self.fields['to_time'].label = "Alle"
        self.fields['description'].label = "Descrizione"
        self.fields['category'].label = "Categoria"
        self.fields['project'].label = "Progetto"

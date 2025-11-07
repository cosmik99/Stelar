# store/forms.py

from django import forms
from store.models import Customer # Importa el modelo Customer de tu models.py

class SignupForm(forms.ModelForm):
    # Usamos CharField con PasswordInput para asegurar que la contraseña se oculte
    password = forms.CharField(widget=forms.PasswordInput)
    
    class Meta:
        model = Customer
        # Especifica los campos que quieres que aparezcan en el formulario
        fields = ['first_name', 'last_name', 'phone', 'email', 'password']

class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Correo electrónico'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
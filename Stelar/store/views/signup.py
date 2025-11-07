from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models import Customer
from django.views import View
from store.forms import SignupForm

class Signup(View):
    def get(self, request):
        print("✅ GET ejecutado")
        form = SignupForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        print("🚀 POST ejecutado")
        form = SignupForm(request.POST)

        if form.is_valid():
            print("✅ Formulario válido")
            customer = form.save(commit=False)
            customer.password = make_password(customer.password)
            customer.save()
            print("💾 Usuario guardado:", customer.email)

            
            request.session['customer_id'] = customer.id
            request.session['customer_email'] = customer.email
            print("🔐 Sesión iniciada para:", customer.email)

            
            return redirect('index')
        else:
            print("❌ Errores:", form.errors)
            return render(request, 'signup.html', {'form': form})

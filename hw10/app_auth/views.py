from django.shortcuts import render
from django.views import View

# Create your views here.

class RegisterView(View):
    template_name = 'register.html'
    def get(self, request):
        pass
    def post(self, request):
        pass
def login(request):
    return render(request, template_name='app_auth/login.html')

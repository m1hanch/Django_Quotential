import smtplib
from email.mime.text import MIMEText

from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages

from .forms import RegisterForm, ResetPasswordForm
from .utils import send_email_via_smtp



class RegisterView(View):
    template_name = 'app_auth/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:index")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            messages.success(request, f"Вітаємо {username}. Ваш акаунт успішно створено")
            return redirect(to="app_auth:signin")
        return render(request, self.template_name, {"form": form})


def login(request):
    return render(request, template_name='app_auth/login.html')


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'app_auth/password_reset.html'
    success_url = reverse_lazy('app_auth:password_reset_done')
    email_template_name = 'app_auth/password_reset_email.html'
    html_email_template_name = 'app_auth/password_reset_email.html'
    success_message = "An email with instructions to reset your password has been sent to %(email)s."
    subject_template_name = 'app_auth/password_reset_subject.txt'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        subject = "Your Password Reset Link"
        body = "This is where you put the password reset message and link."
        if send_email_via_smtp(email, subject, body):
            return super().form_valid(form)
        else:
            form.add_error(None, 'Error sending email')
            return self.form_invalid(form)

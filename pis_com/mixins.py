from django.contrib.auth.mixins import LoginRequiredMixin


class AuthRequiredMixin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = None

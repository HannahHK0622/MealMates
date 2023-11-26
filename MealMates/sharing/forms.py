from django.contrib.auth.forms import UserCreationForm as UCrF
from django.contrib.auth.forms import UserChangeForm as UChF

from .models import Profile

class CustomUserCreationForm(UCrF):
    class Meta:
        model = Profile
        fields = ('email', )

class CustomUserChangeForm(UChF):
    class Meta:
        model = Profile
        fields = ('email',)
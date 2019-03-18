from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from .forms import SignUpForm
from .models import User


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})


@ method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    template_name = 'my_account.html'
    fields = ['first_name', 'last_name', 'email']
    success_url = reverse_lazy('my_account')

    def get_object(self, queryset=None):
        return self.request.user

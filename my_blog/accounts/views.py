from django.shortcuts import render
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserForm


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('post_list')
    else:
        form = UserForm()
    return render(request, 'accounts/register.html', {'form': form})
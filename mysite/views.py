from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from action.forms import UserForm


def signup(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_passwd = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_passwd)
            login(request, user)
            return redirect("action:index")
    else:
        form = UserForm()
    return render(request, 'registration/signup.html', {'form': form})

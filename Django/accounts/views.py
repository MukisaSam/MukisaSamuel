from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Saves secure user to database
            return redirect('register')  # Refreshes page on success
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

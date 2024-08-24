from django.shortcuts import render
from .forms import TextInputForm

def index(request):
    result = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            result = process_input(user_input)
    else:
        form = TextInputForm()

    return render(request, 'index.html', {'form': form, 'result': result})

def process_input(user_input):
    return user_input.upper()

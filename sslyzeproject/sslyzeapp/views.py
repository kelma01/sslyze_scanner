from django.shortcuts import render
from .forms import TextInputForm
from .sslyze_scanner import sslyze_scan
import json

def index(request):
    result = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            json_result = sslyze_scan(user_input)
            result = json.loads(json_result)
    else:
        form = TextInputForm()

    return render(request, 'index.html', {'form': form, 'result': result})

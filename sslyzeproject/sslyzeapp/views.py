from django.shortcuts import render
from .forms import TextInputForm
from .sslyze_scanner import sslyze_scan
import json
import datetime

def index(request):
    result = None
    payload = None
    if request.method == 'POST':
        form = TextInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            json_result = sslyze_scan(user_input)
            result = json.loads(json_result)
            not_valid_after_unparsed = result.get("server_scan_results")[0].get("scan_result").get("certificate_info").get("result").get("certificate_deployments")[0].get("received_certificate_chain")[0].get("not_valid_after")
            not_valid_after = str(not_valid_after_unparsed).replace("T", " ").replace("Z", "").replace("-","/")
            validity_status = 'True' if str(datetime.datetime.utcnow()) < not_valid_after_unparsed else 'False'

            payload = {
                "Validity Status": validity_status,
                "Hostname": result.get("server_scan_results")[0].get("server_location").get("hostname"),
                "Port": result.get("server_scan_results")[0].get("server_location").get("port"),
                "IP Address": result.get("server_scan_results")[0].get("server_location").get("ip_address"),
                "Not Valid After": not_valid_after,
                "SAN": result.get("server_scan_results")[0].get("scan_result").get("certificate_info").get("result").get("certificate_deployments")[0].get("received_certificate_chain")[0].get("subject_alternative_name").get("dns_names")
            }
    else:
        form = TextInputForm()

    return render(request, 'index.html', {'form': form, 'result': payload})

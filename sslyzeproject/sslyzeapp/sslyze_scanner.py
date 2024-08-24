import datetime
from pathlib import Path
from typing import List
import json

from sslyze import *


def sslyze_scan(domain):
    json_output_as_str = start_scan(domain)
    return json.dumps(json_output_as_str)

def start_scan(domain) -> str:
    date_scans_started = datetime.datetime.utcnow()
    try:
        scan_reqs = [ServerScanRequest(server_location=ServerNetworkLocation(hostname=domain))]
    except ServerHostnameCouldNotBeResolved:
        return ""

    scanner = Scanner()
    scanner.queue_scans(scan_reqs)

    all_server_scan_results = []
    for server_scan_result in scanner.get_results():
        all_server_scan_results.append(server_scan_result)
        if server_scan_result.scan_status == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
            exit(0)

    json_file_out = Path(f"{domain}.json")
    return json_result_output(json_file_out, all_server_scan_results, date_scans_started, datetime.datetime.utcnow())

def json_result_output(
        json_file_out: Path,
        all_server_scan_results: List[ServerScanResult],
        date_scans_started: datetime,
        date_scans_completed: datetime
):
    json_output = SslyzeOutputAsJson(
        server_scan_results=[ServerScanResultAsJson.model_validate(result) for result in all_server_scan_results],
        invalid_server_strings=[],
        date_scans_started=date_scans_started,
        date_scans_completed=date_scans_completed,
    )
    json_output_as_str = json_output.model_dump_json()
    json_file_out.write_text(json_output_as_str)
    return json_output_as_str

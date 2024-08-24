import sslyze
from sslyze import *

start_time = 0

class SslyzeScanner:
    def init(self):
        pass

    def start_scan(self, domain):
        scanner = Scanner()
        request = ServerScanRequest(server_location=ServerNetworkLocation(hostname=domain))
        scanner.queue_scans([request])
        for result in scanner.get_results():
            self.result_as_json(result)

    def result_as_json(self, result):
        if result.scan_status == ServerScanStatusEnum.ERROR_NO_CONNECTIVITY:
            return {
                "ERROR": result.scan_status
            }
        json_output = SslyzeOutputAsJson(
            server_scan_results=result,
            date_scans_started=None,
            date_scans_completed=None,
        )
        json_output_as_str = json_output.model_dump_json()
        pass
        # json_file_out.write_text(json_output_as_str)

def main():
    # domain = input("Enter domain to start scan...")
    domain = 'google.com'
    ssl_scanner = SslyzeScanner()
    ssl_scanner.start_scan(domain)

if __name__ == '__main__':
    main()

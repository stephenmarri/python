import csv
import ctypes
import datetime
import os.path
from pathlib import Path

import requests

counter_success = 0


def open_chart(in_path, out_folder):
    global report
    with open(in_path) as file_txt:
        counter_pdf = 1
        total_pdfs = get_lines_count(in_path)
        for line_pdf in file_txt:
            report = []
            print(f"Downloading pdf: [{counter_pdf}/{total_pdfs}], folder: [{os.path.basename(folder)}]")
            out_path = os.path.join(out_folder, f"Chart_{counter_pdf}.pdf")
            pdf_name = line_pdf.replace("\n", "")
            download_chart(base_url + pdf_name, out_path)
            counter_pdf += 1

            report.append(os.path.basename(folder))
            report.append(folder)
            report.append(pdf_name)
            report.append("Success")
            report.append(out_path)

            write_result(report)


def write_result(lst):
    with open(output_report_path, 'a', newline='', encoding='utf-8') as file_namee:
        writer = csv.writer(file_namee, dialect='excel')
        writer.writerow(lst)


def download_chart(api_url, out_path):
    global counter_success
    cookies = {'PHPSESSID': 'pe06bhpqd98m22q8ficgg5cc8s', }
    headers = {}
    response = requests.get(api_url, cookies=cookies, headers=headers, )
    with open(out_path, 'wb') as file_download:
        file_download.write(response.content)
    counter_success += 1


def get_lines_count(in_path) -> int:
    lines_in_file = open(in_path, 'r').readlines()
    number_of_lines = len(lines_in_file)
    return number_of_lines


if __name__ == "__main__":
    print("Process Started")
    counter_file = 1
    input_report = ''

    output_file_name = r"DownloadCharts_" + datetime.datetime.now().strftime("%H%M%S") + ".csv"
    output_report_path = 'D:/steve/random stuff/Terrebone/FHR/charts/' + output_file_name
    if not os.path.exists(output_report_path):
        f = open(output_report_path, "w")  # 'r' for reading and 'w' for writing
        f.close()

    input_path = 'D:/steve/random stuff/Terrebone/FHR/charts/charts_134710.txt'
    base_url = 'https://ats.medtronsoftware.com/uploadedfile/ats/scanneddocs/'

    with open(input_path) as file:
        total_files = get_lines_count(input_path)
        for line in file:
            report = []
            print(f"Processing file: [{counter_file}/{total_files}]. Success: [{counter_success}]")
            folder = line.split(",")[0]
            file_name = line.split(",")[1]
            curr_path = os.path.join(folder, file_name)
            curr_path = curr_path.replace("\\", "/").replace("\n", "")

            if os.path.exists(curr_path):
                output_folder = os.path.dirname(curr_path) + "/ScannedCharts"
                if not os.path.exists(output_folder):
                    Path(output_folder).mkdir(parents=True, exist_ok=True)
                open_chart(curr_path, output_folder)
            counter_file += 1

    ctypes.windll.user32.MessageBoxW(0, "Process Completed", "Information", 1)

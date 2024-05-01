import csv
import ctypes
import datetime
import os.path
import time
from pathlib import Path
import requests
from config_charts import *


def download_pdf(pat_name, ref_name, ind):
    pat_output_dir = dir_charts_output + "/" + pat_name
    create_dir(pat_output_dir)
    out_ref_name = f"Chart_{ind}_" + process_file_name(ref_name)
    out_path = pat_output_dir + '/' + out_ref_name
    final_url = base_url + ref_name
    curl(final_url, out_path)

    row = [pat_name, pat_output_dir, ref_name, out_ref_name, out_path]
    write_result(row)


def curl(api_url, out_path):
    global counter_success, counter_failed
    try:
        cookies = {'PHPSESSID': f'{cnf_token}', }
        headers = {}
        response = requests.get(api_url, cookies=cookies, headers=headers, )
        with open(out_path, 'wb') as file_download:
            file_download.write(response.content)
        counter_success += 1
    except Exception as e:
        print("Failed to download: " + out_path)
        print(str(e))
        counter_failed += 1


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        Path(dir_name).mkdir(parents=True, exist_ok=True)


def get_lines_count(in_path) -> int:
    lines_in_file = open(in_path, 'r').readlines()
    number_of_lines = len(lines_in_file)
    return number_of_lines


def write_result(lst):
    with open(output_report_path, 'a', newline='', encoding='utf-8') as file_namee:
        writer = csv.writer(file_namee, dialect='excel')
        writer.writerow(lst)


def process_patient_name(patient_str) -> str:
    patient_str = str(patient_str).split("__")[0]
    return patient_str


def process_file_name(file_str) -> str:
    file_str = str(file_str)
    if len(file_str) > 50 and file_str.endswith('.pdf'):
        file_str = file_str[-59:]
    elif len(file_str) > 25 and file_str.endswith('.pdf'):
        file_str = file_str[-59:]
    else:
        file_str = ''
    return file_str


if __name__ == "__main__":
    print("Process Started")
    counter_success = 0
    counter_failed= 0
    start_time = time.time()
    start_from_line = 1022

    input_path = f'{cnf_root_dir}/charts/{cnf_curl_csv}'
    root_dir = f'{cnf_root_dir}/charts/'
    create_dir(root_dir)

    base_url = 'https://ats.medtronsoftware.com/uploadedfile/ats/scanneddocs/'
    root_time = str(datetime.datetime.now().strftime("%H%M%S"))
    output_file_name = r"DownloadedCharts_" + root_time + ".csv"
    output_report_path = root_dir + output_file_name
    dir_charts_output = root_dir + 'charts_output_' + root_time
    create_dir(dir_charts_output)

    with open(input_path) as file:
        counter_total_refs = get_lines_count(input_path)
        reader = csv.reader(file, delimiter=",")
        for i, line in enumerate(reader):
            if i >= start_from_line:
                patient_name = process_patient_name(line[0])
                pdf_name = line[1]
                print(f"Processing Ref: [{i+1}/{counter_total_refs}] Pass|Fail: [{counter_success}|{counter_failed}]  Patient: [{patient_name}] Time:[{time.strftime('%H:%M:%S')}] Elapsed Time: [{str(datetime.timedelta(seconds=(time.time() - start_time)))}]")
                download_pdf(patient_name, pdf_name, i+1)

    ctypes.windll.user32.MessageBoxW(0, "Process Completed", "Information", 1)

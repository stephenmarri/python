import csv
import ctypes
import datetime
import os.path
from pathlib import Path
from config_charts import *


def grab_refs_from_file(path_charts):
    global counter_refs
    with open(path_charts) as charts_file:
        total_refs = get_lines_count(path_charts)
        folder_name = os.path.basename(path_charts)
        for ref in charts_file:
            counter_refs += 1
            row = [folder_name, ref.replace("\n", "")]
            write_result(row)


def write_result(lst):
    with open(output_report_path, 'a', newline='', encoding='utf-8') as file_namee:
        writer = csv.writer(file_namee, dialect='excel')
        writer.writerow(lst)


def get_lines_count(in_path) -> int:
    lines_in_file = open(in_path, 'r').readlines()
    number_of_lines = len(lines_in_file)
    return number_of_lines


def make_good_path(input_str) -> str:
    folder = input_str.split(",")[0]
    file_name = input_str.split(",")[1]
    curr_path = os.path.join(folder, file_name)
    curr_path = curr_path.replace("\\", "/").replace("\n", "")
    return curr_path


if __name__ == "__main__":
    print("Process Started")
    counter_txt_files = 1
    counter_refs = 0

    input_file = f'{cnf_root_dir}/charts/{cnf_collate_txt}'
    output_file_name = r"CollatedCharts_" + datetime.datetime.now().strftime("%H%M%S") + ".csv"
    output_report_path = f'{cnf_root_dir}/charts/' + output_file_name

    with open(input_file) as file:
        total_txt_files = get_lines_count(input_file)
        for line in file:
            print(f"Processing txt file: [{counter_txt_files}/{total_txt_files}]")
            path_patient_chart = make_good_path(line)
            grab_refs_from_file(path_patient_chart)
            counter_txt_files += 1

    print(f"Total Refs Found: [{counter_refs}]")
    ctypes.windll.user32.MessageBoxW(0, "Process Completed", "Information", 1)
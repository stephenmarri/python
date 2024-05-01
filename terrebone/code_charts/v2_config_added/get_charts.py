import datetime
import os.path
import ctypes
from config_charts import *


def write(str_input):
    file_mod = open(output_path, "a")
    file_mod.write(str_input + "\n")
    file_mod.close()


if __name__ == "__main__":
    print("Process Started")
    output_file_name = r"charts_" + datetime.datetime.now().strftime("%H%M%S") + ".txt"
    output_path = cnf_root_dir + 'charts/' + output_file_name
    root_folder = cnf_root_dir + 'download_completed'

    if not os.path.exists(output_path):
        f = open(output_path, "w")  # 'r' for reading and 'w' for writing
        f.close()

    counter = 1
    success = 0
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            print(f"Scanning file: [{counter}]. Found files: [{success}]")
            if str(file).endswith("ScannedCharts.txt"):
                if os.path.getsize(os.path.join(root, file)) > 0:
                    write(f"{root},{file}")
                    success += 1

    ctypes.windll.user32.MessageBoxW(0, "Process Completed", "Information", 1)

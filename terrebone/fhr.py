import os
import shutil
import time
import re
import datetime

import pandas as pd
import json
import cls
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path

# global values
timeout_patient_reload = 30  # seconds
current_patient_name = ""
count_intermediate = 5
dir_output = 'D:/steve/random stuff/Terrebone/FHR/output/'
dir_download = 'D:/steve/random stuff/Terrebone/FHR/download'
dir_intermediate = 'D:/steve/random stuff/Terrebone/FHR/intermediate'
file_input = 'D:/steve/random stuff/Terrebone/FHR/Output_155448.xlsx'


def load_driver():
    chrome_options = webdriver.ChromeOptions()
    settings = {"recentDestinations": [{"id": "Save as PDF", "origin": "local", "account": ""}],
                "selectedDestinationId": "Save as PDF", "version": 2}
    prefs = {
        "download.default_directory": dir_download,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True,
        'printing.print_preview_sticky_settings.appState': json.dumps(settings),
        'savefile.default_directory': dir_download
    }
    chrome_options.add_experimental_option('prefs', prefs)

    chrome_options.add_argument('--kiosk-printing')
    inner_driver = webdriver.Chrome(options=chrome_options)
    return inner_driver


def login_to_site(url, user, pwdd):
    driver.get(url)
    assert "Medtron" in driver.title
    el_usr = driver.find_element(By.NAME, "txtUserName")
    el_usr.clear()
    el_usr.send_keys(user)
    el_pwd = driver.find_element(By.NAME, "txtPassword")
    el_pwd.clear()
    el_pwd.send_keys(pwdd)
    el_lgn = driver.find_element(By.NAME, "btnSubmit")
    el_lgn.click()

    if "Dashboard" in driver.page_source:
        print("Logged In Successfully")
    else:
        cls.msg("Failed To Login", "E")


def browse_to_facesheet(demo_id, prev_name="") -> bool:
    global current_patient_name
    driver.execute_script(f"fncPatientRedirect('D','{demo_id}','0',0)")
    if prev_name == "":
        wait_till_load(by_id="rwFacesheetRow")
    else:
        has_name_reloaded(prev_name)

    el_name = driver.find_element(By.ID, "linkDemo")
    current_patient_name = el_name.text
    # patient details
    df.loc[index, "Patient_Name"] = str(current_patient_name)
    try:
        df.loc[index, "DOB"] = str(driver.find_element(By.ID, "demoPanel_dob").text)
    except:
        print("Some additional details could not be fetched")

    result_demo_id = el_name.get_attribute("demoid")
    if result_demo_id is not None and int(result_demo_id) == demo_id:
        print("Facesheet Loaded")
        return True
    else:
        cls.msg("Error Loading facesheet", "E")
        return False


def has_name_reloaded(prev_name_1) -> bool:
    global current_patient_name
    for i in range(1, timeout_patient_reload):
        curr_name = driver.find_element(By.ID, "linkDemo").text
        if curr_name == prev_name_1:
            print("Waitig for facesheet to load")
            time.sleep(1)
        else:
            print(f"New Facesheet loaded: {curr_name}")
            return True
    return False


def load_print_form():
    driver.execute_script("window.open('about:blank','secondtab');")
    driver.switch_to.window("secondtab")
    driver.get("https://ats.medtronsoftware.com/facesheet/printall?iCompleteFlag=1&")
    # driver.execute_script("fncPrintAll()")

    select_template = Select(driver.find_element(By.NAME, "letter_template_id"))
    select_template.select_by_visible_text("FORMAL HEALTH RECORD")
    lst_check = ["chkEncounter", "chkMedication", "chkMedHistory", "chkSurgHistory", "chkFamilyHistory",
                 "chkSocialHistory", "printAllergies", "chkProgressNotes", "chkFinancialNotes", "chkTelephoneNotes"]
    for chk_id in lst_check:
        chk_encounter = driver.find_element(By.ID, chk_id)
        chk_encounter.click()

    elem_go = driver.find_element(By.ID, "Print")
    elem_go.click()



def wait_till_load(by_id="", type="", timeout=300) -> bool:
    print(f"waiting started id: {by_id}")
    try:
        if by_id is not None:
            WebDriverWait(driver, timeout).until(EC.visibility_of_element_located((By.ID, by_id)))
        print("Element Found")
        return True
    except:
        print("Element not found")
        return False


def save_as_pdf():
    elem_print = driver.find_element(By.ID, "btnReferralPrint")
    elem_print.click()
    time.sleep(2)
    driver.execute_script('window.print();')
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    print("File downloaded successfully")


def move_file(dir_name):
    allfiles = os.listdir(dir_download)
    dir_target = os.path.join(dir_output ,dir_name)
    if len(allfiles) > 0:
        if not os.path.exists(dir_target):
            Path(dir_target).mkdir(parents=True, exist_ok=True)
        counter = 1
        for file_name in allfiles:
            if file_name.endswith(".pdf"):
                shutil.move(os.path.join(dir_download, file_name), os.path.join(dir_target,dir_name + datetime.datetime.now().strftime("%H%M%S") + ".pdf"))
            counter += 1
        df.loc[index, "Download_Path"] = dir_target
        print("All files moved successfully")
    else:
        print("No files found in download directory")

def make_name(input : str) -> str:
    output = re.findall('\w+', input)
    return " ".join(output)


def save_page_source(dir_name):
    dir_target = os.path.join(dir_output, dir_name)
    file_path = os.path.join(dir_target , "WebPage.html")
    with open(file_path, "w", encoding='utf-8') as f:
        f.write(driver.page_source)
    print("Page source written")

def write_intermediate(curr_index):
    if curr_index % count_intermediate == 0:
        if not os.path.exists(dir_intermediate):
            Path(dir_intermediate).mkdir(parents=True, exist_ok=True)
        inter_file_name = r"Intermediate__" + datetime.datetime.now().strftime("%H%M%S") + ".xlsx"
        df.to_excel(os.path.join(dir_intermediate, inter_file_name))

if __name__ == "__main__":
    print("Process Started")
    driver = load_driver()
    url = 'https://ats.medtronsoftware.com/login/login'
    usr, pwd = 'mccoym', 'mm1234'

    login_to_site(url, usr, pwd)

    df = pd.read_excel(file_input)
    for index, row in df.iterrows():
        if row["Status"] != "Completed" and row["Status"] != "Failed":
            d_id = int(row["Demo_Id"])
            print(f"Processing demo id: {d_id}. Total: [{index}/{df.shape[0]}]")
            df.loc[index, "StartedAt"] = str(datetime.datetime.now().strftime("%H%M%S"))
            browse_to_facesheet(d_id, current_patient_name)

            load_print_form()

            if wait_till_load(by_id="btnReferralPrint", timeout=300):
                print("print form loaded")
                save_as_pdf()
                modified_name = make_name(str(d_id) + "_" + current_patient_name)
                move_file(modified_name)
                save_page_source(modified_name)
                df.loc[index, "Status"] = "Completed"
                df.loc[index, "CompletedAt"] = str(datetime.datetime.now().strftime("%H%M%S"))
        write_intermediate(int(index))

    driver.quit()

    #final output
    output_file_name = r"Output_" + datetime.datetime.now().strftime("%H%M%S") + ".xlsx"
    df.to_excel(output_file_name)
    print("Process Completed")

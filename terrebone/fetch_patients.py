import requests


def main(out_folder, start, end):
    headers = {'Cookie': 'PHPSESSID=6bsp8qh5t0from32ssp6d1bfod'}
    url = r"https://ats.medtronsoftware.com/schedule/patientinfosheet?demo_Id="

    for i in range(start, end):
        print(f'Processing patient: [{i}]')
        out_path = out_folder + str(i) + '.html'
        new_url = url + str(i)
        response = requests.get(new_url, headers=headers)

        with open(out_path, "wb") as f:
            f.write((response.content))


if __name__ == "__main__":
    print("Process Started")
    out_folder = 'D:/steve/random stuff/Terrebone/patient-info-sheets/info-sheets/'
    main(out_folder, 1, 2)
    print("Process Completed")

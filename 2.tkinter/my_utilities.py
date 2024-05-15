import os.path
import tkinter as tk
import tkinter.ttk as ttk
import json


class MyUtilties:
    def __init__(self):
        print("Program Started")
        self.root = tk.Tk()
        self.root.title("steve's Utilities")
        self.root.configure(background="whitesmoke")
        # self.root.geometry("600x600")
        self.style = ttk.Style()
        self.style.configure("color1.TFrame", foreground="black", background="whitesmoke")

        self.main_frame = tk.Frame(self.root, width=300, background="whitesmoke")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        row = 0
        for item in details:
            self.createButton(item["value"], item["button_text"], row)
            row += 1

        # open details file
        icon_open = tk.PhotoImage(file = path_open_file_icon)
        icon_open = icon_open.subsample(18)
        self.btn_open = tk.Button(self.main_frame,  text="Open", image=icon_open, command=self.open_file, font=('Helvetica', 12))
        self.btn_open.grid(column=4, row=10, pady=5, padx=5, sticky=tk.W + tk.E)

        # Spacer Column for viewing
        spacer1 = tk.Label(self.main_frame, text="", width=3)
        spacer1.grid(row=10, column=1)

        self.main_frame.pack(fill='both', expand=True, pady=50, padx=50)
        self.root.mainloop()

    def copy_value(self, val):
        print(val)
        self.root.clipboard_clear()
        self.root.clipboard_append(val)
        self.root.update()

    def open_file(self):
        print("Open File")
        os.startfile(r"D:\steve\my study\learning\python\py_projects\2.tkinter\details.txt")

    def createButton(self, value, button_text, index):
        lbl_details = tk.Label(self.main_frame, pady=2, padx=2, borderwidth=2, relief="ridge", background="white", width=30,text=value, font=('Helvetica',  12))
        lbl_details.grid(column=0,  row=index, sticky=tk.W )

        btn_details = tk.Button(self.main_frame,  width=15, text=button_text, command=lambda: self.copy_value(value), font=('Helvetica', 12))
        btn_details.grid(column=2, row=index, pady=5, padx=5, sticky= tk.E)


if __name__ == "__main__":
    with open(os.path.abspath(r"D:\steve\my study\github\python\2.tkinter\details.txt"), 'r') as file:
        details = file.read()
    details = json.loads(details)
    path_open_file_icon = os.path.abspath(r"D:\steve\my study\github\python\2.tkinter\open.png")

    a = MyUtilties()

import tkinter as tk
import tkinter.ttk as ttk
import requests


def app():
    global lbl, lbl_author
    root = tk.Tk()
    root.title("Qutoes")
    root.configure(background="white")

    main_frame = tk.Frame(root, width=400, height=300, background="white")

    lbl = tk.Label(main_frame, wraplength=400, width=60, height=10, text="random text", font=("Courier New", 14, "normal"))
    lbl.grid(row=0,  ipadx=10,  sticky=tk.W + tk.E )
    lbl.configure(anchor="center")
    lbl_author = tk.Label(main_frame, width=60, background="wheat",text="Socrates", font=("Helvetica", 10, "italic"))
    lbl_author.grid(row=1, ipadx=10, ipady=5,  sticky=tk.W + tk.E )

    getText()

    btn = tk.Button(main_frame, text="Generate Quote", background="#A5C695", foreground="#000", command=getText)
    btn.grid(row=2, ipadx=20, ipady=10, pady=50)

    main_frame.pack(fill="both",  expand=True, pady=50, padx=50)
    root.mainloop()


def getText():
    global lbl
    quote = requests.get("http://api.quotable.io/random")
    quote = quote.json()
    lbl['text'] = quote["content"]
    lbl_author['text'] = "- " + quote["author"]


if __name__ == "__main__":
    print("Process Started")
    app()

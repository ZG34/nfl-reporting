import os
import tkinter as tk
from tkinter import ttk
import win32api
import win32print
from PIL import Image


class PrinterHandler:
    def __init__(self):
        printerdef = ""

        def locprinter():
            pt = tk.Toplevel()
            pt.geometry("250x250")
            pt.title("choose printer")
            var1 = tk.StringVar()
            LABEL = tk.Label(pt, text="select Printer").pack()
            PRCOMBO = ttk.Combobox(pt, width=35, textvariable=var1)
            print_list = []
            printers = list(win32print.EnumPrinters(2))
            for i in printers:
                print_list.append(i[2])
            print(print_list)
            # Put printers in combobox
            PRCOMBO["values"] = print_list
            PRCOMBO.pack()

            def select():
                global printerdef
                printerdef = PRCOMBO.get()
                pt.destroy()

            BUTTON = ttk.Button(pt, text="Done", command=select).pack()
            pt.mainloop()

        locprinter()


class PrintingAction:
    def __init__(self):
        print("printing")
        img_path = "print_prep"
        os.chdir(img_path)

        def convert_to_pdf():

            for filename in os.listdir(os.getcwd()):
                if filename.endswith(".png"):
                    img1 = Image.open(filename)
                    img2 = img1.convert("RGB")
                    img2.save(f"{filename}.pdf")

        convert_to_pdf()

        def send_to_printer():
            print(printerdef)

            win32print.SetDefaultPrinter(printerdef)

            for filename in os.listdir(os.getcwd()):
                if filename.endswith(".pdf"):
                    win32api.ShellExecute(0, "print", filename, None, ".", 0)

        send_to_printer()

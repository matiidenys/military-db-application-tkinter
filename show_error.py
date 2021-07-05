from tkinter import Tk, messagebox


def show_error(err):
    root = Tk()
    root.geometry("-700+300")
    root.withdraw()
    if messagebox.showerror("Помилка!", err):
        root.destroy()

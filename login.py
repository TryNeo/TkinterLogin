# !/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
import mysql.connector
from PIL import Image, ImageTk
from dominio.entidades import *
from menu.principal import *
from tkinter import ttk, messagebox, PhotoImage


class MainWindow(Usuario):
    def __init__(self, root):
        root.title('Login')
        root.iconbitmap('image/login.ico')
        root.geometry("300x500")
        root.resizable(0, 0)

        #########centered screen##############
        root.update_idletasks()
        width = root.winfo_width()
        frm_width = root.winfo_rootx() - root.winfo_x()
        win_width = width + 2 * frm_width
        height = root.winfo_height()
        titlebar_height = root.winfo_rooty() - root.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = root.winfo_screenwidth() // 2 - win_width // 2
        y = root.winfo_screenheight() // 2 - win_height // 2
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.deiconify()

        #######image user#######
        load = Image.open("image/user.png")
        render = ImageTk.PhotoImage(load)
        img = tk.Label(root, image=render)
        img.image = render
        img.place(x=100, y=50)

        self.username = tk.StringVar()
        label_user = tk.Label(root, text="Username", font=("Arial", 12)).place(x=35, y=210)
        entry_user = tk.Entry(root, width=40, textvariable=self.username).place(x=35, y=240)

        self.password = tk.StringVar()
        label_pass = tk.Label(root, text="Password", font=("Arial", 12)).place(x=35, y=270)
        entry_user = tk.Entry(root, width=40, textvariable=self.password, show="*").place(x=35, y=300)

        button_login = tk.Button(root, text="Login", font=("Arial", 12), command=self.login).place(x=35, y=350)
        button_register = tk.Button(root, text="Register", font=("Arial", 12), command=self.registry).place(x=210,
                                                                                                            y=350)

    #########Connection Mysql###########
    def connecting(self):
        try:
            self.mydb = mysql.connector.connect(host='localhost',
                                                user='root',
                                                passwd='root',
                                                db='login')
            self.mysqlcursor = self.mydb.cursor()
        except mysql.connector.errors.ProgrammingError as error:
            print("Review the Error -->", error)
        finally:
            print("connection successfully")

    def login(self):
        self.connecting()
        user_name = self.username.get()
        password = self.password.get()
        query = "SELECT * FROM usuarios WHERE username = %s and password = %s"
        get_data = (user_name, password)
        self.mysqlcursor.execute(query, get_data)
        validate = self.mysqlcursor.fetchall()
        if validate:
            messagebox.showinfo(title="Login Successful", message='Correct username and password')
            main.destroy()

            ####MENU PRINCIPAL####
            main_p = tk.Tk()
            window_p = MainWindowP(main_p)
            main_p.mainloop()

        else:
            messagebox.showerror(title="Incorrect Login", message='Incorrect user or password')

    def registry(self):
        self.registry_win = tk.Toplevel()
        self.registry_win.title('Registry')
        self.registry_win.iconbitmap('image/register.ico')
        self.registry_win.geometry("300x350")
        self.registry_win.resizable(0, 0)

        title_label = tk.Label(self.registry_win, text="Registry", font=("Arial", 20), fg="black").place(x=90,
                                                                                                         y=0)
        self.email = tk.StringVar()
        email_label = tk.Label(self.registry_win, text="Email:", font=("Arial", 12)).place(x=20, y=50)
        email_entry = tk.Entry(self.registry_win, width=30, textvariable=self.email).place(x=100, y=51)

        self.username = tk.StringVar()
        label_user = tk.Label(self.registry_win, text="Username:", font=("Arial", 12)).place(x=20, y=90)
        entry_user = tk.Entry(self.registry_win, width=30, textvariable=self.username).place(x=100, y=91)

        self.password = tk.StringVar()
        label_pass = tk.Label(self.registry_win, text="Password:", font=("Arial", 12)).place(x=20, y=130)
        entry_user = tk.Entry(self.registry_win, width=30, textvariable=self.password, show="*").place(x=100, y=131)

        button_new = tk.Button(self.registry_win, text="New", font=("Arial", 12), command=self.new).place(x=20, y=200)

        button_registry_sql = tk.Button(self.registry_win, text="Register", font=("Arial", 12),
                                        command=self.register_sql).place(x=210,
                                                                         y=200)

    def new(self):
        self.email.set("")
        self.username.set("")
        self.password.set("")

    def register_sql(self):
        self.connecting()
        email = self.email.get()
        user_name = self.username.get()
        password = self.password.get()
        query = "INSERT INTO usuarios (email,username,password) values (%s, %s, %s)"
        get_data = (email, user_name, password)
        if email == "" and user_name == "" and password == "":
            messagebox.showerror(title="Incomplete data", message="Fill in the data")
        else:
            self.mysqlcursor.execute(query, get_data)
            self.mydb.commit()
            messagebox.showinfo(title="Registration completed", message='Correct email, username and password')


if __name__ == '__main__':
    main = tk.Tk()
    window = MainWindow(main)
    main.mainloop()



from tkinter import *
from tkinter import messagebox
import pandas as pd
from os.path import exists
import random
import re
import PIL.Image
import PIL.ImageTk
import pyperclip
import json


# ---------------------------- CONSTANTS ------------------------------- #
BLACK = 'black'
WHITE = 'white'
RED = "#e7305b"
GREEN = "#9bdeac"
CHECK_MARK = '✓'

znaki = [chr(i) for i in range(33, 47)]
znaki.append([chr(i) for i in range(58, 64)])
litery_duze = [chr(i) for i in range(65, 90)]
litery_male = [chr(i) for i in range(97, 122)]

nr_letters_upper = 3
nr_letters_lower = 3
nr_symbols = 2
nr_numbers = 2
email = 'kszmydki@gmail.com'


# ---------------------------- GENERATE PASSWRD ------------------------------- #

def generate_passwd():

    password = []
    password.append([random.randint(0,10) for i in range(0,nr_numbers)])
    password.append([random.choice(znaki) for i in range(0,nr_symbols)])
    password.append([random.choice(litery_duze) for i in range(0,nr_letters_upper)])
    password.append([random.choice(litery_male) for i in range(0,nr_letters_lower)])

    password = [item for sublist in password for item in sublist] #unnesting listy
    random.shuffle(password) #przesortowanie listy
    password = ''.join(str(i) for i in password)

    entr_passwd.delete(0, END)
    entr_passwd.insert(0, password)
    pyperclip.copy(password)



# ---------------------------- ADDITIONAL FUNCS ------------------------------- #

def open_popup(window_text):
    top = Toplevel(window)
    top.geometry("500x200")
    Label(top, text=window_text, font=('Ariel')).place(x=50, y=80)



def validate_data(type):

    if type == 'website':
        # url = re.findall(r'[\w\.]+.+[\w\.]+.+[\w\.]' , entr_website.get())
        if re.search(r'[\w\.]+.+[\w\.]+.+[\w\.]', entr_website.get()):
            return True

    elif type == 'email':
        if re.search(r'[\w\.]+@+[\w\.]+.+[\w\.]', entr_email.get()):
            return True

    elif type == 'password':

        password = entr_passwd.get()
        passwd_nr_numbers = len([i for i in list(password) if i in [str(j) for j in range(0, 10)]])
        passwd_nr_symbols = len([i for i in list(password) if i in znaki])
        passwd_nr_letters_lower = len([i for i in list(password) if i in litery_male])
        passwd_nr_letters_upper = len([i for i in list(password) if i in litery_duze])

        if passwd_nr_numbers >= nr_numbers and passwd_nr_symbols >= nr_symbols \
                and passwd_nr_letters_lower >= nr_letters_lower and passwd_nr_letters_upper >= nr_letters_upper:
            return True
    else:
        return False



def check_password(*args):

    password = entr_passwd.get()
    passwd_nr_numbers = len([i for i in list(password) if i in [str(j) for j in range(0, 10)]])
    passwd_nr_symbols = len([i for i in list(password) if i in znaki])
    passwd_nr_letters_lower = len([i for i in list(password) if i in litery_male])
    passwd_nr_letters_upper = len([i for i in list(password) if i in litery_duze])

    if passwd_nr_numbers >= nr_numbers:
        lbl_check_passwd1.config(fg=GREEN)
        lbl_check_passwd1_chck.config(fg=GREEN)
    else:
        lbl_check_passwd1.config(fg=RED)
        lbl_check_passwd1_chck.config(fg=RED)
    if passwd_nr_symbols >= nr_symbols:
        lbl_check_passwd2.config(fg=GREEN)
        lbl_check_passwd2_chck.config(fg=GREEN)
    else:
        lbl_check_passwd2.config(fg=RED)
        lbl_check_passwd2_chck.config(fg=RED)
    if passwd_nr_letters_lower >= nr_letters_lower:
        lbl_check_passwd3.config(fg=GREEN)
        lbl_check_passwd3_chck.config(fg=GREEN)
    else:
        lbl_check_passwd3.config(fg=RED)
        lbl_check_passwd3_chck.config(fg=RED)
    if passwd_nr_letters_upper >= nr_letters_upper:
        lbl_check_passwd4.config(fg=GREEN)
        lbl_check_passwd4_chck.config(fg=GREEN)
    else:
        lbl_check_passwd4.config(fg=RED)
        lbl_check_passwd4_chck.config(fg=RED)


# ---------------------------- ADD PASSWRD ------------------------------- #

def add_passwd():

    if len(entr_website.get())==0 or len(entr_email.get())==0 or len(entr_passwd.get())==0:
        open_popup(window_text="Please provide all details.")

    else:

        if validate_data('website') == True and validate_data('email') == True and validate_data('password') == True:

            is_ok = messagebox.askokcancel(title='Saving...', message=f'Provided details:\n'
                                                                      f'Website: {entr_website.get()}\n'
                                                                      f'User: {entr_email.get()}\n'
                                                                      f'Password: {entr_passwd.get()}\n')

            if is_ok:

                new_data = {
                    entr_website.get(): {
                    'email': entr_email.get(),
                    'password': entr_passwd.get()
                    }
                }

                try:
                    with open('password_manager.json', 'r') as f:
                        # json.dump(new_data, f, indent=4)
                        # f.write(f'{entr_website.get()}|{entr_email.get()}|{entr_passwd.get()}\n')
                        data = json.load(f)

                except FileNotFoundError:
                    with open('password_manager.json', 'w') as f:
                        json.dump(new_data, f, indent=4)

                else:
                    data.update(new_data)

                    with open('password_manager.json', 'w') as f:
                        json.dump(data, f, indent=4)

                finally:
                    open_popup(window_text=f'Password {entr_passwd.get()} successfully saved!')
                    entr_passwd.delete(0, END)
                    entr_website.delete(0, END)

        else:
            open_popup(window_text="Please provide correct data.")



def password_search():

    website = entr_website.get()

    try:
        with open('password_manager.json', 'r') as f:
            data = json.load(f)

    except FileNotFoundError:
        open_popup(window_text="No file found.")

    else:
        if website in data:
            messagebox.showinfo(title=f'{website}', message= f"User: {data[website]['email']}\n"
                                                              f"Password: {data[website]['password']}\n")
        else:
            messagebox.showinfo(title=f'{website}', message=f'The key {website} does not exist.')



# ---------------------------- UI ------------------------------- #

window = Tk()
window.title('Password Manager')
window.config(padx=100, pady=50, bg='white')


var = StringVar()
var.trace_add('write', check_password)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=WHITE)
canvas.grid(column=1,row=0)

im = PIL.Image.open("logo.png")
photo = PIL.ImageTk.PhotoImage(im)
image = canvas.create_image(100, 100, image=photo)


lbl_website = Label(text='Website: ', fg=BLACK, bg=WHITE)
lbl_website.grid(column=0,row=1)
lbl_email = Label(text='Email/Username: ', fg=BLACK, bg=WHITE)
lbl_email.grid(column=0,row=2)
lbl_passwd = Label(text='Password: ', fg=BLACK, bg=WHITE)
lbl_passwd.grid(column=0,row=3)


lbl_check_passwd1 = Label(text=f'{nr_numbers} Numbers',fg=RED, bg=WHITE)
lbl_check_passwd1.grid(column=0,row=4)
lbl_check_passwd1_chck = Label(text=CHECK_MARK,fg=RED, bg=WHITE)
lbl_check_passwd1_chck.grid(column=1,row=4)

lbl_check_passwd2 = Label(text=f'{nr_symbols} Symbols',fg=RED, bg=WHITE)
lbl_check_passwd2.grid(column=0,row=5)
lbl_check_passwd2_chck = Label(text=CHECK_MARK,fg=RED, bg=WHITE)
lbl_check_passwd2_chck.grid(column=1,row=5)

lbl_check_passwd3 = Label(text=f'{nr_letters_lower} Lowercase letters',fg=RED, bg=WHITE)
lbl_check_passwd3.grid(column=0,row=6)
lbl_check_passwd3_chck = Label(text=CHECK_MARK,fg=RED, bg=WHITE)
lbl_check_passwd3_chck.grid(column=1,row=6)

lbl_check_passwd4 = Label(text=f'{nr_letters_upper} Uppercase letters',fg=RED, bg=WHITE)
lbl_check_passwd4.grid(column=0,row=7)
lbl_check_passwd4_chck = Label(text=CHECK_MARK,fg=RED, bg=WHITE)
lbl_check_passwd4_chck.grid(column=1,row=7)


entr_website = Entry(width=50)
entr_website.grid(column=1,row=1)
entr_email = Entry(width=50)
entr_email.insert(0,email)
entr_email.grid(column=1,row=2)
entr_passwd = Entry(width=30, textvariable=var)
entr_passwd.grid(column=1,row=3)



bttn_generate = Button(text='Generate Password', command=generate_passwd)
bttn_generate.grid(column=2,row=3)
bttn_add = Button(text='Add', command=add_passwd)
bttn_add.grid(column=1,row=4)
bttn_search = Button(text='Search', command=password_search)
bttn_search.grid(column=2,row=1)

window.mainloop()
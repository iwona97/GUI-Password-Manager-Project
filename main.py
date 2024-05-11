from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json
import os

EMAIL = os.environ.get('EMAIL')


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = []

    password_list += [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)

    password = ''.join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get().title()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if not website or not email or not password:
        messagebox.showinfo(title="Oops", message="Please don't leave any field empty!")
        return

    try:
        with open("data.json", mode="r") as data_file:
            # Reading old data
            data = json.load(data_file)

    except FileNotFoundError:
        with open("data.json", mode="w") as data_file:
            json.dump(new_data, data_file, indent=4)

    else:
        # Updating old data with new data
        data.update(new_data)

        with open("data.json", mode="w") as data_file:
            # Saving updated data
            json.dump(data, data_file, indent=4)

    finally:
        messagebox.showinfo(title=website, message="Password successfully added to the database.")
        website_entry.delete(0, END)
        password_entry.delete(0, END)
        website_entry.focus()


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = website_entry.get().title()

    try:
        with open("data.json", mode="r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found.")

    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email:{email} \nPassword: {password}.")
            pyperclip.copy(password)
            website_entry.delete(0, END)
        else:
            messagebox.showinfo(title=website, message=f"No details for {website} exists.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.config(padx=50, pady=50)
window.title("Password Manager")

canvas = Canvas(width=200, height=200, highlightthickness=0)
logo_img = PhotoImage(file="images/logo.png")
logo = canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)

email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

password_label = Label(text="Password:")
password_label.grid(row=3, column=0)

# Entries
website_entry = Entry(width=33)
website_entry.grid(row=1, column=1, sticky="w")
website_entry.focus()

email_entry = Entry(width=52)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, EMAIL)

password_entry = Entry(width=33)
password_entry.grid(row=3, column=1, sticky="w")

# Buttons
search_button = Button(text="Search", width=14, command=search_password)
search_button.grid(row=1, column=2, sticky="w")

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(row=3, column=2, sticky="w")

add_button = Button(text="Add", width=44, command=save_password)
add_button.grid(row=4, column=1, columnspan=2, sticky="w")

window.mainloop()
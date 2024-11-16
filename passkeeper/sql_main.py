# Database Setup: The code now connects to an SQLite database (passwords.db) and creates a table (passwords) if it doesn't already exist.
# Save Function: Instead of saving data to a JSON file, it now inserts the data into the SQLite database.
# Search Function: The search function now queries the SQLite database to retrieve the stored password.

# Encryption: Instead of storing passwords in plain text within the data.json file, encrypt the passwords using a strong
# encryption algorithm such as AES (Advanced Encryption Standard). You can use libraries like cryptography in Python to
# implement this.

from tkinter import messagebox
from tkinter import *
import random
import pyperclip
import uuid
import time
import string
import sqlite3
import re


BLACK = "#040514"
TURQUOISE = "#0ce3c7"
DARK_CHARCOAL = "#333031"
FONT = ("consolas", 10, "normal")
ENTRY_PAD = 7


def exit_fullscreen(event=None):
    window.attributes("-fullscreen", False)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    password_entry.delete(first=0, last=END)  # as soon as the generate password button gets clicked, previous password
    # entry is deleted

    # Combine device-specific and time-based seeds
    device_seed = uuid.getnode()
    current_time_seed = time.time()

    combined_seed = device_seed + int(current_time_seed)
    random.seed(combined_seed)  # setting seeed as devices mac address and current system time in seconds to generate
    # unique passwords on different devices

    # these create lists(array) of letters, numbers and symbols
    letters = string.ascii_letters
    numbers = string.digits
    symbols = '!#$%&()*+'

    # selecting number of numbers, symbols and letters to be added in the password
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    # choosing random numbers, letters, symbols for the above selected no. of times and appending them to these lists
    # below using list comprehension

    # list comprehension is list to derive a new list from old list with some modifications in the elements from the old
    # list
    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

    # adding all lists to a single list
    password_list = password_letters + password_numbers + password_symbols
    random.shuffle(password_list)

    # converting list to a string
    password = "".join(password_list)

    pyperclip.copy(password)  # copies password in the field to the clipboard
    password_entry.insert(index=0, string=password)  # password generated gets inserted in the field from the starting of
    # entry


# ---------------------------- DATABASE SETUP ------------------------------- #

conn = sqlite3.connect('passwords.db')  # Creating a connection to the SQLite database using conn object
c = conn.cursor()  # c object used to perform queries in the database.

# Create a table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                website TEXT NOT NULL, 
                email TEXT NOT NULL, 
                password TEXT NOT NULL)''')


conn.commit()  # all changes are committed in database


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():

    # getting all entries from website, email and password into below variables
    website = website_entry.get()
    email = email_username_entry.get()
    password = password_entry.get()

    # if add button is clicked with leaving some fields empty then
    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
    else:

        # else we will display the message in popup box

        # is_ok takes value as true if ok is clicked in the pop up box
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n "
                                                              f"Email: {email}\n password: "
                                                              f"{password}\n Is it ok to save?")

        # if is_ok = True, that is user is satisfied with all the entries entered, then we insert them into database
        if is_ok:
            c.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
                      (website, email, password))
            conn.commit()

            # after adding all the fields are emptied
            website_entry.delete(first=0, last=END)
            password_entry.delete(first=0, last=END)
            email_username_entry.delete(first=0, last=END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #

def search_password():
    website = website_entry.get()  # taking website entry text in website variable

    # corresponding email and password is selected
    c.execute("SELECT email, password FROM passwords WHERE website = ?", (website,)) # corresponding
    # email and password is selected
    result = c.fetchone()  # entire row email and password is stored as tuple in the form (email, password)
    # in result variable

    # if result that is row exists
    if result:
        email, password = result  # tuple of (email, password) gets separated and stored in email and password variable
        # independently

        # email and password is displayed in the belowe pop up box
        messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
    else:

        # no website found pop up box is displayed
        messagebox.showinfo(title="Error", message=f"No password found for {website}.")

#-----------------------Default email--------------------------------#
# Database Setup
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Create tables if they don't exist
c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                website TEXT NOT NULL, 
                email TEXT NOT NULL, 
                password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS default_emails (
                email TEXT NOT NULL UNIQUE)''')
conn.commit()

# Validate email function
def validate_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

# Save default email
def save_default_email():
    email = email_username_entry.get()

    if not validate_email(email):
        messagebox.showerror("Invalid Email", "Please enter a valid email address.")
        return

    # Confirm popup
    is_ok = messagebox.askokcancel(title="Confirm Save", message=f"Do you want to save this email: {email}?")

    if is_ok:
        try:
            # Insert into default_emails table
            c.execute("INSERT INTO default_emails (email) VALUES (?)", (email,))
            conn.commit()
            messagebox.showinfo("Success", "Email saved successfully!")
        except sqlite3.IntegrityError:
            messagebox.showwarning("Duplicate Entry", "This email already exists in the database.")

    email_username_entry.delete(0, 'end')  # Clear the email entry after saving

# Display saved emails in the dropdown
def display_emails_in_dropdown():
    top = Toplevel(window)
    top.title("Select Email")

    c.execute("SELECT email FROM default_emails")
    emails = [row[0] for row in c.fetchall()]

    if emails:
        label = Label(top, text="Select an Email:")
        label.pack(pady=10)

        email_var = StringVar(top)
        email_var.set(emails[0])  # Default value is the first email

        dropdown = OptionMenu(top, email_var, *emails)  # Dropdown with emails
        dropdown.pack(pady=10)

        # Use selected email
        def select_email():
            selected_email = email_var.get()
            messagebox.showinfo("Selected Email", f"You selected: {selected_email}")
            # Here you can use the selected email for further processing
            top.destroy()

        Button(top, text="Select", command=select_email).pack(pady=10)
    else:
        messagebox.showwarning("No Emails", "No default emails found.")

# ---------------------------- UI SETUP ------------------------------- #

# creating a window
window = Tk()  # inititalized window object which creates a screen
window.title("PASSKEEPER")
# window.attributes('-fullscreen', True)
window.bind("<Escape>", exit_fullscreen)
window.config(padx=50, pady=50, bg=BLACK)

# adding the lock image in canvas which is located in window

# we are creating canvas object as we cannot directly add an image on the app through tkinter, canvas object acts as a
# drawing window

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=BLACK)
lock_img = PhotoImage(file="lock1file.png")  # creating image object to make it appear in canvas
canvas.create_image(130, 100, image=lock_img)  # adding image to canvas
canvas.grid(row=0, column=1)

# labels
website_label = Label(text="Website:", bg= BLACK, fg=TURQUOISE, font=FONT)
website_label.grid(row=2, column=0)

email_username_label = Label(text="Email/Username:", bg=BLACK, fg=TURQUOISE, font=FONT)
email_username_label.grid(row=3, column=0)

password_label = Label(text="Password:", bg=BLACK, fg=TURQUOISE, font=FONT)
password_label.grid(row=4, column=0)

# entries

# columnspan attribute extends entry upto the value assigned to it which represents column

# sticky attribute is used to align length of components like entries and buttons with the component possessing the
# longest length in directions e.g. EW(east-west), NE(north-east)
website_entry = Entry(width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
website_entry.grid(row=2, column=1, columnspan=2, pady=ENTRY_PAD)
website_entry.focus() # .focus() gets the cursor to website field as soon as the app opens

email_username_entry = Entry(width=59, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
email_username_entry.grid(row=3, column=1, columnspan=3, pady=ENTRY_PAD, sticky=EW)
email_username_entry.insert(index=0, string="ath@gmail.com")  # inserts a default email to the entry as soon as the app
# is opened

password_entry = Entry(width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
password_entry.grid(row=4, column=1, columnspan=2, pady=ENTRY_PAD)

# buttons
generate_password_button = Button(text="Generate Password", command=generate_password, bg=DARK_CHARCOAL, fg=TURQUOISE,
                                  font=FONT)
generate_password_button.grid(row=4, column=3, sticky=EW)

add_button = Button(text="Add", width=59, command=save, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
add_button.grid(row=5, column=1, columnspan=3, pady=ENTRY_PAD)

search_button = Button(text="Search", width=17, command=search_password, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
search_button.grid(row=2, column=3, sticky=EW)

# Add Default Email Button
Button(window, text="Add Default Email", command=save_default_email).grid(row=5, column=2)

# Show Default Emails Button
Button(window, text="Show Saved Emails", command=display_emails_in_dropdown).grid(row=6, column=1, columnspan=2)

window.mainloop()

# Close the database connection when the program exits
conn.close()


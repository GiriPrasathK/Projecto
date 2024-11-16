from tkinter import *
from tkinter import messagebox
import sqlite3
import string

BLACK = "#040514"
TURQUOISE = "#0ce3c7"
DARK_CHARCOAL = "#333031"
FONT = ("consolas", 10, "normal")
ENTRY_PAD = 7

# Connect to the SQLite database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()


def sign_up():
    numbers = string.digits

    mobile_no = mobile_no_entry.get()
    pin = pin_entry.get()

    # field validations
    if len(mobile_no) == 0 or len(pin) == 0:
        messagebox.showinfo(title="Error", message="Make sure you have not left any empty fields")
        return

    for number in mobile_no:
        if number not in numbers:
            messagebox.showinfo(title="Error", message="Please enter a valid Mobile.No without characters")
            return

    for number in pin:
        if number not in numbers:
            messagebox.showinfo(title="Error", message="Please enter a valid pin without characters")
            return

    if len(mobile_no) < 10 or len(mobile_no) > 10 or len(pin) < 4 or len(pin) > 6:
        messagebox.showinfo(title="Error", message="Please enter a valid Mobile.No")
        return
    elif len(pin) < 4 or len(pin) > 6:
        messagebox.showinfo(title="Error", message="Please enter a valid pin")
        return

    # creating new user_info table in database
    c.execute('''CREATE TABLE IF NOT EXISTS USER_INFO (
                    mobile_no TEXT NOT NULL, 
                    pin TEXT NOT NULL)''')

    c.execute("INSERT INTO USER_INFO (mobile_no, pin) VALUES (?, ?)",
              (mobile_no, pin))

    conn.commit()

    c.execute("SELECT mobile_no, pin FROM USER_INFO WHERE mobile_no = ?", (mobile_no,))  # corresponding
    # email and password is selected
    result = c.fetchone()  # entire row email and password is stored as tuple in the form (email, password)
    # in result variable

    # if result that is row exists
    if result:
        mobile_no, pin = result  # tuple of (email, password) gets separated and stored in email and password variable
        # independently

        # email and password is displayed in the below popup box
        messagebox.showinfo(title="user_info", message=f"Mobile.No: {mobile_no}\npin: {pin}")


# ----------------------------------UI SETUP-------------------------------------------------------------------#


window = Tk()  # initialized window object which creates a screen
window.title("Sign_up")
window.config(padx=50, pady=50, bg=BLACK)

canvas = Canvas(width=200, height=200, highlightthickness=0, bg=BLACK)
lock_img = PhotoImage(file="lock1file.png")  # creating image object to make it appear in canvas
canvas.create_image(130, 100, image=lock_img)  # adding image to canvas
canvas.grid(row=0, column=1)

# labels
mobile_no_label = Label(text="Set Mobile No.:", bg= BLACK, fg=TURQUOISE, font=FONT)
mobile_no_label.grid(row=2, column=0)

pin_label = Label(text="Set the pin:", bg=BLACK, fg=TURQUOISE, font=FONT)
pin_label.grid(row=2, column=0)

mobile_no_valid_label = Label(text="*Enter 10-digits number", bg= BLACK, fg=TURQUOISE, font=("consolas", 9, "normal"), pady=ENTRY_PAD)
mobile_no_valid_label.grid(row=3, column=1, sticky=W)

pin_valid_label = Label(text="*Enter 4 or 6-digits pin", bg= BLACK, fg=TURQUOISE, font=("consolas", 9, "normal"), pady=ENTRY_PAD)
pin_valid_label.grid(row=5, column=1, sticky=W)

# entries
mobile_no_entry = Entry(width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
mobile_no_entry.grid(row=2, column=1, columnspan=3, sticky=W)
mobile_no_entry.focus()  # .focus() gets the cursor to website field as soon as the app opens

pin_entry = Entry(width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
pin_entry.grid(row=4, column=1, columnspan=3, sticky=EW)

# button
sign_up_button = Button(text="Sign up", width=59, command=sign_up, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
sign_up_button.grid(row=7, column=1, columnspan=3, pady=ENTRY_PAD)

window.mainloop()

conn.close()
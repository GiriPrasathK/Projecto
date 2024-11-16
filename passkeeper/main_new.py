import sqlite3
from tkinter import *
from tkinter import messagebox, ttk
import string
import random
import pyperclip
import uuid
import time
import re

# Common constants
BLACK = "#040514"
TURQUOISE = "#0ce3c7"
DARK_CHARCOAL = "#333031"
FONT = ("consolas", 10, "normal")
ENTRY_PAD = 7

# Connect to the SQLite database
conn = sqlite3.connect('passwords.db')
c = conn.cursor()

# Main window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg=BLACK)

# Keep a reference to images to prevent garbage collection
images = {}


def is_valid_email(email):
    # Simple regex pattern for email validation
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email) is not None


# Function to check if user exists
def user_exists():
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='USER_INFO'")
    if c.fetchone():
        # Table exists, check if there's a user
        c.execute("SELECT * FROM USER_INFO")
        if c.fetchone():
            return True
    return False


# Start the application
def start_app():
    if user_exists():
        # User exists, show log-in page
        log_in_page()
    else:
        # No user, show sign-up page
        sign_up_page()


# ------------------- Sign-Up Page -------------------
def sign_up_page():
    # Clear the window
    for widget in window.winfo_children():
        widget.destroy()
    window.title("Sign Up")

    # Canvas and Image
    canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=BLACK)
    images['lock_img'] = PhotoImage(file="lock1file.png")  # Update the image path accordingly
    canvas.create_image(130, 100, image=images['lock_img'])
    canvas.grid(row=0, column=1)

    # Labels
    # username_label = Label(window, text="Set username.:", bg=BLACK, fg=TURQUOISE, font=FONT)
    # username_label.grid(row=2, column=0)

    pin_label = Label(window, text="Set the pin:", bg=BLACK, fg=TURQUOISE, font=FONT)
    pin_label.grid(row=4, column=0)

    # mobile_no_valid_label = Label(window, text="*Alphanumeric", bg=BLACK, fg=TURQUOISE,
    #                               font=("consolas", 9, "normal"), pady=ENTRY_PAD)
    # mobile_no_valid_label.grid(row=3, column=1, sticky=W)

    pin_valid_label = Label(window, text="*Enter 4 or 6-digits pin", bg=BLACK, fg=TURQUOISE,
                            font=("consolas", 9, "normal"), pady=ENTRY_PAD)
    pin_valid_label.grid(row=5, column=1, sticky=W)

    # Entries
    # username_entry = Entry(window, width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    # username_entry.grid(row=2, column=1, columnspan=3, sticky=W)
    # username_entry.focus()

    pin_entry = Entry(window, width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    pin_entry.grid(row=4, column=1, columnspan=3, sticky=EW)

    # Function for sign-up button
    def sign_up():
        # username = username_entry.get()
        pin = pin_entry.get()

        # Field validations
        if len(pin) == 0:
            messagebox.showinfo(title="Error", message="Make sure you have not left any empty fields")
            return

        # if not username.isdigit() and not username.isalpha():
        #     messagebox.showinfo(title="Error", message="Please enter a valid username")
        #     return

        if not pin.isdigit():
            messagebox.showinfo(title="Error", message="Please enter a valid pin without characters")
            return

        # if len(username) != 10:
        #     messagebox.showinfo(title="Error", message="Please enter a valid 10-digit Mobile No.")
        #     return
        if len(pin) not in (4, 6):
            messagebox.showinfo(title="Error", message="Please enter a valid 4 or 6-digit pin")
            return

        # Creating USER_INFO table in database
        # c.execute('''CREATE TABLE IF NOT EXISTS USER_INFO (
        #                 username TEXT NOT NULL,
        #                 pin TEXT NOT NULL)''')
        #
        # c.execute("INSERT INTO USER_INFO (username, pin) VALUES (?, ?)",
        #           (username, pin))

        c.execute('''CREATE TABLE IF NOT EXISTS USER_INFO (
                                 pin TEXT NOT NULL)''')

        c.execute("INSERT INTO USER_INFO (pin) VALUES (?)", (pin,))

        conn.commit()

        messagebox.showinfo(title="Success", message="Sign-up successful!")
        # Go to log-in page
        log_in_page()

    # Sign-up Button
    sign_up_button = Button(window, text="Sign up", width=59, command=sign_up, bg=DARK_CHARCOAL, fg=TURQUOISE,
                            font=FONT)
    sign_up_button.grid(row=7, column=1, columnspan=3, pady=ENTRY_PAD)


# ------------------- Log-In Page -------------------
def log_in_page():
    # Clear the window
    for widget in window.winfo_children():
        widget.destroy()
    window.title("Log In")

    # Canvas and Image
    canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=BLACK)
    images['lock_img'] = PhotoImage(file="lock1file.png")  # Update the image path accordingly
    canvas.create_image(130, 100, image=images['lock_img'])
    canvas.grid(row=0, column=1)

    # Label and Entry
    pin_label = Label(window, text="Enter the pin:", bg=BLACK, fg=TURQUOISE, font=FONT)
    pin_label.grid(row=2, column=0)

    pin_entry = Entry(window, width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT, show='*')
    pin_entry.grid(row=2, column=1, columnspan=3, pady=ENTRY_PAD, sticky=EW)
    pin_entry.focus()

    # Function for log-in button
    def log_in():
        pin = pin_entry.get()

        if len(pin) == 0:
            messagebox.showerror(title="Error!", message="Fill the pin field; it can't be empty!")
            return

        c.execute("SELECT pin FROM USER_INFO")
        result = c.fetchone()

        if result and pin == result[0]:
            messagebox.showinfo(title="Success", message="Login successful!")
            # Proceed to add password page
            add_password_page()
        else:
            messagebox.showerror(title="Error", message="Entered pin is wrong!")
            return

    # Log-in Button
    sign_in_button = Button(window, text="Log in", width=59, command=log_in, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    sign_in_button.grid(row=3, column=1, columnspan=3, pady=ENTRY_PAD)


# ------------------- Add Password Page -------------------
def add_password_page():
    # Clear the window
    for widget in window.winfo_children():
        widget.destroy()

    window.title("PASSKEEPER")
    window.config(padx=50, pady=50, bg=BLACK)

    # Canvas and Image
    images['lock_img'] = PhotoImage(file="lock1file.png")

    canvas = Canvas(window, width=240, height=200, highlightthickness=0, bg=BLACK)
    canvas.create_image(170, 100, image=images['lock_img'])
    canvas.grid(row=0, column=1)

    # Labels
    website_label = Label(window, text="Website:", bg=BLACK, fg=TURQUOISE, font=FONT)
    website_label.grid(row=2, column=0)

    email_var = StringVar()
    email_username_label = Label(window, text="Email/Username:", bg=BLACK, fg=TURQUOISE, font=FONT)
    email_username_label.grid(row=3, column=0)

    blank_label = Label(text=" "
                             " "
                             " "
                             " ", bg=BLACK)

    blank_label.grid(row=4, column=1)

    password_label = Label(window, text="Password:", bg=BLACK, fg=TURQUOISE, font=FONT)
    password_label.grid(row=6, column=0)

    # Entries
    website_entry = Entry(window, width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    website_entry.grid(row=2, column=1, columnspan=2, pady=ENTRY_PAD, sticky=EW)
    website_entry.focus()

    # email_username_entry = Entry(window, width=59, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    # email_username_entry.grid(row=3, column=1, columnspan=3, pady=ENTRY_PAD, sticky=EW)
    # email_username_entry.insert(index=0, string="ath@gmail.com")

    # Create a style object
    style = ttk.Style()

    # Set the theme to 'clam' or another that supports styling changes
    style.theme_use("clam")

    # Configure the style for the Combobox
    style.configure("TCombobox",
                    fieldbackground=DARK_CHARCOAL,  # The background color of the selected item
                    background=DARK_CHARCOAL,  # The dropdown button background color
                    foreground=TURQUOISE,  # The text color
                    selectbackground=DARK_CHARCOAL,  # The selected item's background in the dropdown
                    selectforeground=TURQUOISE)  # The selected item's text color

    dropdown = ttk.Combobox(window, width=59, height=15, textvariable=email_var)
    dropdown.grid(row=3, column=1, columnspan=3, pady=ENTRY_PAD, sticky=EW)

    password_entry = Entry(window, width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    password_entry.grid(row=6, column=1, columnspan=2, pady=ENTRY_PAD, sticky=EW)

    c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                                    website TEXT NOT NULL, 
                                    email TEXT NOT NULL, 
                                    password TEXT NOT NULL)''')

    # Functions for buttons
    def generate_password():
        password_entry.delete(first=0, last=END)  # Clear previous password

        # If "manual" is selected, open a popup to get custom lengths
        if password_length_choice.get() == "manual":
            manual_length_popup()  # Open popup window to get manual lengths
        else:
            # Default length generation
            create_random_password(nr_letters=10, nr_symbols=4, nr_numbers=4)  # Use default values

    def create_random_password(nr_letters, nr_symbols, nr_numbers):
        # Combine device-specific and time-based seeds
        device_seed = uuid.getnode()
        current_time_seed = time.time()

        combined_seed = device_seed + int(current_time_seed)
        random.seed(combined_seed)

        # Generate password components
        letters = string.ascii_letters
        numbers = string.digits
        symbols = '!#$%&()*+'

        # Create the password
        password_letters = [random.choice(letters) for _ in range(nr_letters)]
        password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]
        password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]

        password_list = password_letters + password_numbers + password_symbols
        random.shuffle(password_list)

        password = "".join(password_list)

        pyperclip.copy(password)  # Copy to clipboard
        password_entry.insert(index=0, string=password)

    def manual_length_popup():
        # Popup window to get manual lengths
        popup = Toplevel(window)
        popup.title("Enter Manual Lengths")
        popup.config(padx=50, pady=50, bg=BLACK)

        Label(popup, text="Number of Letters:", bg=BLACK, fg=TURQUOISE, font=FONT).grid(row=0, column=0, padx=10, pady=10)
        Label(popup, text="Number of Symbols:", bg=BLACK, fg=TURQUOISE, font=FONT).grid(row=1, column=0, padx=10, pady=10)
        Label(popup, text="Number of Numbers:", bg=BLACK, fg=TURQUOISE, font=FONT).grid(row=2, column=0, padx=10, pady=10)

        letters_entry = Entry(popup, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        symbols_entry = Entry(popup, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        numbers_entry = Entry(popup, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)

        letters_entry.grid(row=0, column=1, padx=10, pady=10)
        symbols_entry.grid(row=1, column=1, padx=10, pady=10)
        numbers_entry.grid(row=2, column=1, padx=10, pady=10)

        def get_manual_values():
            try:
                nr_letters = int(letters_entry.get())
                nr_symbols = int(symbols_entry.get())
                nr_numbers = int(numbers_entry.get())
                create_random_password(nr_letters, nr_symbols, nr_numbers)
                popup.destroy()  # Close popup after collecting data
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter valid numbers.")

        Button(popup, text="Generate", command=get_manual_values, bg=DARK_CHARCOAL, fg=TURQUOISE,
               font=FONT).grid(row=3, column=1, padx=10, pady=10)

    def save():
        website = website_entry.get()
        #email = email_username_entry.get()
        email = dropdown.get()
        password = password_entry.get()

        if len(website) == 0 or len(email) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops!", message="Please make sure you haven't left any fields empty.")
        elif not is_valid_email(email):
            messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
        else:
            is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\n "
                                                                  f"Email: {email}\nPassword: "
                                                                  f"{password}\nIs it ok to save?")
            if is_ok:
                c.execute("INSERT INTO passwords (website, email, password) VALUES (?, ?, ?)",
                          (website, email, password))
                conn.commit()

                website_entry.delete(first=0, last=END)
                password_entry.delete(first=0, last=END)
                #email_username_entry.delete(first=0, last=END)
                dropdown.delete(first=0, last=END)

    def search_password():
        website = website_entry.get()
        c.execute("SELECT email, password FROM passwords WHERE website = ?", (website,))
        result = c.fetchone()
        if result:
            email, password = result
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No password found for {website}.")

    def delete_account():
        confirm = messagebox.askyesno(title="Delete Account",
                                      message="Are you sure you want to delete your account? All data will be lost.")
        if confirm:
            c.execute("DROP TABLE IF EXISTS USER_INFO")
            c.execute("DROP TABLE IF EXISTS passwords")
            conn.commit()
            messagebox.showinfo(title="Account Deleted", message="Your account has been deleted.")
            # Return to sign-up page
            sign_up_page()

    def get_all_emails():
        c.execute('''CREATE TABLE IF NOT EXISTS default_emails (
                                    email TEXT NOT NULL)''')
        c.execute("SELECT email FROM default_emails")
        emails = [row[0] for row in c.fetchall()]
        return emails

    def update_dropdown():
        emails = get_all_emails()
        email_var.set('')
        dropdown['values'] = emails

    update_dropdown()

    # ---------------------------- Radio Buttons ------------------------------- #
    password_length_choice = StringVar(value="default")  # Default option

    # Create radio buttons for password length options
    default_radio = Radiobutton(window, text="Default Length", variable=password_length_choice, value="default",
                                bg=BLACK, fg=TURQUOISE, font=FONT)
    manual_radio = Radiobutton(window, text="Manual Length", variable=password_length_choice, value="manual", bg=BLACK,
                               fg=TURQUOISE, font=FONT)

    # Place the radio buttons below the email entry
    default_radio.grid(row=5, column=1, sticky="w", padx=10, pady=ENTRY_PAD)
    manual_radio.grid(row=5, column=2, sticky="w", padx=10, pady=ENTRY_PAD)

    # ---------------------------- save_default_emails ------------------------------- #
    def save_default_emails_page():
        # Clear the window
        for widget in window.winfo_children():
            widget.destroy()

        def save_default_email():
            # Create the default_emails table if it doesn't exist
            c.execute('''CREATE TABLE IF NOT EXISTS default_emails (
                                email TEXT NOT NULL)''')
            conn.commit()

            email = email_entry.get()

            # Email validation
            if len(email) == 0:
                messagebox.showinfo(title="Oops!", message="Please make sure you haven't left the email field empty.")
            elif not is_valid_email(email):
                messagebox.showinfo(title="Invalid Email", message="Please enter a valid email address.")
            else:
                # Displaying a pop-up box to confirm saving
                is_ok = messagebox.askokcancel(title="Confirm Email",
                                               message=f"Is it okay to save this email?\n\nEmail: {email}")

                if is_ok:
                    # Insert the email into the default_emails table
                    c.execute("INSERT INTO default_emails (email) VALUES (?)", (email,))
                    conn.commit()

                    # Clear the email field
                    email_entry.delete(first=0, last=END)
                    messagebox.showinfo(title="Success", message="Email has been saved successfully!")

        # Canvas and Image
        images['lock_img'] = PhotoImage(file="lock1file.png")

        canvas = Canvas(window, width=200, height=200, highlightthickness=0, bg=BLACK)
        canvas.create_image(120, 100, image=images['lock_img'])
        canvas.grid(row=0, column=1)

        # Labels
        email_label = Label(text="Enter Email:", bg=BLACK, fg=TURQUOISE, font=FONT)
        email_label.grid(row=1, column=0)

        # Entry
        email_entry = Entry(width=59, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        email_entry.grid(row=1, column=1, pady=ENTRY_PAD, columnspan=2)

        # Add Button
        add_button = Button(text="Add", width=59, command=save_default_email, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        add_button.grid(row=2, column=1, columnspan=2, pady=ENTRY_PAD)

        blank_label = Label(text=" "
                                 " "
                                 " "
                                 " ", bg=BLACK)

        blank_label.grid(row=3, column=1)

        # back Button
        back_button = Button(text="<-Back", width=22, command=add_password_page, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        back_button.grid(row=4, column=1, columnspan=2, pady=ENTRY_PAD)


    # ---------------------------- update_delete_password) ------------------------------- #

    def update_delete_password_page():

        # Clear the window
        for widget in window.winfo_children():
            widget.destroy()

        # ---------------------------- UPDATE PASSWORD ------------------------------- #
        def update_password():
            website = website_entry.get()

            # Check if the website field is not empty
            if len(website) == 0:
                messagebox.showinfo(title="Error", message="Please enter a website name to update.")
                return

            # Fetch the existing data for the website
            c.execute("SELECT email, password FROM passwords WHERE website = ?", (website,))
            result = c.fetchone()

            if result:
                # Display the current email and password in a popup for updating
                update_window = Toplevel(window)
                update_window.title("Update Password")
                update_window.config(padx=20, pady=20, bg=BLACK)

                # Labels and entries for email and password
                email_label = Label(update_window, text="Email/Username:", bg=BLACK, fg=TURQUOISE, font=FONT)
                email_label.grid(row=0, column=0)

                password_label = Label(update_window, text="Password:", bg=BLACK, fg=TURQUOISE, font=FONT)
                password_label.grid(row=1, column=0)

                email_entry = Entry(update_window, width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
                email_entry.grid(row=0, column=1, pady=ENTRY_PAD)
                email_entry.insert(0, result[0])  # Populate the existing email

                password_entry = Entry(update_window, width=40, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
                password_entry.grid(row=1, column=1, pady=ENTRY_PAD)
                password_entry.insert(0, result[1])  # Populate the existing password

                # Function to update the database
                def update_in_db():
                    new_email = email_entry.get()
                    new_password = password_entry.get()

                    if len(new_email) == 0 or len(new_password) == 0:
                        messagebox.showinfo(title="Error", message="Please fill in all fields.")
                    else:
                        c.execute("UPDATE passwords SET email = ?, password = ? WHERE website = ?",
                                  (new_email, new_password, website))
                        conn.commit()
                        messagebox.showinfo(title="Success", message="Password updated successfully!")
                        update_window.destroy()

                # Update button
                update_button = Button(update_window, text="Update", command=update_in_db, bg=DARK_CHARCOAL, fg=TURQUOISE,
                                       font=FONT)
                update_button.grid(row=2, column=0, columnspan=2, pady=ENTRY_PAD)
            else:
                messagebox.showinfo(title="Error", message="No password found for the given website.")

        # ---------------------------- DELETE PASSWORD ------------------------------- #
        def delete_password():
            website = website_entry.get()

            if len(website) == 0:
                messagebox.showinfo(title="Error", message="Please enter a website name to delete.")
                return

            # Confirmation popup
            is_ok = messagebox.askokcancel(title="Delete Confirmation",
                                           message=f"Are you sure you want to delete the record for {website}?")

            if is_ok:
                c.execute("DELETE FROM passwords WHERE website = ?", (website,))
                conn.commit()
                messagebox.showinfo(title="Success", message="Record deleted successfully!")

        # ---------------------------- UI SETUP ------------------------------- #

        # Canvas and Image
        images['lock_img'] = PhotoImage(file="lock1file.png")

        canvas = Canvas(window, width=250, height=200, highlightthickness=0, bg=BLACK)
        canvas.create_image(175, 100, image=images['lock_img'])
        canvas.grid(row=0, column=1)

        # Labels
        website_label = Label(text="Website:", bg=BLACK, fg=TURQUOISE, font=FONT)
        website_label.grid(row=2, column=0)

        # Entries
        website_entry = Entry(width=60, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        website_entry.grid(row=2, column=1, columnspan=2, pady=ENTRY_PAD, sticky=W)
        website_entry.focus()

        # Buttons
        update_button = Button(text="Update", width=20, command=update_password, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        update_button.grid(row=3, column=1, pady=ENTRY_PAD, sticky=W)

        delete_button = Button(text="Delete", width=20, command=delete_password, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        delete_button.grid(row=3, column=2, pady=ENTRY_PAD, sticky=E)


        blank_label = Label(text=" "
                                 " "
                                 " "
                                 " ", bg=BLACK)

        blank_label.grid(row=4, column=1)

        # back Button
        back_button = Button(text="<-Back", width=22, command=add_password_page, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
        back_button.grid(row=5, column=1, columnspan=2, pady=ENTRY_PAD)


    # ---------------------------- view_saved_websites ------------------------------- #

    def view_saved_websites_page():

        # Clear the window
        for widget in window.winfo_children():
            widget.destroy()

            # Fetching all saved websites from the database
            c.execute("SELECT website, email FROM passwords")
            websites = c.fetchall()  # This returns a list of tuples

            # If there are no saved websites
            if not websites:
                # messagebox.showinfo(title="No Websites", message="No websites have been saved yet.")
                # saved_websites_window.destroy()
                # return add_password_page()
                window.config(padx=0)

                back_button = Button(text="<-Back", width=22, command=add_password_page, bg=DARK_CHARCOAL, fg=TURQUOISE,
                                     font=FONT)
                back_button.grid(row=0, column=0, pady=ENTRY_PAD)
                line_label = Label(
                    text="_______________________________________________________________________________________________",
                    bg=BLACK, fg=TURQUOISE, font=FONT)
                line_label.grid(row=1, column=0, columnspan=4, pady=5)

                line_label = Label(
                    text="No website has been saved yet.",
                    bg=BLACK, fg=TURQUOISE, font=FONT)
                line_label.grid(row=2, column=0, columnspan=4, pady=5)
            else:

                window.config(padx=0)
                # back Button
                back_button = Button(text="<-Back", width=22, command=add_password_page, bg=DARK_CHARCOAL, fg=TURQUOISE,
                                     font=FONT)
                back_button.grid(row=0, column=0, pady=ENTRY_PAD)
                line_label = Label(text="_______________________________________________________________________________________________", bg=BLACK, fg=TURQUOISE, font=FONT)
                line_label.grid(row=1, column=0, columnspan=4, pady=5)
                # Display websites using Labels
                for index, (website, email) in enumerate(websites):
                    # website_label = Label(saved_websites_window, text=website, bg=BLACK, fg=TURQUOISE, font=FONT)
                    website_label = Label(text=website, bg=BLACK, fg=TURQUOISE, font=FONT)
                    website_label.grid(row=index + 2, column=0, pady=5)

                    website_label = Label(text=f"-{email}", bg=BLACK, fg=TURQUOISE, font=FONT)
                    website_label.grid(row=index + 2, column=1, pady=5)

    # Buttons
    generate_password_button = Button(window, text="Generate Password", command=generate_password, bg=DARK_CHARCOAL,
                                      fg=TURQUOISE, font=FONT)
    generate_password_button.grid(row=6, column=3, sticky=EW)

    add_button = Button(window, text="Add", width=59, command=save, bg=DARK_CHARCOAL, fg=TURQUOISE, font=FONT)
    add_button.grid(row=7, column=1, columnspan=3, pady=ENTRY_PAD, sticky=EW)

    search_button = Button(window, text="Search", width=17, command=search_password, bg=DARK_CHARCOAL, fg=TURQUOISE,
                           font=FONT)
    search_button.grid(row=2, column=3, sticky=EW)

    view_saved_websites_button = Button(text="view saved websites", command=view_saved_websites_page, bg=DARK_CHARCOAL,
                                        fg=TURQUOISE, font=FONT)
    view_saved_websites_button.grid(row=9, column=0, pady=20)

    save_default_emails_button = Button(text="save_default_emails", command=save_default_emails_page, bg=DARK_CHARCOAL,
                                        fg=TURQUOISE, font=FONT)
    save_default_emails_button.grid(row=9, column=1, columnspan=2, pady=20)

    update_passwords_button = Button(text="update_passwords", command=update_delete_password_page, bg=DARK_CHARCOAL,
                                     fg=TURQUOISE, font=FONT)
    update_passwords_button.grid(row=9, column=3, pady=20, columnspan=4, sticky=E)

    delete_account_button = Button(text="delete_account", command=delete_account, bg=DARK_CHARCOAL, fg=TURQUOISE,
                                   font=FONT)
    delete_account_button.grid(row=10, column=1, columnspan=2, pady=20, sticky=EW)


# Call the app's start logic
start_app()

# Main window loop
window.mainloop()

# Close the database connection when the program exits
conn.close()

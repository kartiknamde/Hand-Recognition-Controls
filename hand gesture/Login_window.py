import tkinter as tk #tkinter gui
import time # time module for timer
import mysql.connector  # for connecting to mysql database
from tkinter import messagebox  #for showing message box
from tkinter import *
import smtplib # for implementation of email verification
import random # for generating random otp
import re   # for verifing for of input detail 
import subprocess



def open_registration_window():
    global new_username_entry
    global new_password_entry
    global new_email_entry
    global otp_entry

    registration_window = tk.Toplevel(root)
    registration_window.title("Registration")

    # Set larger dimensions for the registration window
    window_width = 750
    window_height = 450
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's size and position
    registration_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    registration_window.configure(bg="#16dffa")  # Light Blue

    # Set the registration window as transient for the root window
    registration_window.transient(root)

    # Make the registration window a child window of the root window
    registration_window.top = root

    # Make the registration window a child window of the root window
    registration_window.top = root
    

    # Create new username label and entry for registration
    new_username_label = tk.Label(registration_window, text="New Username:", font=("Georgia", 20, "bold"), bg='white')
    new_username_label.place(x=20, y=20)
    new_username_entry = tk.Entry(registration_window, font=("Arial", 18), width=30)
    new_username_entry.place(x=240, y=20)

    # Create new password label and entry for registration
    new_password_label = tk.Label(registration_window, text="New Password:", font=("Georgia", 20, "bold"), bg='white')
    new_password_label.place(x=20, y=80)
    new_password_entry = tk.Entry(registration_window, show="*", font=("Arial", 18), width=30)
    new_password_entry.place(x=240, y=80)

    # Create new email label and entry for registration
    new_email_label = tk.Label(registration_window, text="Email:", font=("Georgia", 20, "bold"), bg='white')
    new_email_label.place(x=20, y=140)
    new_email_entry = tk.Entry(registration_window, font=("Arial", 18), width=30)
    new_email_entry.place(x=240, y=140)

    # Create register button for registration window
    register_button = tk.Button(registration_window, text="Register", command=generate_and_send_otp, font=("Georgia", 16, "bold"))
    register_button.place(x=240, y=200)

    # Create OTP label and entry for verification
    otp_label = tk.Label(registration_window, text="Enter OTP:", font=("Georgia", 20, "bold"), bg='white')
    otp_label.place(x=20, y=260)
    otp_entry = tk.Entry(registration_window, font=("Arial", 18), width=10)
    otp_entry.place(x=240, y=260)

    # Create verify button for OTP verification
    verify_button = tk.Button(registration_window, text="Verify OTP", command=verify_otp, font=("Georgia", 16, "bold"))
    verify_button.place(x=240, y=320)


def forget_password():



    forget_password_window = tk.Toplevel(root)
    forget_password_window.title("Forget Password")

    # Set dimensions for the forget password window
    window_width = 400
    window_height = 200
    screen_width = forget_password_window.winfo_screenwidth()
    screen_height = forget_password_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's size and position
    forget_password_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create labels and entries for username and email
    username_label = tk.Label(forget_password_window, text="Username:", font=("Verdana", 14), fg="purple", image=usernameimg, compound="left")
    username_label.grid(row=0, column=0, padx=10, pady=10)
    username_entry = tk.Entry(forget_password_window, font=("Arial", 14))
    username_entry.grid(row=0, column=1, padx=10, pady=10)

    email_label = tk.Label(forget_password_window, text="Email:", font=("Verdana", 14), fg="purple", image=usernameimg, compound="left")
    email_label.grid(row=1, column=0, padx=10, pady=10)
    email_entry = tk.Entry(forget_password_window, font=("Arial", 14))
    email_entry.grid(row=1, column=1, padx=10, pady=10)

    # Create a button to send OTP
    send_otp_button = tk.Button(
        forget_password_window, text="Send OTP", font=("Verdana", 14), fg="green")
    send_otp_button.grid(row=2, column=0, columnspan=2, pady=10)




def send_otp_and_open_new_window(username, email):
    # Generate and send OTP to the user's email
    generated_otp = str(random.randint(1000, 9999))
    send_otp(email, generated_otp)

    # Open a new window for OTP verification and password reset
    verify_otp_and_reset_password(username, generated_otp)



def verify_otp_and_reset_password(username, generated_otp):
    verify_otp_window = tk.Toplevel(root)
    verify_otp_window.title("Verify OTP")

    # Create labels and entry for OTP verification
    otp_label = tk.Label(verify_otp_window, text="Enter OTP:", font=("Georgia", 20, "bold"), bg='white')
    otp_label.grid(row=0, column=0, padx=10, pady=10)
    otp_entry = tk.Entry(verify_otp_window, font=("Arial", 18), width=10)
    otp_entry.grid(row=0, column=1, padx=10, pady=10)

    def verify_otp_and_change_password():
        entered_otp = otp_entry.get()

        if not entered_otp:
            messagebox.showerror("Incomplete Information", "Please enter the OTP.")
            return

        # Check if the entered OTP matches the generated OTP
        if entered_otp == generated_otp:
            change_password_window = tk.Toplevel(root)
            change_password_window.title("Change Password")

            # Create label and entry for new password
            new_password_label = tk.Label(change_password_window, text="New Password:", font=("Georgia", 20, "bold"), bg='white')
            new_password_label.grid(row=0, column=0, padx=10, pady=10)
            new_password_entry = tk.Entry(change_password_window, show="*", font=("Arial", 18), width=30)
            new_password_entry.grid(row=0, column=1, padx=10, pady=10)

            def update_password():
                new_password = new_password_entry.get()

                if not new_password:
                    messagebox.showerror("Incomplete Information", "Please enter the new password.")
                    return

                # Update the password in the database
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='os'
                )
                cursor = conn.cursor()

                cursor.execute("UPDATE login_info SET password = %s WHERE username = %s", (new_password, username))
                conn.commit()

                conn.close()

                messagebox.showinfo("Password Updated", "Your password has been successfully updated.")
                verify_otp_window.destroy()
                change_password_window.destroy()

            # Create a button to update the password
            update_password_button = tk.Button(
                change_password_window, text="Update Password", command=update_password, font=("Georgia", 16, "bold"))
            update_password_button.grid(row=1, column=0, columnspan=2, pady=10)

        else:
            messagebox.showerror("Invalid OTP", "The entered OTP is incorrect.")

    # Create a button to verify the OTP
    verify_otp_button = tk.Button(
        verify_otp_window, text="Verify OTP", command=verify_otp_and_change_password, font=("Georgia", 16, "bold"))
    verify_otp_button.grid(row=1, column=0, columnspan=2, pady=10)


# Update the send_otp function with app-specific password
def send_otp(email, otp):
    sender_email = 'dmyacc0364@gmail.com'
    app_specific_password = 'njnh knif etgf ugjt'  # This is apps specific password generated from google account
    subject = 'Verification Code for Hand Gesture Controlling.'
    message = f'Your verification code is: {otp}'

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server: # connects to the smtp server with standard port 587
            server.starttls() # initiates a TLS (Transport Layer Security) encryption session
            server.login(sender_email, app_specific_password)

            msg = f'Subject: {subject}\n\n{message}'
            server.sendmail(sender_email, email, msg)

        messagebox.showinfo("Verification Code Sent", "An email with the verification code has been sent to your email address.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send the verification code. {str(e)}")



def generate_and_send_otp():
    global generated_otp # global makes the otp available for all the other functions
    email = new_email_entry.get()

    if not email:
        messagebox.showerror("Incomplete Information", "Please enter your email.")
        return

    # Check if the email is in a valid format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        messagebox.showerror("Invalid Email", "Please enter a valid Email format.")
        return

    # Generate a random 4-digit OTP
    generated_otp = str(random.randint(1000, 9999))

    # Send the OTP to the provided email
    send_otp(email, generated_otp) # calls the send_otp function with email and generated otp as an argument


def verify_otp():
    global generated_otp
    entered_otp = otp_entry.get() # it retrives the enered otp form user entry widgit

    if not entered_otp: #checks whether the otp entry label is empty or not
        messagebox.showerror("Incomplete Information", "Please enter the OTP.")
        return

    # Check if the entered OTP matches the generated OTP
    if entered_otp == generated_otp:
        register_user()  # Proceed with user registration if OTP is verified
    else:
        messagebox.showerror("Invalid OTP", "The entered OTP is incorrect.")




# Function to verify user credentials and open a new window on successful login
def verify_credentials():
    username = username_entry.get()
    password = password_entry.get()

    if not username or not password: # shows error message if username or password is empty
        messagebox.showerror("Incomplete Information", "Please enter both username and password.")
        return

    # Connect to the MySQL database 
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='os'
    )
    cursor = conn.cursor()

    # Query to check if the username and password exist in the database
    cursor.execute("SELECT * FROM login_info WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone() # retrives the first row if data found and if not it will be None

    conn.close()

    if user:
        messagebox.showinfo("Login Successful",
                            "WELCOME, " + username + "   😄 ")
        new_os_window()
        root.withdraw()  # Hide the login window
    else:
        messagebox.showerror("Login Failed", "Invalid username or password  😓")






# Function to handle user registration
def register_user():
    global new_username_entry
    global new_password_entry
    global new_email_entry
    global otp_entry

    new_username = new_username_entry.get() # it retrives the enered username form user entry widgit
    new_password = new_password_entry.get() # it retrives the enered password form user entry widgit
    new_email = new_email_entry.get()       # it retrives the enered email form user entry widgit

    if not new_username or not new_password or not new_email:
        messagebox.showerror("Incomplete Information", "Please enter username, password, and email.")
        return

    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='os'
    )
    cursor = conn.cursor()

    # Check if the username or email already exists
    cursor.execute("SELECT * FROM login_info WHERE username = %s OR email = %s", (new_username, new_email))
    existing_user = cursor.fetchone() 

    if existing_user:
        if existing_user[1] == new_username:
            messagebox.showerror("Registration Error", "Username already exists. Please choose a different one.")
        elif existing_user[3] == new_email:
            messagebox.showerror("Registration Error", "Email already exists. Please use a different one.")
    else:
        # Insert the new user into the "login_info" table
        cursor.execute("INSERT INTO login_info (id, username, password, email) VALUES (NULL, %s, %s, %s)",
                       (new_username, new_password, new_email))
        conn.commit() # it is used to commit the inserted details into database
        messagebox.showinfo("Registration Successful", f"Registration successful for user: {new_username}")

        # Clear the entry fields only if the registration is successful
        new_username_entry.delete(0, 'end')
        new_password_entry.delete(0, 'end')
        new_email_entry.delete(0, 'end')
        otp_entry.delete(0, 'end')

    conn.close()


def log_out():
    # Show a confirmation message box
    confirmation = messagebox.askquestion("Confirm Log Out", "Are you sure you want to log out?")

    if confirmation == "yes":
        # User clicked "Yes," so log out and return to the login window and also erase the previously enered detail
        username_entry.delete(0, "end")
        password_entry.delete(0, "end")
        new_window.withdraw()
        root.deiconify()  # Show the login window
        new_window.destroy()



def new_os_window():
    root.withdraw()  # Hide the login window
    
    global new_window
    new_window = tk.Toplevel()
    new_window.geometry("1000x562+300+100")
    new_window.title("Hand Gesture Controlling")

    window_width = 1000
    window_height = 562
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Set the window's size and position
    new_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def Date_Tim():
        time_string = time.strftime("%H:%M:%S")
        date_string = time.strftime("%d/%m/%Y")
        clockdateLabel.configure(text=" Date : " + date_string)
        clocktimLabel.configure(text=" Time : " + time_string)
        clocktimLabel.after(1000, Date_Tim) # this will update the time after every 1 sec that is after 1000 m/s

    new_os_background_image = tk.PhotoImage(file='assets/images/2.png')
    new_os_background_label = tk.Label(new_window, image=new_os_background_image)
    new_os_background_label.place(relwidth=1, relheight=1)

    
    def open_camera_program():
        subprocess.run(["python", "HGR.py"])


    # TopLevel Frame Title
    root_title = Label(new_window, text="Hand Gesture Control using ML", fg="black", bg='#56e8cb', font=("Courier New", 40, "bold"),relief='groove', bd=2)
    root_title.pack(side='top', fill='x')

    # TopLevel Date Time Admin Frame

    Admin_dateFrame = Frame(new_window, bg="#c887ed", height=64, relief='groove', bd=5)
    Admin_dateFrame.pack(fill='x') # this will create the the frame in new window for the username, date, time is shown

    nameLabel = Label(Admin_dateFrame, text="Name:", font=("Arial", 13, "bold"), bg="#c887ed")
    nameLabel.place(x=10, y=0, relheight=1) # this label is added to admin label

    nameValLabel = Label(Admin_dateFrame, font=("Arial", 14, "italic bold"), fg='black', bg="#c887ed", padx=5)
    nameValLabel.place(x=68, y=0, relheight=1) # this label is added to admin label

    # Get the username from the login window
    username = username_entry.get()
    # Set the username in the nameValLabel
    nameValLabel.config(text=username)

    calanderimg = PhotoImage(file='assets/images/Calendar.png')
    calanderimg = calanderimg.subsample(1, 1)

    clockimg = PhotoImage(file='assets/images/Clock.png')
    clockimg = clockimg.subsample(1, 1)

    cameraimg = PhotoImage(file='assets/images/camera.png')
    cameraimg = cameraimg.subsample(6, 6)

    clockdateLabel = Label(Admin_dateFrame, image=calanderimg, font=('times', 14, 'bold'), relief='flat', bg='#c887ed', compound='left')
    clockdateLabel.place(x=470, y=0, relheight=1)

    clocktimLabel = Label(Admin_dateFrame, image=clockimg, font=('times', 14, 'bold'), relief='flat', bg='#c887ed', compound='left')
    clocktimLabel.place(x=690, y=0, relheight=1)
    Date_Tim()



    add_Logoutbutton = Button(Admin_dateFrame, text="Log Out", font=("Optima", 14, "bold"), fg='black', bg="#C0392B", activebackground='#C0392B', activeforeground='white', width=8,command=log_out)
    add_Logoutbutton.place(x=880, y=0, relheight=0.9)


    # DashBoard Button Frame and Image
    dashboardframe = Frame(new_window) # this frame will hold all the buttons inside it
    dashboardframe.pack(fill='both')

    add_openbtn = Button(new_window, text="Open Camera", font=("Optima", 12, "bold"), fg='black',
                            bg="#78888a",
                            activebackground='#78888a', activeforeground='white', bd=10, width=200, height=60, image=cameraimg, compound='left',
                            command=open_camera_program)
    add_openbtn.place(relx=0.4, rely=0.74)

    # Add a text area
    tutorial_text = "Tutoriol :                                       1. Click on Open Camera Button to start hand gesture recognization.                            2. Press 'q' to Quit the Camera.                   3. Click Logout Button to fully Logout"

    tutorial_area = tk.Text(new_window, wrap="word", font=("Courier New", 14, "bold"), height=10, width=50, bg="black", fg="green")
    tutorial_area.insert("1.0", tutorial_text)
    tutorial_area.config(state="disabled")  # Make the text area read-only
    tutorial_area.pack(pady=20)

    # Frame Raise will put the new main window on top 
    def raise_frame(fm):
        fm.tkraise()

    # Start the main loop for the new window
    new_window.mainloop()














# Create the main window
root = tk.Tk()
root.title("Welcome !!!, Login to Use Hand Gesture Control")

passwordimg = PhotoImage(file='assets/images/Password.png')
passwordimg = passwordimg.subsample(6, 6)

usernameimg = PhotoImage(file='assets/images/User.png')
usernameimg = usernameimg.subsample(1, 1)

passwordimg = PhotoImage(file='assets/images/pass.png')
passwordimg = passwordimg.subsample(1, 1)  



# Set window size and position
window_width = 1000
window_height = 562
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# Load background image (you should replace 'background.jpg' with your image file)
background_image = tk.PhotoImage(file='assets/images/1.png')
background_label = tk.Label(root, image=background_image)
background_label.place(relwidth=1, relheight=1)

# Create a heading label
heading_label = tk.Label(root, text="Please Enter Login Info", font=(
    "Impact", 35, "bold"), fg="red")
heading_label.place(relx=0.28, rely=0.15)



login_img = tk.PhotoImage(file='assets/images/Loginimg.png')
login_img = login_img.subsample(4, 5)
login_label = tk.Label(root, image=login_img)
login_label.place(relx=0.45, rely=0.3)


# Create username label and entry
username_label = tk.Label(root, text="Username:", font=("Verdana", 14), fg="purple", image=usernameimg, compound="left")
username_label.place(relx=0.33, rely=0.5)
username_entry = tk.Entry(root, font=("Arial", 14))
username_entry.place(relx=0.48, rely=0.5)
#username_entry.configure(bg=root.cget('bg'))

# Create password label and entry
password_label = tk.Label(root, text="Password:", font=("Verdana", 14), fg="purple", image=passwordimg, compound="left")
password_label.place(relx=0.33, rely=0.6)
password_entry = tk.Entry(root, show="*", font=("Arial", 14))
password_entry.place(relx=0.48, rely=0.6)
#password_entry.configure(bg=root.cget('bg'))

# Create login button
login_button = tk.Button(
    root, text="Login", command=verify_credentials, font=("Verdana", 14), fg="green")
login_button.place(relx=0.32, rely=0.7)

# Create register button
register_button = tk.Button(
    root, text="Register", command=open_registration_window, font=("Verdana", 14), fg="blue")
register_button.place(relx=0.42, rely=0.7)

forget_password_button = tk.Button(
    root, text="Forget Password",  command=forget_password, font=("Verdana", 14), fg="red")
forget_password_button.place(relx=0.55, rely=0.7)



# Start the main loop
root.mainloop()
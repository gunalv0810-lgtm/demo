from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from tensorflow.keras.models import load_model
from tkinter import messagebox
import mysql.connector

root = Tk()

root.title("SkinLens AI")
root.state("zoomed")
root.configure(bg="#FAFAFA")
selected_image_path = ""
model = load_model("skin_disease_model.h5")
preview_label = None
result_preview_model = None

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# ===== FUNCTION =====

def show_frame(frame):
    frame.tkraise()

def select_image():
    global selected_image_path
    file_path = filedialog.askopenfilename(
        title="Select Skin Image",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if file_path:
        selected_image_path = file_path
        print("Selected Image:",selected_image_path)

    image = Image.open(selected_image_path)
    image = image.resize((250, 250))
    photo = ImageTk.PhotoImage(image)
    preview_label.config(image=photo)
    preview_label.image = photo

class_names = [
    "Actinic Keratoses (AKIEC)",
    "Basal Cell Carcinoma (BCC)",
    "Benign Keratosis (BKL)",
    "Dermatofibroma (DF)",
    "Melanoma (MEL)",
    "Melanocytic Nevus (NV)",
    "Vascular Lesion (VASC)"
]

def analyse_image():

    global selected_image_path

    if selected_image_path == "":
        print("No image selected")
        return

    image = Image.open(selected_image_path)
    image = image.resize((128, 128))
    image = np.array(image)
    image = image / 255.0
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)
    confidence = np.max(prediction) * 100
    predicted_class = class_names[np.argmax(prediction)]

    result_disease.set(f"Disease: {predicted_class}")

    result_confidence.set(
        f"Confidence: {confidence:.2f}%"
    )

    # AI Instructions
    if confidence >= 50:

        result_instruction.set(
            "AI prediction confidence is strong. Please consult a dermatologist for professional medical confirmation."
        )

    elif confidence >= 30:

        result_instruction.set(
            "Moderate confidence detected. Try using a clearer skin image for better AI analysis."
        )

    else:

        result_instruction.set(
            "Low confidence prediction. The image may be unclear or the condition may visually overlap with other diseases."
        )

    result_img = Image.open(selected_image_path)
    result_img = result_img.resize((250,250))
    result_photo = ImageTk.PhotoImage(result_img)
    result_image_label.config(image = result_photo)
    result_image_label.image= result_photo
    result_image_label.pack(pady=20)
    show_frame(result_page)

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="ai_skin_analyser"

    )
       
def create_account():
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    mobile = mobile_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    confirm_password = confirm_password_entry.get()

    if first_name == "":
        messagebox.showerror("Error","First name required")
        return
    if password != confirm_password:
        messagebox.showerror("Error","Password do not match")
        return


    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM users WHERE email=%s OR mobile=%s """ ,(email,mobile))
    
    existing_user = cursor.fetchone()


    if existing_user:

        messagebox.showerror("Error","Email or mobile number already exist")

        cursor.close()
        conn.close()

        return
 
    conn = connect_db()

    cursor = conn.cursor()

    query = """ INSERT INTO users
          (first_name, last_name, mobile, email, password)
          VALUES (%s, %s, %s, %s, %s)"""
    
    values =(first_name, last_name, mobile, email, password)

    cursor.execute(query, values)

    conn.commit()
    cursor.close()
    conn.close()
    
    messagebox.showinfo("Success","Account created successfully")

    show_frame(dashboard_page)

    
def login_user():
    email_or_mobile= login_email_entry.get()
    password= login_password_entry.get()
    conn = connect_db()
    cursor = conn.cursor()

    query = """ SELECT * FROM users WHERE (email= %s OR mobile =%s) AND password= %s """

    cursor.execute(
        query,
        (
            email_or_mobile,
            email_or_mobile,
            password
        )
    )

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:

        messagebox.showinfo(
            "Success",
            "Login Successful"
        )

        show_frame(dashboard_page)

    else:

        messagebox.showerror(
            "Error",
            "Invalid Credentials"
        )


# ===== CONTAINER =====
container = Frame(root)
container.pack(fill="both", expand=True)

# ===== PAGES =====

front_page = Frame(container, bg="#FAFAFA")
auth_page = Frame(container, bg="#FAFAFA")
signup_page = Frame(container, bg="#FAFAFA")
login_page = Frame(container, bg="#FAFAFA")
dashboard_page = Frame(container, bg="#FAFAFA")
result_page = Frame(container, bg="#FAFAFA")

for frame in (front_page, auth_page, signup_page, login_page, dashboard_page, result_page):
    frame.place(relwidth=1, relheight=1)

# ===== FRONT PAGE =====

header = Frame(
    front_page,
    bg="white",
    height=70
)

header.pack(fill=X)

header.pack_propagate(False)

Label(
    header,
    text="🎓",
    font=("Segoe UI",28),
    bg="white"
).pack(side=LEFT,padx=40)

Label(
    header,
    text="SkinLens AI",
    font=("Segoe UI",18,"bold"),
    fg="#1D1D1F",
    bg="white"
).pack(side=LEFT)

content= Frame(front_page,bg="#FAFAFA")

content.pack(fill=BOTH, expand= True)

Label (content,text="AI Skin Disease \nClassifier.",
               font=("Segoe UI",48,"bold"),fg="#1D1D1F",
               bg="#FAFAFA",justify= CENTER).pack(pady=45)

Label (content,text="AI powered skin disease prediction & analysis",
               font=("Segoe UI" ,14), fg="#6E6E73",
               bg="#FAFAFA").pack(pady=10)

Button(content,text="Get Started",font=("Segoe UI",12), fg="white",
       bg="#0074FF", relief=FLAT, padx=45, pady=15,cursor="hand2",bd=0,
       command=lambda: show_frame(auth_page)).pack(pady=40)
              
# ===== AUTH PAGE =====

header = Frame(auth_page, bg="white", height=70)
header.pack(fill=X)

header.pack_propagate(False)

auth_content = Frame(auth_page, bg="#FAFAFA")
auth_content.pack(expand=True)

Label(
    header,
    text="🎓",
    font=("Segoe UI",28),
    bg="white"
).pack(side=LEFT,padx=40)

Label(header,
      text="SkinLens AI",
      font=("Segoe UI", 18, "bold"),
      bg="white",
      fg="#1D1D1F").pack(side=LEFT)

Label(auth_content,
      text="Welcome!",
      font=("Segoe UI",35,"bold"),
      fg="#1D1D1F",
      bg="#FAFAFA").pack(pady=(20,10))

Label(auth_content,
      text="To continue your AI skin analysis you need to Login",
      font=("Segoe UI",14),
      fg="#6E6E73",
      bg="#FAFAFA").pack()

auth_card = Frame(
    auth_content,
    bg="white"
)

auth_card.pack(
    pady=50,
    ipadx=100,
    ipady=80
)

auth_btn_frame = Frame(
    auth_card,
    bg="white"
)

auth_btn_frame.pack(pady=20)

# Sign In button
Button(
    auth_btn_frame,
    text="Sign up",
    font=("Segoe UI",12),
    bg="#007AFF",
    fg="white",
    relief=FLAT,
    width=10,
    padx=45,
    pady=17,
    bd=0,
    command=lambda: show_frame(signup_page)
).pack(side= LEFT,padx=20)


# Login button
Button(
    auth_btn_frame,
    text="Login",
    font=("Segoe UI",12),
    bg="white",
    fg="#007AFF",
    relief=SOLID,
    width=10,
    bd=1,
    padx=40,
    pady=17,
    command=lambda: show_frame(login_page)
).pack(side= LEFT,padx=20)


# Back button
Button(auth_page,
       text="← Back",
       font=("Segoe UI", 11),
       bg="#FAFAFA",
       bd=0,
       cursor="hand2",
       command=lambda: show_frame(front_page)
).place(x=1150, y=650)

# ================= SIGNUP PAGE =================

# Header
header = Frame(signup_page, bg="white", height=70)
header.pack(fill=X)

header.pack_propagate(False)

Label(
    header,
    text="🎓",
    font=("Segoe UI",28),
    bg="white"
).pack(side=LEFT,padx=40)

Label(header,
      text="SkinLens AI",
      font=("Segoe UI", 18, "bold"),
      bg="white",
      fg="#1D1D1F").pack(side=LEFT)

Button(signup_page,
       text="← Back",
       font=("Segoe UI", 11),
       bg="#FAFAFA",
       bd=0,
       cursor="hand2",
       command=lambda: show_frame(auth_page)
).place(x=1150, y=650)

Label(signup_page,
      text="Create Your Account",
      font=("Segoe UI", 34, "bold"),
      fg="#1D1D1F",
      bg="#FAFAFA").pack(pady=(30,10))

Label(signup_page,
      text="Join SkinLens AI today & analyse",
      font=("Segoe UI", 13),
      fg="#6E6E73",
      bg="#FAFAFA").pack()

# Form Frame
form_frame = Frame(signup_page, bg="#FAFAFA")
form_frame.pack(pady=25)

name_frame = Frame(form_frame, bg="#FAFAFA")
name_frame.pack(pady=10)

#First Name
first_name_frame = Frame(name_frame, bg="#FAFAFA")
first_name_frame.pack(side=LEFT, padx=8)

Label(first_name_frame,
      text="First Name",
      font=("Segoe UI",10),
      fg="#6E6E73",
      bg="#FAFAFA").pack(anchor="w")

first_name_entry = Entry(
      first_name_frame,
      font=("Segoe UI",12),
      relief=FLAT,
      bg="#F2F2F7",
      width=16)

first_name_entry.pack(ipady=4)

#Last Name
last_name_frame = Frame(name_frame, bg="#FAFAFA")
last_name_frame.pack(side=LEFT, padx=8)

Label(last_name_frame,
      text="Last Name",
      font=("Segoe UI",10),
      fg="#6E6E73",
      bg="#FAFAFA").pack(anchor="w")

last_name_entry = Entry(
      last_name_frame,
      font=("Segoe UI",12),
      relief=FLAT,
      bg="#F2F2F7",
      width=16)

last_name_entry.pack(ipady=4)

# Mobile
Label(form_frame,
      text="Mobile Number",
      font=("Segoe UI",10),
      fg="#6E6E73",
      bg="#FAFAFA").pack(anchor="w")

mobile_entry = Entry(form_frame,
      font=("Segoe UI", 12),relief=FLAT,bg="#F2F2F7",
      width=35)

mobile_entry.pack(pady=10,ipady=4)


# Email
Label(form_frame,
      text="Your Email",
      font=("Segoe UI",10),
      fg="#6E6E73",bg="#FAFAFA").pack(anchor="w")

email_entry = Entry(
    form_frame,
    font=("Segoe UI",12),
    relief=FLAT,
    bg="#F2F2F7",
    width=35
)

email_entry.pack(pady=10, ipady=4)

# Password
password_frame = Frame(form_frame,bg="#FAFAFA")
password_frame.pack(pady=10)

pswd_frame = Frame(password_frame,bg="#FAFAFA")
pswd_frame.pack(side= LEFT,padx=8)

Label(pswd_frame,text="Set Password",font=("Segoe UI",10),
      fg="#6E6E73", bg="#FAFAFA").pack(anchor="w")

password_entry = Entry(pswd_frame,
      font=("Segoe UI", 12),relief=FLAT,bg="#F2F2F7",
      width=16,
      show="*")

password_entry.pack(pady=10, ipady=4)

# Confirm Password
pswd_frame2= Frame(password_frame,bg="#FAFAFA")
pswd_frame2.pack(side= LEFT,padx=8)

Label(pswd_frame2,text="Confirm Password",font=("Segoe UI",10),
      fg="#6E6E73", bg="#FAFAFA").pack(anchor="w")

confirm_password_entry = Entry(pswd_frame2,
      font=("Segoe UI", 12),relief=FLAT,bg="#F2F2F7",
      width=16,
      show="*")

confirm_password_entry.pack(pady=10, ipady=4)

# Submit Button
Button(signup_page,
       text="Create Account",
       font=("Segoe UI", 12),
       bg="#007AFF",
       fg="white",
       relief=FLAT,
       padx=40,
       pady=12,
       cursor="hand2",
       bd=0, command= create_account).pack(pady=20)


# ================= LOGIN PAGE =================

# Header
header = Frame(login_page, bg="white", height=70)
header.pack(fill=X)

header.pack_propagate(False)

Label(header,
      text="🎓",
      font=("Segoe UI ", 28),
      bg="white").pack(side=LEFT, padx=40)

Label(header,
      text="SkinLens AI",
      font=("Segoe UI", 18, "bold"),
      bg="white",
      fg="#1D1D1F").pack(side=LEFT, padx=40, pady=15)

Label(login_page,
      text="Welcome Back",
      font=("Segoe UI",34,"bold"),
      fg="#1D1D1F",
      bg="#FAFAFA").pack(pady=(80,10))

Label(login_page,
      text="Login to continue your AI skin analysis",
      font=("Segoe UI",13),
      fg="#6E6E73",
      bg="#FAFAFA").pack()

form_frame = Frame(login_page, bg="#FAFAFA")
form_frame.pack(pady=30)

Button(login_page,
       text="← Back",
       font=("Segoe UI", 11),
       bg="#FAFAFA",
       bd=0,
       cursor="hand2",
       command=lambda: show_frame(auth_page)
).place(x=1050, y=650)

# Email / Mobile
Label(form_frame,
      text="Email",
      font=("Segoe UI",10),
      fg="#6E6E73",
      bg="#FAFAFA").pack(anchor="w")

login_email_entry= Entry(form_frame,
      font=("Segoe UI", 12),relief=FLAT,bg="#F2F2F7",
      width=35)
login_email_entry.pack(pady=10,ipady=4)

# Password
Label(form_frame,text="Password",
      font=("Segoe UI",10),
      fg="#6E6E73",
      bg="#FAFAFA").pack(anchor="w")

login_password_entry= Entry(form_frame,
      font=("Segoe UI", 12),relief=FLAT,bg="#F2F2F7",
      width=35,show="*")
login_password_entry.pack(pady=10,ipady=4)

# Login Button
Button(form_frame,
       text="Login",
       font=("Segoe UI", 12),
       bg="#007AFF",
       fg="white",
       relief=FLAT,
       padx=40,
       pady=12,
       cursor="hand2",
       bd=0, command= login_user
).pack(pady=20)

# ================= DASHBOARD PAGE =================
result_disease = StringVar()
result_confidence = StringVar()
result_instruction = StringVar()

Button(dashboard_page,
       text="← Back",
       font=("Segoe UI", 11),
       bg="#FAFAFA", fg="#6E6E73",
       bd=0, cursor="hand2",
       command=lambda: show_frame(front_page)
).place(x=40, y=20)

Label(dashboard_page,
      text="SkinLens AI",
      font=("Segoe UI", 13, "bold"),
      fg="#1D1D1F", bg="#FAFAFA"
).place(x=760, y=22)

Label(dashboard_page,
      text="Upload a skin image for analysis",
      font=("Segoe UI", 32, "bold"),
      fg="#1D1D1F", bg="#FAFAFA"
).pack(pady=(80, 8))

Label(dashboard_page,
      text="Clear, well-lit photos give the best results",
      font=("Segoe UI", 13),
      fg="#6E6E73", bg="#FAFAFA"
).pack()

# Image preview
preview_label = Label(dashboard_page, bg="#FAFAFA")
preview_label.pack(pady=25)

# Buttons
btn_frame = Frame(dashboard_page, bg="#FAFAFA")
btn_frame.pack(pady=10)

Button(btn_frame,
       text="Select Photo",
       font=("Segoe UI", 12),
       bg="white", fg="#007AFF",
       relief=SOLID, bd=1,
       padx=35, pady=12,
       cursor="hand2",
       command=select_image
).pack(side=LEFT, padx=12)

Button(btn_frame,
       text="Analyse",
       font=("Segoe UI", 12, "bold"),
       bg="#007AFF", fg="white",
       relief=FLAT, bd=0,
       padx=40, pady=12,
       cursor="hand2",
       command=analyse_image
).pack(side=LEFT, padx=12)

# ================= RESULT PAGE =================

Button(result_page,
       text="← Back",
       font=("Segoe UI", 11),
       bg="#FAFAFA", fg="#6E6E73",
       bd=0, cursor="hand2",
       command=lambda: show_frame(dashboard_page)
).place(x=40, y=20)

Label(result_page,
      text="SkinLens AI",
      font=("Segoe UI", 13, "bold"),
      fg="#1D1D1F", bg="#FAFAFA"
).place(x=760, y=22)

Label(result_page,
      text="AI Analysis Result",
      font=("Segoe UI", 32, "bold"),
      fg="#1D1D1F", bg="#FAFAFA"
).pack(pady=(80, 10))

# Uploaded image preview
result_image_label = Label(result_page, bg="#FAFAFA")
result_image_label.pack(pady=10)

# Result Card
result_card = Frame(result_page, bg="white", bd=0)
result_card.pack(pady=20, ipadx=60, ipady=30)

Label(result_card,
      textvariable=result_disease,
      font=("Segoe UI", 26, "bold"),
      fg="#007AFF", bg="white"
).pack(pady=(15, 5))

Label(result_card,
      textvariable=result_confidence,
      font=("Segoe UI", 14),
      fg="#1D1D1F", bg="white"
).pack(pady=5)

Frame(result_card, bg="#F2F2F7", height=1).pack(fill=X, padx=30, pady=10)

Label(result_card,
      textvariable=result_instruction,
      font=("Segoe UI", 12),
      fg="#6E6E73", bg="white",
      wraplength=500, justify=CENTER
).pack(pady=(5, 15))

Label(result_page,
      text="⚠️  For educational purposes only. Consult a dermatologist for medical diagnosis.",
      font=("Segoe UI", 10),
      fg="#FF3B30", bg="#FAFAFA",
      wraplength=600
).pack(pady=15)

# ===== START PAGE =====
show_frame(front_page)
root.mainloop()

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from tkinter import *
from PIL import ImageTk, Image  # type "Pip install pillow" in your terminal to install ImageTk and Image module
import os
import re
import pandas as pd
from time import strftime
import datetime
import Clerk
import Supervisor
import Admin
import Mayor

try:
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()

    gauth.SaveCredentialsFile("credentials.json")

except:
    print("Network connection failed")
    exit()

drive = GoogleDrive(gauth)

system_specs_df = pd.read_csv('system_specs.csv')
database_folder = ''

if len(system_specs_df.index) == 0:
    for folder in drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList():
        if folder['title'] == "RRTS": database_folder = folder['id']
    if database_folder == '': 
        print("System set-up required")
        exit()
    for file in drive.ListFile({'q': "'"+database_folder+"' in parents and trashed=false"}).GetList():
        if file['title'] == "System Specs.csv": 
            file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': file['id']})
            file_obj.GetContentFile(filename='system_specs.csv')
            system_specs_df = pd.read_csv('system_specs.csv')
            break

else: 
    database_folder = system_specs_df['Folder'][0]

links_file = system_specs_df['Links_file'][0]
try:
    links_df = pd.read_csv('https://drive.google.com/uc?id='+links_file)
except:
    print("Network connection failed")
    exit()

database_file = {}
for i in range(len(links_df.index)):
    database_file[links_df['File'][i]] = links_df['Link'][i]

Database = (drive,database_folder,database_file)

try:
    file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': database_file["Login Info"]})
    file_obj.GetContentFile(filename='temp.csv')
    login_info_df=pd.read_csv('temp.csv')
except:
    print("Network connection failed")
    exit()

# Get today's date
today = datetime.date.today()

# Get the day of the week
day_of_week = today.strftime("%A")

# Get the month
month = today.strftime("%B")

# Get the day of the month
day_of_month = today.strftime("%d")

# Get the year
year = today.strftime("%Y")

def update_time1():
    #Updates the label's text with the current time.
    string_time = strftime('%H:%M:%S %p')
    clock_label1.config(text=string_time)
    window.after(1000, update_time1)

def update_time2():
    #Updates the label's text with the current time.
    string_time = strftime('%H:%M:%S %p')
    clock_label2.config(text=string_time)
    window.after(1000, update_time2)


window = Tk()
window.rowconfigure(0, weight=1)
window.columnconfigure(0, weight=1)
window.state('zoomed')
window.resizable(0, 0)
window.title('Road Repair and Tracking Software')
photo = PhotoImage(file = "Images/icon.png")
window.iconphoto(True, photo)


LoginPage = Frame(window)
SignupPage = Frame(window)

for frame in (LoginPage, SignupPage):
    frame.grid(row=0, column=0, sticky='nsew')

def show_page(frame):
    frame.tkraise()

#login page 
    
login_listbox1 = Listbox(LoginPage, bg="white", width=window.winfo_screenwidth(), height=window.winfo_screenheight(), highlightthickness=0, borderwidth=0)
login_listbox1.place(x=0,y=0)

side_bar1 = Frame(LoginPage, bg="#5cdb95", height=window.winfo_screenheight(), width=int(window.winfo_screenwidth()*0.2), highlightthickness=0, borderwidth=0)
side_bar1.place(x=0,y=0)

central_frame1 = Frame(LoginPage, bg="white", height=window.winfo_screenheight(), width=window.winfo_screenwidth()*0.8)
central_frame1.place(x=window.winfo_screenwidth()*0.2, y=0)

logo_img=Image.open('Images/logo.png')
logo_pic=ImageTk.PhotoImage(logo_img)

bg_label1 = Label(side_bar1, image=logo_pic, bg="#5cdb95")
bg_label1.image=logo_pic
bg_label1.place(x=side_bar1.winfo_screenwidth()*0.005, y=side_bar1.winfo_screenheight()*0.1)

login_box1 = Listbox(central_frame1, bg="#05386B", width=int(window.winfo_screenwidth()*0.08), height=int(window.winfo_screenheight()*0.04), highlightthickness=2, borderwidth=0, highlightbackground="#05386B", highlightcolor="#05386B")
login_box1.place(x=central_frame1.winfo_screenwidth()*0.17, y=central_frame1.winfo_screenheight()*0.19)

def switch_to_login():
    name_entry1.delete(0,END)
    type_variable.set(type_options[0])
    email_entry2.delete(0,END)
    password_entry2.delete(0,END)
    show_pass2_var.set(0)
    password_entry2.config(show='•')
    locality_variable.set(locality_options[0])
    confirm_password_entry2.delete(0,END)
    show_conf_pass2_var.set(0)
    confirm_password_entry2.config(show='•')
    head.config(text="")
    condition1.config(text="")
    condition2.config(text="")
    condition3.config(text="")
    condition4.config(text="")
    condition5.config(text="")
    condition6.config(text="")
    show_page(LoginPage)

login_button1 = Button(login_box1, command=switch_to_login, fg="#5cdb95", bg="#05386B", text="Log In", font=("yu gothic ui bold", 17), borderwidth=0, cursor='hand2', activebackground="#05386B", activeforeground="#5cdb95", width=int(login_box1.winfo_screenwidth()*0.0185))
login_button1.place(x=0, y=0)

def switch_to_signup():
    error_label1.config(text="")
    email_entry1.delete(0, END)
    password_entry1.delete(0, END)
    show_pass_var.set(0)
    password_entry1.config(show='•')
    show_page(SignupPage)

signup_button1 = Button(login_box1, command=switch_to_signup, fg="#8ee4af", bg="black", text="Sign Up", font=("yu gothic ui bold", 17), borderwidth=0, cursor='hand2', activebackground="#05386B", activeforeground="#5cdb95", width=int(login_box1.winfo_screenwidth()*0.0185))
signup_button1.place(x=login_box1.winfo_screenwidth()*0.235, y=0)

welcome_label1 = Label(login_box1, fg="#5cdb95", bg="#05386B", font=("yu gothic ui bold", 30), text="Welcome")
welcome_label1.place(x=login_box1.winfo_screenwidth()*0.17, y=login_box1.winfo_screenheight()*0.069)

clock_icon1 = Image.open('Images/time.png')
clock_pic = ImageTk.PhotoImage(clock_icon1)
clock_icon_label1 = Label(login_box1, image=clock_pic, bg='#05386B')
clock_icon_label1.image = clock_pic
clock_icon_label1.place(x=login_box1.winfo_screenwidth()*0.025, y=login_box1.winfo_screenheight()*0.195)

clock_label1 = Label(login_box1, font=('calibri', 15, 'bold'), background='#05386B', foreground='white')
clock_label1.place(x=login_box1.winfo_screenwidth()*0.05, y=login_box1.winfo_screenheight()*0.2)
update_time1()

date_icon1 = Image.open('Images/date.png')
date_pic = ImageTk.PhotoImage(date_icon1)
date_icon_label1 = Label(login_box1, image=date_pic, bg='#05386B')
date_icon_label1.image = date_pic
date_icon_label1.place(x=login_box1.winfo_screenwidth()*0.025, y=login_box1.winfo_screenheight()*0.27)

date_label1 = Label(login_box1, text=day_of_week+" \n"+month+" "+day_of_month+" \n"+year, fg="white", bg="#05386B", font=('calibri', 15, 'bold'))
date_label1.place(x=login_box1.winfo_screenwidth()*0.055, y=login_box1.winfo_screenheight()*0.275)

email_icon1 = Image.open('Images/email.png')
email_pic = ImageTk.PhotoImage(email_icon1)
emailIcon_label1 = Label(login_box1, image=email_pic, bg='#05386B')
emailIcon_label1.image = email_pic
emailIcon_label1.place(x=login_box1.winfo_screenwidth()*0.195, y=login_box1.winfo_screenheight()*0.195)

email_entry1 = Entry(login_box1, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(login_box1.winfo_screenwidth()*0.02), highlightcolor="white")
email_entry1.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.2)
email_label1 = Label(login_box1, text="• Email Id", fg="white", bg="#05386B", font=("yu gothic ui", 15, "bold"))
email_label1.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.16)

password_icon1 = Image.open('Images/password.png')
password_pic = ImageTk.PhotoImage(password_icon1)
password_icon_label1 = Label(login_box1, image=password_pic, bg='#05386B')
password_icon_label1.image = password_pic
password_icon_label1.place(x=login_box1.winfo_screenwidth()*0.195, y=login_box1.winfo_screenheight()*0.32)

password_entry1 = Entry(login_box1, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2, width=int(login_box1.winfo_screenwidth()*0.02), highlightcolor="white")
password_entry1.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.325)
password_label1 = Label(login_box1, text="• Password", fg="white", bg="#05386B", font=("yu gothic ui", 15, "bold"))
password_label1.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.285)

# function for show and hide password
def password_command():
    if password_entry1.cget('show') == '•':
        password_entry1.config(show='')
    else:
        password_entry1.config(show='•')

show_pass_var = IntVar(value=0)
show_password = Checkbutton(login_box1, bg='#05386B', command=password_command, text='show password', variable=show_pass_var, onvalue=1, offvalue=0, fg="white", activebackground="#1f2833", activeforeground="#5cdb95", selectcolor="#05386B")
show_password.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.37)

error_label1=Label(login_box1, text="", fg="red", bg="#05386B", font=("yu gothic ui", 11, 'bold'))
error_label1.place(x=login_box1.winfo_screenwidth()*0.225, y=login_box1.winfo_screenheight()*0.4)

def encrypt(password):
    mod1 = 0
    mod2 = 0
    mod3 = 0
    for i in range(len(password)):
        mod1 = (mod1*97 + ord(password[i]) - 31) % (17)
        mod2 = (mod2*97 + ord(password[i]) - 31) % int(1e9+7)
        mod3 = (mod3*97 + ord(password[i]) - 31) % int((1e18+1)/(1e6+1))
    return str(hex(mod1)) + str(hex(mod2)) + str(hex(mod3))

# On pressing Login
def loginUser():
    error_label1.config(text="")
    email=email_entry1.get().lower()
    password=password_entry1.get()
    global login_info_df
    idx=login_info_df[login_info_df['Email Id'] == email]
    if len(idx)>0 and encrypt(password)==login_info_df['Password'][idx.index[0]]:
        if login_info_df['Authorized'][idx.index[0]]=='N':
            error_label1.config(text="Authorization Pending.\nPlease wait.")
        else:
            userType=login_info_df['Type'][idx.index[0]]
            userLocality=login_info_df['Locality'][idx.index[0]]
            email_entry1.delete(0, END)
            password_entry1.delete(0, END)
            show_pass_var.set(0)
            password_entry1.config(show='•')
            if userType=="Clerk":
                Clerk.clerk_page(window,Database,userLocality)
            elif userType=="Supervisor":
                Supervisor.supervisor_page(window,Database,userLocality)
            elif userType=="Admin":
                Admin.admin_page(window,Database,login_info_df)
                if os.path.exists('temp.csv'): login_info_df=pd.read_csv('temp.csv')
            else:
                Mayor.mayor_page(window,Database,locality_options)
    else:
        error_label1.config(text="Incorrect Email-Id or Password.")

login_button_down=Button(login_box1, text="Log In", bg="white", fg="#05386B", font=("yu gothic ui bold", 17), cursor="hand2", activebackground="white", activeforeground="#05386B", borderwidth=0, width=int(login_box1.winfo_screenwidth()*0.01), command=loginUser)
login_button_down.place(x=login_box1.winfo_screenwidth()*0.245, y=login_box1.winfo_screenheight()*0.45)

partition_frame1=Frame(login_box1, bg="white", width=int(login_box1.winfo_screenwidth()*0.0025), height=int(login_box1.winfo_screenheight()*0.35))
partition_frame1.place(x=login_box1.winfo_screenwidth()*0.165, y=login_box1.winfo_screenheight()*0.15)

#sign up page

login_listbox2=Listbox(SignupPage, bg="white", width=window.winfo_screenwidth(), height=window.winfo_screenheight(), highlightthickness=0, borderwidth=0)
login_listbox2.place(x=0,y=0)

side_bar2=Frame(SignupPage, bg="#5cdb95", height=window.winfo_screenheight(), width=int(window.winfo_screenwidth()*0.2), highlightthickness=0, borderwidth=0)
side_bar2.place(x=0,y=0)

central_frame2=Frame(SignupPage, bg="white", height=window.winfo_screenheight(), width=window.winfo_screenwidth()*0.8)
central_frame2.place(x=window.winfo_screenwidth()*0.2, y=0)

bg_label2 = Label(side_bar2, image=logo_pic, bg="#5cdb95")
bg_label2.image=logo_pic
bg_label2.place(x=side_bar2.winfo_screenwidth()*0.005, y=side_bar2.winfo_screenheight()*0.1)

login_box2=Listbox(central_frame2, bg="#05386B", width=int(window.winfo_screenwidth()*0.08), height=int(window.winfo_screenheight()*0.04), highlightthickness=2, borderwidth=0, highlightbackground="#05386B", highlightcolor="#05386B")
login_box2.place(x=central_frame2.winfo_screenwidth()*0.17, y=central_frame2.winfo_screenheight()*0.19)

login_button2=Button(login_box2, command=switch_to_login, fg="#8ee4af", bg="black", text="Log In", font=("yu gothic ui bold", 17), borderwidth=0, cursor='hand2', activebackground="#05386B", activeforeground="#5cdb95", width=int(login_box2.winfo_screenwidth()*0.0185))
login_button2.place(x=0, y=0)

signup_button2=Button(login_box2, command=switch_to_signup, fg="#5cdb95", bg="#05386B", text="Sign Up", font=("yu gothic ui bold", 17), borderwidth=0, cursor='hand2', activebackground="#05386B", activeforeground="#5cdb95", width=int(login_box2.winfo_screenwidth()*0.0185))
signup_button2.place(x=login_box2.winfo_screenwidth()*0.235, y=0)

clock_pic = ImageTk.PhotoImage(clock_icon1)
clock_icon_label2 = Label(login_box2, image=clock_pic, bg='#05386B')
clock_icon_label2.image = clock_pic
clock_icon_label2.place(x=login_box2.winfo_screenwidth()*0.025, y=login_box2.winfo_screenheight()*0.095)

clock_label2 = Label(login_box2, font=('calibri', 15, 'bold'), background='#05386B', foreground='white')
clock_label2.place(x=login_box2.winfo_screenwidth()*0.05, y=login_box2.winfo_screenheight()*0.1)
update_time2()

date_pic = ImageTk.PhotoImage(date_icon1)
date_icon_label2 = Label(login_box2, image=date_pic, bg='#05386B')
date_icon_label2.image = date_pic
date_icon_label2.place(x=login_box2.winfo_screenwidth()*0.025, y=login_box2.winfo_screenheight()*0.17)

date_label2=Label(login_box2, text=day_of_week+" \n"+month+" "+day_of_month+" \n"+year, fg="white", bg="#05386B", font=('calibri', 15, 'bold'))
date_label2.place(x=login_box2.winfo_screenwidth()*0.055, y=login_box2.winfo_screenheight()*0.175)

partition_frame2=Frame(login_box2, bg="white", width=int(login_box2.winfo_screenwidth()*0.0025), height=int(login_box2.winfo_screenheight()*0.5))
partition_frame2.place(x=login_box2.winfo_screenwidth()*0.165, y=login_box2.winfo_screenheight()*0.075)

head=Label(login_box2, text='', fg="white", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
head.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.3)
condition1=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition1.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.325)
condition2=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition2.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.35)
condition3=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition3.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.375)
condition4=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition4.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.4)
condition5=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition5.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.425)
condition6=Label(login_box2, text='', fg="red", bg='#05386b', font=("yu gothic ui", 11, 'bold'))
condition6.place(x=login_box2.winfo_screenwidth()*0.015, y=login_box2.winfo_screenheight()*0.45)

#type, name, locality, password, email id, confirm pass
# Type
type_options=["Clerk", "Supervisor"]
type_variable = StringVar()
type_variable.set(type_options[0])
type_menu = OptionMenu(login_box2, type_variable, *type_options)
type_menu.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
tmenu=login_box2.nametowidget(type_menu.menuname)
tmenu.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
type_menu.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.10, width=int(login_box2.winfo_screenwidth()*0.18), height=35)
type_label = Label(login_box2, text='• Type of Account', fg="white", bg='#05386B', font=("yu gothic ui", 11, 'bold'))
type_label.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.07)

name_entry1=Entry(login_box2, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(login_box2.winfo_screenwidth()*0.02), highlightcolor="white")
name_entry1.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.17)
name_label1=Label(login_box2, text="• Name", fg="white", bg="#05386B", font=("yu gothic ui", 11, "bold"))
name_label1.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.14)

locality_options = [x for x in links_df['File'].to_list() if(x[:3]!="new" and x not in ["Schedule", "Resources", "Login Info"])]
locality_variable = StringVar()
locality_variable.set(locality_options[0])
locality_menu = OptionMenu(login_box2, locality_variable, *locality_options)
locality_menu.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
lmenu=login_box2.nametowidget(locality_menu.menuname)
lmenu.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
locality_menu.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.24, width=int(login_box2.winfo_screenwidth()*0.18), height=35)
locality_label = Label(login_box2, text='• Locality', fg="white", bg='#05386B', font=("yu gothic ui", 11, 'bold'))
locality_label.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.21)

emailId2=StringVar()

email_entry2=Entry(login_box2, text=(emailId2), fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(login_box2.winfo_screenwidth()*0.02), highlightcolor="white")
email_entry2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.31)
email_label2=Label(login_box2, text="• Email Id", fg="white", bg="#05386B", font=("yu gothic ui", 11, "bold"))
email_label2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.28)

# UserIdChecker
userIdValid=False

def userIdCheck(*args):
    str2=emailId2.get()
    condition1.config(text='')
    global userIdValid
    if re.match(r"^[a-zA-Z0-9_.]+@[a-zA-Z0-9_.]+\.[a-zA-Z]{2,}$", str2):
        userIdValid=True
    else:
        condition1.config(text='Invalid Email Id', fg="red")
        userIdValid=False
    if userIdValid:
        if str2 in login_info_df['Email Id'].to_list():
            condition1.config(text='Email Id Already In Use', fg="red")
            userIdValid=False
        else:
            condition1.config(text='')


def userIdActive():
    head.config(text='')
    condition1.config(text='')
    condition2.config(text='')
    condition3.config(text='')
    condition4.config(text='')
    condition5.config(text='')
    condition6.config(text='')
    emailId2.trace('w', userIdCheck)

def userIdInactive():
    condition1.config(text='')
    

email_entry2.bind('<Enter>', lambda event: userIdActive())
email_entry2.bind('<Leave>', lambda event: userIdInactive())


password2=StringVar()

password_entry2=Entry(login_box2, text=(password2), fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2, width=int(login_box2.winfo_screenwidth()*0.02), highlightcolor="white")
password_entry2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.38)
password_label2=Label(login_box2, text="• Password", fg="white", bg="#05386B", font=("yu gothic ui", 11, "bold"))
password_label2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.35)


#password checker
req=[False, False, False, False, False, False]

def passwordCheck(*args):
    global req
    str1=password2.get()
    head.config(text='• Password must contain:')
    condition1.config(text='• More than 7 characters')
    condition4.config(text='• At least one number')
    condition3.config(text='• At least one lowercase letter')
    condition2.config(text='• At least one uppercase letter')
    condition5.config(text='• At least one special character')
    condition6.config(text='• No blank spaces')
    condition1.config(fg='red')
    condition2.config(fg='red')
    condition3.config(fg='red')
    condition4.config(fg='red')
    condition5.config(fg='red')
    condition6.config(fg='green')
    specialCharacter=list(('~','!','@','#','$','%','^','&','*','(',')','-','_','/'))
    req=[False, False, False, False, False, True]
    if len(str1)>7:
        condition1.config(fg='green')            
        req[0]=True
    for i in range(len(str1)):
        if str1[i]>='0' and str1[i]<='9':
            condition4.config(fg='green')            
            req[3]=True

        elif str1[i]>='a' and str1[i]<='z':
            condition3.config(fg='green')            
            req[2]=True

        elif str1[i]>='A' and str1[i]<='Z':
            condition2.config(fg='green')            
            req[1]=True

        elif str1[i] in specialCharacter:
            condition5.config(fg='green')            
            req[4]=True
        
        else:
            req[0]=False
            if str1[i]==' ': 
                condition6.config(fg='red')

    for j in range(5):
            if(req[j]==False):
                req[5]=False
                break


def passwordActive():
    head.config(text='')
    condition1.config(text='')
    condition2.config(text='')
    condition3.config(text='')
    condition4.config(text='')
    condition5.config(text='')
    condition6.config(text='')
    password2.trace('w', passwordCheck)

def passwordInactive():
    head.config(text='')
    condition1.config(text='')
    condition2.config(text='')
    condition3.config(text='')
    condition4.config(text='')
    condition5.config(text='')
    condition6.config(text='')


password_entry2.bind('<Enter>', lambda event: passwordActive())
password_entry2.bind('<Leave>', lambda event: passwordInactive())

# function for show and hide password
def password_command2():
    if password_entry2.cget('show') == '•':
        password_entry2.config(show='')
    else:
        password_entry2.config(show='•')

show_pass2_var = IntVar(value=0)
show_password2 = Checkbutton(login_box2, bg='#05386B', command=password_command2, text='show password', variable=show_pass2_var, onvalue=1, offvalue=0, fg="white", activebackground="#1f2833", activeforeground="#5cdb95", selectcolor="#05386B")
show_password2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.42)

confirm_password = StringVar()

confirm_password_entry2 = Entry(login_box2, text=(confirm_password), fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), show='•', highlightthickness=2, width=int(login_box2.winfo_screenwidth()*0.02), highlightcolor="white")
confirm_password_entry2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.48)
confirm_password_label2 = Label(login_box2, text="• Confirm Password", fg="white", bg="#05386B", font=("yu gothic ui", 11, "bold"))
confirm_password_label2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.45)

def confirmPasswordCheck(*args):
    condition1.config(text='Confirm Password must be \nsame as Password')
    condition1.config(fg='red')
    if confirm_password.get()==password1:
        condition1.config(fg='green')
    else:
        condition1.config(fg='red')

def confirmPasswordActive():
    head.config(text='')
    condition1.config(text='')
    condition2.config(text='')
    condition3.config(text='')
    condition4.config(text='')
    condition5.config(text='')
    condition6.config(text='')
    global password1
    password1=password2.get()
    confirm_password.trace('w', confirmPasswordCheck)

def confirmPasswordInactive():
    head.config(text='')
    condition1.config(text='')
    condition2.config(text='')
    condition3.config(text='')
    condition4.config(text='')
    condition5.config(text='')
    condition6.config(text='')


confirm_password_entry2.bind('<Enter>', lambda event: confirmPasswordActive())
confirm_password_entry2.bind('<Leave>', lambda event: confirmPasswordInactive())

# function for show and hide password
def confirm_password_command2():
    if confirm_password_entry2.cget('show') == '•':
        confirm_password_entry2.config(show='')
    else:
        confirm_password_entry2.config(show='•')

show_conf_pass2_var = IntVar(value=0)
show_confirm_password2 = Checkbutton(login_box2, bg='#05386B', command=confirm_password_command2, text='show password', variable=show_conf_pass2_var, onvalue=1, offvalue=0, fg="white", activebackground="#1f2833", activeforeground="#5cdb95", selectcolor="#05386B")
show_confirm_password2.place(x=login_box2.winfo_screenwidth()*0.225, y=login_box2.winfo_screenheight()*0.52)

def signUp():
    global login_info_df, userIdValid, req
    head.config(text="")
    condition1.config(text="")
    condition2.config(text="")
    condition3.config(text="")
    if not userIdValid:
        head.config(text="Error")
        condition1.config(text="• Invalid Email Id.", fg="red")
    if not req[5]:
        head.config(text="Error")
        condition2.config(text="• Invalid Password.", fg="red")
    if not name_entry1.get().replace(" ",""):
        head.config(text="Error")
        condition3.config(text="• Please provide a Name.", fg="red")
    if confirm_password.get()!=password1:
        head.config(text="Error")
        condition4.config(text="• Confirm Password not \nsame as Password.", fg="red")
    if userIdValid and req[5] and confirm_password.get()==password1 and name_entry1.get().replace(" ",""):
        temp_dict=[{'Type': type_variable.get(), 'Name': name_entry1.get(), 'Locality': locality_variable.get(), 'Email Id': emailId2.get().lower(), 'Password': encrypt(password2.get()), 'Authorized': 'N'}]
        temp_df=pd.DataFrame(temp_dict)
        login_info_df=pd.concat([login_info_df,temp_df], ignore_index=True)
        login_info_df.to_csv('temp.csv', index=False)
        file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': database_file['Login Info']})
        file_obj.SetContentFile(filename='temp.csv')
        file_obj.Upload()
        name_entry1.delete(0,END)
        type_variable.set(type_options[0])
        email_entry2.delete(0,END)
        password_entry2.delete(0,END)
        show_pass2_var.set(0)
        password_entry2.config(show='•')
        locality_variable.set(locality_options[0])
        confirm_password_entry2.delete(0,END)
        show_conf_pass2_var.set(0)
        confirm_password_entry2.config(show='•')
        head.config(text="Account details sent\nto Admin for\nAuthorization.\nPlease wait.")
        condition1.config(text="")
        condition2.config(text="")
        condition3.config(text="")
        condition4.config(text="")
        condition5.config(text="")
        condition6.config(text="")
        


signup_button_down=Button(login_box2, text="Sign Up", bg="white", fg="#05386B", font=("yu gothic ui bold", 17), cursor="hand2", activebackground="white", activeforeground="#05386B", borderwidth=0, width=int(login_box2.winfo_screenwidth()*0.01), command=signUp)
signup_button_down.place(x=login_box2.winfo_screenwidth()*0.25, y=login_box2.winfo_screenheight()*0.56)

show_page(LoginPage)

window.mainloop()

if os.path.exists('temp.csv'): os.remove('temp.csv')
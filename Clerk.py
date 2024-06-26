from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image  # type "Pip install pillow" in your terminal to install ImageTk and Image module
import pandas as pd
from datetime import date

def clerk_page(window, Database, locality):

    window.overrideredirect(True)

    new_complaints_df = pd.DataFrame(columns=['Locality','Street','Problem','Reporting Date'])

    logo_img=Image.open('Images/logo_s.png')
    logo_pic=ImageTk.PhotoImage(logo_img)

    logout_img=Image.open('Images/logout.png')
    logout_pic=ImageTk.PhotoImage(logout_img)

    refresh_img=Image.open('Images/refresh.png')
    refresh_pic=ImageTk.PhotoImage(refresh_img)

    clerk_frame=Frame(window)
    clerk_frame.grid(row=0, column=0, sticky='nsew')

    header1=Listbox(clerk_frame, bg="#5cdb95", width=clerk_frame.winfo_screenwidth(), height=int(clerk_frame.winfo_screenheight()*0.01), borderwidth=0, highlightthickness=0)
    header1.place(x=0,y=0)

    title1=Label(header1, image=logo_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui bold", 30))
    title1.image=logo_pic
    title1.place(x=header1.winfo_screenwidth()*0.45, y=header1.winfo_screenheight()*0.001)

    def refresh():
        nonlocal new_complaints_df
        if len(new_complaints_df.index)>0:
            try:
                new_complaints_df = pd.concat([pd.read_csv('https://drive.google.com/uc?id='+Database[2]["new "+locality]),new_complaints_df], ignore_index=True)
                new_complaints_df.to_csv('temp.csv', index=False)
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]['new '+locality]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()
                new_complaints_df.drop(new_complaints_df.index.to_list(), axis=0, inplace=True)
            except:
                messagebox.showerror("Network Connection Failed", "Error while sending data")
                return

    refresh_button=Button(header1, text="Sync-changes  ", image=refresh_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=refresh)
    refresh_button.image=refresh_pic
    refresh_button.place(x=header1.winfo_screenwidth()*0.75, y=header1.winfo_screenheight()*0.01)

    def exit():
        nonlocal new_complaints_df
        if len(new_complaints_df.index)>0:
            try:
                new_complaints_df = pd.concat([pd.read_csv('https://drive.google.com/uc?id='+Database[2]["new "+locality]),new_complaints_df], ignore_index=True)
                new_complaints_df.to_csv('temp.csv', index=False)
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]['new '+locality]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()
            except:
                confirm=messagebox.askokcancel("Network Connection Failed", "Log out while offline?\nAny changes made will not be saved", icon='warning')
                if not confirm: return
        clerk_frame.destroy()
        window.overrideredirect(False)

    logout_button1=Button(header1, text="Logout  ", image=logout_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=exit)
    logout_button1.image=logout_pic
    logout_button1.place(x=header1.winfo_screenwidth()*0.9, y=header1.winfo_screenheight()*0.01)

    centre1 = Listbox(clerk_frame, bg="white", width=clerk_frame.winfo_screenwidth(), height=int(clerk_frame.winfo_screenheight()), borderwidth=0, highlightthickness=0)
    centre1.place(x=0,y=clerk_frame.winfo_screenheight()*0.1)

    form_box = Frame(centre1, bg="#05386B", borderwidth=0, highlightthickness=0, width=int(clerk_frame.winfo_screenwidth()*0.7), height=int(clerk_frame.winfo_screenheight()*0.7))
    form_box.place(x=clerk_frame.winfo_screenwidth()*0.15, y=clerk_frame.winfo_screenheight()*0.1)

    complaint_no_label = Label(form_box, text="New Complaint Form", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 25))
    complaint_no_label.place(x=form_box.winfo_screenwidth()*0.24, y=form_box.winfo_screenheight()*0.01)

    locality_title = Label(form_box, text="Locality:", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20))
    locality_title.place(x=form_box.winfo_screenwidth()*0.1, y=form_box.winfo_screenheight()*0.125)
    locality_label = Label(form_box, text=locality, bg="#05386b", fg="white", font=("yu gothic ui", 20))
    locality_label.place(x=form_box.winfo_screenwidth()*0.19, y=form_box.winfo_screenheight()*0.125)

    street_title = Label(form_box, text="Street:", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20))
    street_title.place(x=form_box.winfo_screenwidth()*0.1, y=form_box.winfo_screenheight()*0.3)
    street_entry = Entry(form_box, bg="#05386b", fg="white", font=("yu gothic ui", 20), width=int(form_box.winfo_screenwidth()*0.01), highlightthickness=2, highlightcolor="white")
    street_entry.place(x=form_box.winfo_screenwidth()*0.19, y=form_box.winfo_screenheight()*0.3)

    system_specs_df = pd.read_csv('system_specs.csv')
    problem_title = Label(form_box, text="Problem: ", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20))
    problem_title.place(x=form_box.winfo_screenwidth()*0.4, y=form_box.winfo_screenheight()*0.3)
    problem_options = system_specs_df['Problem_options'][0].split(':')
    problem_variable = StringVar()
    problem_variable.set(problem_options[0])
    problem_menu = OptionMenu(form_box, problem_variable, *problem_options)
    problem_menu.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 17), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    pmenu=form_box.nametowidget(problem_menu.menuname)
    pmenu.config(bg='#05386B', font=("yu gothic ui semibold", 17), fg="white", activebackground="black", activeforeground="white")
    problem_menu.place(x=form_box.winfo_screenwidth()*0.49, y=form_box.winfo_screenheight()*0.3, width=int(form_box.winfo_screenwidth()*0.175), height=int(form_box.winfo_screenheight()*0.05))

    reporting_date_text=Label(form_box, text="Reporting Date: ", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20))
    reporting_date_text.place(x=form_box.winfo_screenwidth()*0.35, y=form_box.winfo_screenheight()*0.125)
    reporting_date_label=Label(form_box, text=date.today().strftime("%d/%m/%Y"), bg="#05386b", fg="white", font=("yu gothic ui", 20))
    reporting_date_label.place(x=form_box.winfo_screenwidth()*0.49, y=form_box.winfo_screenheight()*0.125)

    error_label=Label(form_box, text="", bg="#05386b", fg="red", font=("yu gothic ui bold", 20))
    error_label.place(x=form_box.winfo_screenwidth()*0.265, y=form_box.winfo_screenheight()*0.6)

    def submit():
        if not street_entry.get().strip():
            error_label.config(text="Street field is empty.")
            return
        error_label.config(text="")
        temp_dict=[{'Locality': locality, 'Street': street_entry.get(), 'Problem': problem_variable.get(), 'Reporting Date': str(date.today())}]
        nonlocal new_complaints_df
        new_complaints_df=pd.concat([new_complaints_df, pd.DataFrame(temp_dict)], ignore_index=True)
        problem_variable.set(problem_options[0])
        street_entry.delete(0, END)

    submit_button=Button(form_box, text="Submit Complaint", bg="white", fg="#05386B", font=("yu gothic ui bold", 20), cursor="hand2", activebackground="white", activeforeground="#05386B", borderwidth=0, width=int(form_box.winfo_screenwidth()*0.0125), command=submit)
    submit_button.place(x=form_box.winfo_screenwidth()*0.25, y=form_box.winfo_screenheight()*0.475)

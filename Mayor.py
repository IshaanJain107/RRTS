from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image  # type "Pip install pillow" in your terminal to install ImageTk and Image module
import pandas as pd
pd.options.mode.chained_assignment = None
from datetime import *

def mayor_page(window,Database,locality_options):
    try:
        schedule_df=pd.read_csv('https://drive.google.com/uc?id='+Database[2]["Schedule"])
    except:
        messagebox.showerror("Network Connection Failed", "Error while fetching data")
        return
    completed_df=schedule_df[schedule_df['Status']=="Completed"]
    completed_df['Completion Date']=pd.to_datetime(completed_df['Completion Date'], format='%Y-%m-%d')

    system_specs_df = pd.read_csv('system_specs.csv')
    
    logo_img=Image.open('Images/logo_s.png')
    logo_pic=ImageTk.PhotoImage(logo_img)

    logout_img=Image.open('Images/logout.png')
    logout_pic=ImageTk.PhotoImage(logout_img)

    window.overrideredirect(True)

    mayor_frame=Frame(window)
    mayor_frame.grid(row=0, column=0, sticky='nsew')

    header1=Listbox(mayor_frame, bg="#5cdb95", width=mayor_frame.winfo_screenwidth(), height=int(mayor_frame.winfo_screenheight()*0.01), borderwidth=0, highlightthickness=0)
    header1.place(x=0,y=0)

    title1=Label(header1, image=logo_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui bold", 30))
    title1.image=logo_pic
    title1.place(x=header1.winfo_screenwidth()*0.45, y=header1.winfo_screenheight()*0.001)

    centre1=Listbox(mayor_frame, bg="white", width=mayor_frame.winfo_screenwidth(), height=int(mayor_frame.winfo_screenheight()), borderwidth=0, highlightthickness=0)
    centre1.place(x=0,y=mayor_frame.winfo_screenheight()*0.1)

    box1=Frame(centre1, bg="#05386B", borderwidth=0, highlightthickness=0, width=int(mayor_frame.winfo_screenwidth()*0.7), height=int(mayor_frame.winfo_screenheight()*0.7))
    box1.place(x=mayor_frame.winfo_screenwidth()*0.15, y=mayor_frame.winfo_screenheight()*0.1)

    report1=Frame(box1, bg="#05386b", width=box1.winfo_screenwidth(), height=int(box1.winfo_screenheight()*0.23), borderwidth=0, highlightthickness=0)
    report1.place(x=0,y=0)

    stat101=Label(report1, bg="#05386b", fg="white", text="No. of Repairs carried out from ", font=("yu gothic ui", 15))
    stat101.place(x=report1.winfo_screenwidth()*0.05, y=report1.winfo_screenheight()*0.05)

    def date1Active():
        stat103.config(text="(Dates in DD-MM-YYYY format)", fg='white')
    def date1Inactive():
        stat103.config(text="")

    from_date1=Entry(report1, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(report1.winfo_screenwidth()*0.01), highlightcolor="white")
    from_date1.place(x=report1.winfo_screenwidth()*0.245, y=report1.winfo_screenheight()*0.051)

    from_date1.bind('<Enter>', lambda event: date1Active())
    from_date1.bind('<Leave>', lambda event: date1Inactive())

    stat102=Label(report1, bg="#05386b", fg="white", text=" to ", font=("yu gothic ui", 15))
    stat102.place(x=report1.winfo_screenwidth()*0.34, y=report1.winfo_screenheight()*0.05)

    to_date1=Entry(report1, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(report1.winfo_screenwidth()*0.01), highlightcolor="white")
    to_date1.place(x=report1.winfo_screenwidth()*0.365, y=report1.winfo_screenheight()*0.051)

    to_date1.bind('<Enter>', lambda event: date1Active())
    to_date1.bind('<Leave>', lambda event: date1Inactive())

    stat103=Label(report1, bg="#05386b", fg="white", text="", font=("yu gothic ui", 15))
    stat103.place(x=report1.winfo_screenwidth()*0.47, y=report1.winfo_screenheight()*0.05)

    stat104=Label(report1, bg="#05386b", fg="white", text="Locality: ", font=("yu gothic ui", 15))
    stat104.place(x=report1.winfo_screenwidth()*0.05, y=report1.winfo_screenheight()*0.125)

    locality_variable1 = StringVar()
    locality_variable1.set("All")
    locality_menu1 = OptionMenu(report1, locality_variable1, "All", *locality_options)
    locality_menu1.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    lmenu1=report1.nametowidget(locality_menu1.menuname)
    lmenu1.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
    locality_menu1.place(x=report1.winfo_screenwidth()*0.115, y=report1.winfo_screenheight()*0.125, width=int(report1.winfo_screenwidth()*0.1), height=35)

    stat105=Label(report1, bg="#05386b", fg="white", text="Problem: ", font=("yu gothic ui", 15))
    stat105.place(x=report1.winfo_screenwidth()*0.25, y=report1.winfo_screenheight()*0.125)    

    problem_options=system_specs_df['Problem_options'][0].split(':')
    problem_variable1 = StringVar()
    problem_variable1.set("Any")
    problem_menu1 = OptionMenu(report1, problem_variable1, "Any", *problem_options)
    problem_menu1.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    pmenu1=report1.nametowidget(problem_menu1.menuname)
    pmenu1.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
    problem_menu1.place(x=report1.winfo_screenwidth()*0.325, y=report1.winfo_screenheight()*0.125, width=int(report1.winfo_screenwidth()*0.12), height=35)

    def getRepairs():
        nonlocal completed_df
        start_str=from_date1.get()
        end_str=to_date1.get()
        try:
            start_date = datetime.strptime(start_str, "%d-%m-%Y")
        except ValueError:
            stat103.config(text="Invalid Dates", fg='red')
            return
        try:
            end_date = datetime.strptime(end_str, "%d-%m-%Y")
        except ValueError:
            stat103.config(text="Invalid Dates", fg='red')
            return
        if (end_date-start_date).days < 0:
            stat103.config(text="Invalid Dates", fg='red')
            return
        
        local_completed_df=completed_df
        if locality_variable1.get() != "All": local_completed_df=local_completed_df[local_completed_df['Locality'] == locality_variable1.get()]
        if problem_variable1.get() != "Any": local_completed_df=local_completed_df[local_completed_df['Problem'] == problem_variable1.get()]
        completed_repairs=len(local_completed_df[(local_completed_df['Completion Date'] >= start_date) & (local_completed_df['Completion Date'] <= end_date)].index)
        stat106.config(text=completed_repairs)

    get_result_button1=Button(report1, bg="white", fg="#05386b", text="Get", font=("yu gothic ui", 12), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", width=int(report1.winfo_screenwidth()*0.005), command=getRepairs)
    get_result_button1.place(x=report1.winfo_screenwidth()*0.485, y=report1.winfo_screenheight()*0.125)

    stat106=Label(report1, bg="#05386b", fg="#5cdb95", text="", font=("yu gothic ui bold", 15), borderwidth=3, relief="ridge", width=int(report1.winfo_screenwidth()*0.005))
    stat106.place(x=report1.winfo_screenwidth()*0.55, y=report1.winfo_screenheight()*0.124)   

    report2=Frame(box1, bg="#05386b", width=box1.winfo_screenwidth(), height=int(box1.winfo_screenheight()*0.23), borderwidth=0, highlightthickness=0)
    report2.place(x=0,y=box1.winfo_screenheight()*0.23)

    separator_frame1=Frame(report2, bg="white", width=int(report2.winfo_screenwidth()*0.75), height=int(report2.winfo_screenheight()*0.001))
    separator_frame1.place(x=0, y=0)

    stat201=Label(report2, bg="#05386b", fg="white", text="No. of Resources utilised from ", font=("yu gothic ui", 15))
    stat201.place(x=report2.winfo_screenwidth()*0.05, y=report2.winfo_screenheight()*0.05)

    def date2Active():
        stat203.config(text="(Dates in DD-MM-YYYY format)", fg='white')
    def date2Inactive():
        stat203.config(text="")

    from_date2=Entry(report2, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(report1.winfo_screenwidth()*0.01), highlightcolor="white")
    from_date2.place(x=report2.winfo_screenwidth()*0.245, y=report2.winfo_screenheight()*0.051)

    from_date2.bind('<Enter>', lambda event: date2Active())
    from_date2.bind('<Leave>', lambda event: date2Inactive())

    stat202=Label(report2, bg="#05386b", fg="white", text=" to ", font=("yu gothic ui", 15))
    stat202.place(x=report2.winfo_screenwidth()*0.34, y=report2.winfo_screenheight()*0.05)

    to_date2=Entry(report2, fg="white", bg="#05386B", font=("yu gothic ui semibold", 12), highlightthickness=2, width=int(report1.winfo_screenwidth()*0.01), highlightcolor="white")
    to_date2.place(x=report2.winfo_screenwidth()*0.365, y=report2.winfo_screenheight()*0.051)

    to_date2.bind('<Enter>', lambda event: date2Active())
    to_date2.bind('<Leave>', lambda event: date2Inactive())

    stat203=Label(report2, bg="#05386b", fg="white", text="", font=("yu gothic ui", 15))
    stat203.place(x=report2.winfo_screenwidth()*0.47, y=report2.winfo_screenheight()*0.05)

    resource_name_dict={
        "All": ["All"],
        "Raw Materials": system_specs_df['Raw_Materials'][0].split(':'),
        "Machines": system_specs_df['Machines'][0].split(':'),
        "Personnel": system_specs_df['Personnel'][0].split(':')
    }
    def set_resource_names(type):
        menu = resource_name_menu1["menu"]
        menu.delete(0,"end")
        if type != "All": menu.add_command(label="All", command=lambda value="All": resource_name_variable1.set(value))
        for string in resource_name_dict[type]:
            menu.add_command(label=string, command=lambda value=string: resource_name_variable1.set(value))
        resource_name_variable1.set("All")

    stat204=Label(report2, bg="#05386b", fg="white", text="Resource Type: ", font=("yu gothic ui", 15))
    stat204.place(x=report2.winfo_screenwidth()*0.05, y=report2.winfo_screenheight()*0.125)

    resource_type_options=["All", "Raw Materials", "Personnel", "Machines"]
    resource_type_variable1 = StringVar()
    resource_type_variable1.set("All")
    resource_type_menu1 = OptionMenu(report2, resource_type_variable1, *resource_type_options, command=set_resource_names)
    resource_type_menu1.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    rtmenu1=report2.nametowidget(resource_type_menu1.menuname)
    rtmenu1.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
    resource_type_menu1.place(x=report2.winfo_screenwidth()*0.145, y=report2.winfo_screenheight()*0.125, width=int(report2.winfo_screenwidth()*0.1), height=35)

    stat205=Label(report2, bg="#05386b", fg="white", text="Resource Name: ", font=("yu gothic ui", 15))
    stat205.place(x=report2.winfo_screenwidth()*0.25, y=report2.winfo_screenheight()*0.125)    

    resource_name_variable1 = StringVar()
    resource_name_variable1.set("All")
    resource_name_menu1 = OptionMenu(report2, resource_name_variable1, "All")
    resource_name_menu1.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 12), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    rnmenu1=report2.nametowidget(resource_name_menu1.menuname)
    rnmenu1.config(bg='#05386B', font=("yu gothic ui semibold", 12), fg="white", activebackground="black", activeforeground="white")
    resource_name_menu1.place(x=report2.winfo_screenwidth()*0.35, y=report2.winfo_screenheight()*0.125, width=int(report2.winfo_screenwidth()*0.12), height=35)

    def getResourceUtil():
        nonlocal completed_df
        start_str=from_date2.get()
        end_str=to_date2.get()
        try:
            start_date = datetime.strptime(start_str, "%d-%m-%Y")
        except ValueError:
            stat203.config(text="Invalid Dates", fg='red')
            return
        try:
            end_date = datetime.strptime(end_str, "%d-%m-%Y")
        except ValueError:
            stat203.config(text="Invalid Dates", fg='red')
            return
        if (end_date-start_date).days < 0:
            stat203.config(text="Invalid Dates", fg='red')
            return
        
        local_completed_df = completed_df[(completed_df['Completion Date'] >= start_date) & (completed_df['Completion Date'] <= end_date)]
        if resource_type_variable1.get() == "All": resources_utilized = sum([local_completed_df[x].sum() for x in resource_name_dict["Raw Materials"]+resource_name_dict["Machines"]+resource_name_dict["Personnel"]])
        elif resource_name_variable1.get() == "All": resources_utilized = sum([local_completed_df[x].sum() for x in resource_name_dict[resource_type_variable1.get()]])
        else: resources_utilized = local_completed_df[resource_name_variable1.get()].sum()
        stat205.config(text=resources_utilized)

    get_result_button2=Button(report2, bg="white", fg="#05386b", text="Get", font=("yu gothic ui", 12), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", width=int(report2.winfo_screenwidth()*0.005), command=getResourceUtil)
    get_result_button2.place(x=report2.winfo_screenwidth()*0.485, y=report2.winfo_screenheight()*0.125)

    stat205=Label(report2, bg="#05386b", fg="#5cdb95", text="", font=("yu gothic ui bold", 15), borderwidth=3, relief="ridge", width=int(report2.winfo_screenwidth()*0.005))
    stat205.place(x=report2.winfo_screenwidth()*0.55, y=report2.winfo_screenheight()*0.124)   


    report3=Frame(box1, bg="#05386b", width=box1.winfo_screenwidth(), height=int(box1.winfo_screenheight()*0.23), borderwidth=0, highlightthickness=0)
    report3.place(x=0,y=box1.winfo_screenheight()*0.46)

    separator_frame2=Frame(report3, bg="white", width=int(report3.winfo_screenwidth()*0.75), height=int(report3.winfo_screenheight()*0.001))
    separator_frame2.place(x=0, y=0)

    pending_repairs=len(schedule_df[schedule_df['Status']=="Pending"].index)
    in_progress_repairs=len(schedule_df[schedule_df['Status']=="In Progress"].index)

    stat301=Label(report3, bg="#05386b", fg="white", text="No. of currently outstanding Repairs: ", font=("yu gothic ui", 15))
    stat301.place(x=report3.winfo_screenwidth()*0.05, y=report3.winfo_screenheight()*0.05)

    stat302=Label(report3, bg="#05386b", fg="white", text="Pending: ", font=("yu gothic ui", 15))
    stat302.place(x=report3.winfo_screenwidth()*0.05, y=report3.winfo_screenheight()*0.125)

    stat303=Label(report3, bg="#05386b", fg="#5cdb95", text=pending_repairs, font=("yu gothic ui bold", 15), borderwidth=3, relief="ridge", width=int(report3.winfo_screenwidth()*0.008))
    stat303.place(x=report3.winfo_screenwidth()*0.13, y=report3.winfo_screenheight()*0.124)

    stat304=Label(report3, bg="#05386b", fg="white", text="In Progress: ", font=("yu gothic ui", 15))
    stat304.place(x=report3.winfo_screenwidth()*0.3, y=report3.winfo_screenheight()*0.125)    

    stat305=Label(report3, bg="#05386b", fg="#5cdb95", text=in_progress_repairs, font=("yu gothic ui bold", 15), borderwidth=3, relief="ridge", width=int(report3.winfo_screenwidth()*0.008))
    stat305.place(x=report3.winfo_screenwidth()*0.4, y=report3.winfo_screenheight()*0.124)

    def exit():
        mayor_frame.destroy()
        window.overrideredirect(False)

    logout_button1=Button(header1, text="Log Out  ", image=logout_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=exit)
    logout_button1.image=logout_pic
    logout_button1.place(x=header1.winfo_screenwidth()*0.9, y=header1.winfo_screenheight()*0.01)
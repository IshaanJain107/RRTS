import pandas as pd
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image
import os
from functools import partial
from datetime import date

def admin_page(window, Database, login_info_df):
    try:
        resources_df=pd.read_csv('https://drive.google.com/uc?id='+Database[2]["Resources"])
    except:
        messagebox.showerror("Network Connection Failed", "Error while fetching data")
        return
    unauthorized_df=login_info_df[login_info_df['Authorized']=='N']
    authorized_df=login_info_df[login_info_df['Authorized']=='Y']
    login_info_df.drop(login_info_df[login_info_df['Authorized']!='-'].index, inplace=True)
    unauthorized_df.reset_index(inplace=True, drop=True)
    authorized_df.reset_index(inplace=True, drop=True)
    unauthorized_df=pd.concat([unauthorized_df,authorized_df], ignore_index=True)

    resources_updated=False
    login_info_updated=False

    resource_check_frame=Frame(window)
    resource_update_frame=Frame(window)
    authorization_frame=Frame(window)

    window.overrideredirect(True)

    for frame in (resource_check_frame, resource_update_frame, authorization_frame):
        frame.grid(row=0,column=0, sticky='nsew')

    def show_frame(frame):
        frame.tkraise()

    def exit():
        try:
            nonlocal resources_df, login_info_df, unauthorized_df, resources_updated, login_info_updated
            if resources_updated:
                resources_df.to_csv('temp.csv', index=False)
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]["Resources"]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()

            login_info_df = pd.concat([login_info_df,unauthorized_df], ignore_index=True)
            login_info_df.to_csv('temp.csv', index=False)
            if login_info_updated:
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]["Login Info"]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()
            
        except:
            file_obj.content.close()
            confirm=messagebox.askokcancel("Network Connection Failed", "Log out while offline?\nAny changes made will not be saved", icon='warning')
            if os.path.exists('temp.csv'): os.remove('temp.csv')
            if not confirm: return

        resource_check_frame.destroy()
        resource_update_frame.destroy()
        authorization_frame.destroy()
        window.overrideredirect(False)

    def refresh():
        try:
            nonlocal resources_df, login_info_df, unauthorized_df, resources_updated, login_info_updated
            if resources_updated:
                resources_df.to_csv('temp.csv', index=False)
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]["Resources"]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()
                resources_updated = False

            if login_info_updated:
                upload_login_info_df = pd.concat([login_info_df,unauthorized_df], ignore_index=True)
                upload_login_info_df.to_csv('temp.csv', index=False)
                file_obj = Database[0].CreateFile({'parents': [{'id': Database[1]}], 'id': Database[2]["Login Info"]})
                file_obj.SetContentFile(filename='temp.csv')
                file_obj.Upload()
                login_info_updated = False
            
        except:
            file_obj.content.close()
            messagebox.showerror("Network Connection Failed", "Error while sending data")
            return

    logo_img=Image.open('Images/logo_s.png')
    logo_pic=ImageTk.PhotoImage(logo_img)

    logout_img=Image.open('Images/logout.png')
    logout_pic=ImageTk.PhotoImage(logout_img)

    refresh_img=Image.open('Images/refresh.png')
    refresh_pic=ImageTk.PhotoImage(refresh_img)

    header1=Listbox(resource_check_frame, bg="#5cdb95", width=resource_check_frame.winfo_screenwidth(), height=int(resource_check_frame.winfo_screenheight()*0.01), borderwidth=0, highlightthickness=0)
    header1.place(x=0,y=0)

    title1=Label(header1, image=logo_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui bold", 30))
    title1.image=logo_pic
    title1.place(x=header1.winfo_screenwidth()*0.45, y=header1.winfo_screenheight()*0.001)

    logout_button1=Button(header1, text="Logout  ", image=logout_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=exit)
    logout_button1.image=logout_pic
    logout_button1.place(x=header1.winfo_screenwidth()*0.9, y=header1.winfo_screenheight()*0.01)

    refresh_button1=Button(header1, text="Sync-changes  ", image=refresh_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=refresh)
    refresh_button1.image=refresh_pic
    refresh_button1.place(x=header1.winfo_screenwidth()*0.75, y=header1.winfo_screenheight()*0.01)

    resource_check_button1=Button(header1, text="Check Resources", bg="white", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b")
    resource_check_button1.place(x=header1.winfo_screenwidth()*0.01, y=header1.winfo_screenheight()*0.055)

    resource_update_button1=Button(header1, text="Update Resources", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(resource_update_frame))
    resource_update_button1.place(x=header1.winfo_screenwidth()*0.12, y=header1.winfo_screenheight()*0.055)

    authorization_button1=Button(header1, text="Authorize New Registrations", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(authorization_frame))
    authorization_button1.place(x=header1.winfo_screenwidth()*0.24, y=header1.winfo_screenheight()*0.055)

    centre1=Listbox(resource_check_frame, bg="white", width=resource_check_frame.winfo_screenwidth(), height=int(resource_check_frame.winfo_screenheight()), borderwidth=0, highlightthickness=0)
    centre1.place(x=0,y=resource_check_frame.winfo_screenheight()*0.1)

    box1=Frame(centre1, bg="#05386B", borderwidth=0, highlightthickness=0, width=int(resource_check_frame.winfo_screenwidth()*0.7), height=int(resource_check_frame.winfo_screenheight()*0.7))
    box1.place(x=resource_check_frame.winfo_screenwidth()*0.075, y=resource_check_frame.winfo_screenheight()*0.1)

    resource_list_var=[StringVar()]
    resource_list_var[0].set("Resource Type")
    resource_list_entry=[Entry(box1,textvariable=resource_list_var[0], bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="#5cdb95")]
    resource_list_entry[0].config(state='disabled')
    resource_list_entry[0].grid(row=1,column=0)
    type_list_var=[StringVar()]
    type_list_var[0].set("Resource Name")
    type_list_entry=[Entry(box1,textvariable=type_list_var[0], bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="#5cdb95")]
    type_list_entry[0].config(state='disabled')
    type_list_entry[0].grid(row=1,column=1)
    num_available_var=[StringVar()]
    num_available_var[0].set("Total Available")
    num_available_entry=[Entry(box1,textvariable=num_available_var[0], bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="#5cdb95")]
    num_available_entry[0].config(state='disabled')
    num_available_entry[0].grid(row=1,column=2)
    num_in_use_var=[StringVar()]
    num_in_use_var[0].set("In Use")
    num_in_use_entry=[Entry(box1,textvariable=num_in_use_var[0], bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="#5cdb95")]
    num_in_use_entry[0].config(state='disabled')
    num_in_use_entry[0].grid(row=1,column=3)
    for i in resources_df.index:
        resource_list_var.append(StringVar())
        resource_list_var[i+1].set(str(resources_df.iat[i,0]))
        resource_list_entry.append(Entry(box1,textvariable=resource_list_var[i+1], bg="#05386b", fg="white", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="white"))
        resource_list_entry[i+1].config(state='disabled')
        resource_list_entry[i+1].grid(row=i+2,column=0)
        type_list_var.append(StringVar())
        type_list_var[i+1].set(str(resources_df.iat[i,1]))
        type_list_entry.append(Entry(box1,textvariable=type_list_var[i+1], bg="#05386b", fg="white", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="white"))
        type_list_entry[i+1].config(state='disabled')
        type_list_entry[i+1].grid(row=i+2,column=1)
        num_available_var.append(StringVar())
        num_available_var[i+1].set(str(resources_df.iat[i,2]))
        num_available_entry.append(Entry(box1,textvariable=num_available_var[i+1], bg="#05386b", fg="white", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="white"))
        num_available_entry[i+1].config(state='disabled')
        num_available_entry[i+1].grid(row=i+2,column=2)
        num_in_use_var.append(StringVar())
        num_in_use_var[i+1].set(str(resources_df.iat[i,3]))
        num_in_use_entry.append(Entry(box1,textvariable=num_in_use_var[i+1], bg="#05386b", fg="white", font=("yu gothic ui bold", 20), disabledbackground="#05386b", disabledforeground="white"))
        num_in_use_entry[i+1].config(state='disabled')
        num_in_use_entry[i+1].grid(row=i+2,column=3)



    # resource update

    header2=Listbox(resource_update_frame, bg="#5cdb95", width=resource_check_frame.winfo_screenwidth(), height=int(resource_check_frame.winfo_screenheight()*0.01), borderwidth=0, highlightthickness=0)
    header2.place(x=0,y=0)

    title2=Label(header2, image=logo_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui bold", 30))
    title2.image=logo_pic
    title2.place(x=header2.winfo_screenwidth()*0.45, y=header2.winfo_screenheight()*0.001)

    logout_button2=Button(header2, text="Logout  ", image=logout_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=exit)
    logout_button2.image=logout_pic
    logout_button2.place(x=header2.winfo_screenwidth()*0.9, y=header2.winfo_screenheight()*0.01)

    refresh_button2=Button(header2, text="Sync-changes  ", image=refresh_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=refresh)
    refresh_button2.image=refresh_pic
    refresh_button2.place(x=header2.winfo_screenwidth()*0.75, y=header2.winfo_screenheight()*0.01)

    resource_check_button2=Button(header2, text="Check Resources", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(resource_check_frame))
    resource_check_button2.place(x=header2.winfo_screenwidth()*0.01, y=header2.winfo_screenheight()*0.055)

    resource_update_button2=Button(header2, text="Update Resources", bg="white", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b")
    resource_update_button2.place(x=header2.winfo_screenwidth()*0.12, y=header2.winfo_screenheight()*0.055)

    authorization_button2=Button(header2, text="Authorize New Registrations", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(authorization_frame))
    authorization_button2.place(x=header2.winfo_screenwidth()*0.24, y=header2.winfo_screenheight()*0.055)

    centre2=Listbox(resource_update_frame, bg="white", width=resource_update_frame.winfo_screenwidth(), height=int(resource_update_frame.winfo_screenheight()), borderwidth=0, highlightthickness=0)
    centre2.place(x=0,y=resource_update_frame.winfo_screenheight()*0.1)

    box2=Frame(centre2, bg="#05386B", borderwidth=0, highlightthickness=0, width=int(resource_update_frame.winfo_screenwidth()*0.7), height=int(resource_update_frame.winfo_screenheight()*0.7))
    box2.place(x=resource_update_frame.winfo_screenwidth()*0.15, y=resource_update_frame.winfo_screenheight()*0.1)

    system_specs_df = pd.read_csv('system_specs.csv')
    resource_name_dict={
        "Raw Materials": system_specs_df['Raw_Materials'][0].split(':'),
        "Machines": system_specs_df['Machines'][0].split(':'),
        "Personnel": system_specs_df['Personnel'][0].split(':')
    }

    def register_entries():
        nonlocal resources_updated
        resources_updated = True
        resources_df.iloc[((resources_df['Resource Type']==resource_type_variable.get()) & (resources_df['Name']==resource_name_variable.get())),2]=resource_count_variable.get()
        set_label.config(text=resource_name_variable.get()+" set to "+str(resource_count_variable.get()))
        resource_type_variable.set("[select]")
        resource_name_variable.set("[select]")
        resource_count_variable.set(0)

    def set_resource_names(type):
        menu = resource_name_menu["menu"]
        menu.delete(0,"end")
        for string in resource_name_dict[type]:
            menu.add_command(label=string, command=lambda value=string: resource_name_variable.set(value))
        resource_name_variable.set("[select]")
        set_label.config(text="")

    resource_type_label=Label(box2, bg="#05386b", fg="#5cdb95", text="Resource Type: ", font=("yu gothic ui", 20))
    resource_type_label.place(x=box2.winfo_screenwidth()*0.01, y=box2.winfo_screenheight()*0.125)

    resource_type_options=["Raw Materials", "Personnel", "Machines"]
    resource_type_variable = StringVar()
    resource_type_variable.set("[select]")
    resource_type_menu = OptionMenu(box2, resource_type_variable, *resource_type_options, command=set_resource_names)
    resource_type_menu.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 17), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    rtmenu=box2.nametowidget(resource_type_menu.menuname)
    rtmenu.config(bg='#05386B', font=("yu gothic ui semibold", 17), fg="white", activebackground="black", activeforeground="white")
    resource_type_menu.place(x=box2.winfo_screenwidth()*0.15, y=box2.winfo_screenheight()*0.125, width=int(box2.winfo_screenwidth()*0.2), height=int(box2.winfo_screenheight()*0.05))

    resource_name_label=Label(box2, bg="#05386b", fg="#5cdb95", text="Resource Name: ", font=("yu gothic ui", 20))
    resource_name_label.place(x=box2.winfo_screenwidth()*0.35, y=box2.winfo_screenheight()*0.125)    

    resource_name_variable = StringVar()
    resource_name_variable.set("[select]")
    resource_name_menu = OptionMenu(box2, resource_name_variable, "[select]")
    resource_name_menu.config(highlightbackground="#05386B", highlightcolor="white", font=("yu gothic ui semibold", 17), fg="white", bg='#05386B', activebackground="#05386B", activeforeground="white")
    rnmenu=box2.nametowidget(resource_name_menu.menuname)
    rnmenu.config(bg='#05386B', font=("yu gothic ui semibold", 17), fg="white", activebackground="black", activeforeground="white")
    resource_name_menu.place(x=box2.winfo_screenwidth()*0.49, y=box2.winfo_screenheight()*0.125, width=int(box2.winfo_screenwidth()*0.2), height=int(box2.winfo_screenheight()*0.05))    

    resource_count_variable=IntVar()
    resource_count_variable.set(0)
    resource_count_label=Label(box2, text="Enter the total number of units :", bg="#05386b", fg="#5cdb95", font=("yu gothic ui bold", 20))
    resource_count_label.place(x=box2.winfo_screenwidth()*0.075, y=box2.winfo_screenheight()*0.3)
    resource_count_entry=Entry(box2, textvariable=resource_count_variable, bg="#05386b", fg="white", font=("yu gothic ui", 20), width=int(box2.winfo_screenwidth()*0.01), highlightthickness=2, highlightcolor="white")
    resource_count_entry.place(x=box2.winfo_screenwidth()*0.375, y=box2.winfo_screenheight()*0.3)

    submit_button=Button(box2, text="Update Resource", bg="white", fg="#05386B", font=("yu gothic ui bold", 20), cursor="hand2", activebackground="white", activeforeground="#05386B", borderwidth=0, width=int(box2.winfo_screenwidth()*0.0125), command=register_entries)
    submit_button.place(x=box2.winfo_screenwidth()*0.25, y=box2.winfo_screenheight()*0.475)

    set_label=Label(box2, text="", bg="#05386b", fg="green", font=("yu gothic ui bold", 20))
    set_label.place(x=box2.winfo_screenwidth()*0.25, y=box2.winfo_screenheight()*0.55)

    # authorize

    header3=Listbox(authorization_frame, bg="#5cdb95", width=authorization_frame.winfo_screenwidth(), height=int(authorization_frame.winfo_screenheight()*0.01), borderwidth=0, highlightthickness=0)
    header3.place(x=0,y=0)

    title3=Label(header3, image=logo_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui bold", 30))
    title3.image=logo_pic
    title3.place(x=header3.winfo_screenwidth()*0.45, y=header3.winfo_screenheight()*0.001)

    logout_button3=Button(header3, text="Logout  ", image=logout_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=exit)
    logout_button3.image=logout_pic
    logout_button3.place(x=header3.winfo_screenwidth()*0.9, y=header3.winfo_screenheight()*0.01)

    refresh_button3=Button(header3, text="Sync-changes  ", image=refresh_pic, bg="#5cdb95", fg="#05386b", font=("yu gothic ui", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b", cursor="hand2", compound="right", command=refresh)
    refresh_button3.image=refresh_pic
    refresh_button3.place(x=header3.winfo_screenwidth()*0.75, y=header3.winfo_screenheight()*0.01)

    resource_check_button3=Button(header3, text="Check Resources", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(resource_check_frame))
    resource_check_button3.place(x=header3.winfo_screenwidth()*0.01, y=header3.winfo_screenheight()*0.055)

    resource_update_button3=Button(header3, text="Update Resources", bg="#5cdb95", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="white", activeforeground="#05386b", command=lambda: show_frame(resource_update_frame))
    resource_update_button3.place(x=header3.winfo_screenwidth()*0.12, y=header3.winfo_screenheight()*0.055)

    authorization_button3=Button(header3, text="Authorize New Registrations", bg="white", fg="#05386b", cursor="hand2", font=("yu gothic ui bold", 15), borderwidth=0, highlightthickness=0, activebackground="#5cdb95", activeforeground="#05386b")
    authorization_button3.place(x=header3.winfo_screenwidth()*0.24, y=header3.winfo_screenheight()*0.055)

    centre3=Listbox(authorization_frame, bg="white", width=authorization_frame.winfo_screenwidth(), height=int(authorization_frame.winfo_screenheight()), borderwidth=0, highlightthickness=0)
    centre3.place(x=0,y=authorization_frame.winfo_screenheight()*0.1)

    box3=Frame(centre3, bg="#05386B", borderwidth=0, highlightthickness=0, width=int(authorization_frame.winfo_screenwidth()*0.7), height=int(authorization_frame.winfo_screenheight()*0.7))
    box3.place(x=authorization_frame.winfo_screenwidth()*0.15, y=authorization_frame.winfo_screenheight()*0.1)

    authorization_canvas = Canvas(box3, width=int(box3.winfo_screenwidth()*0.697), height=int(box1.winfo_screenheight()*0.697), bg="#05386b")
    authorization_canvas.place(x=0,y=0)

    records = []

    def change_status(row):
        nonlocal unauthorized_df, login_info_updated
        login_info_updated = True
        if unauthorized_df['Authorized'][row]=="Y": unauthorized_df.at[row, 'Authorized'] = "N"
        elif unauthorized_df['Authorized'][row]=="N": unauthorized_df.at[row, 'Authorized'] = "Y"
        records[row].config(text=unauthorized_df['Locality'][row] + " | " + unauthorized_df['Type'][row] + " | " + unauthorized_df['Name'][row] + " | " + unauthorized_df['Email Id'][row] + " | Status: " + unauthorized_df['Authorized'][row])

    y = 0
    row_count=len(unauthorized_df.index)
    for row in range(row_count):
        records.append(Label(authorization_canvas, text=unauthorized_df['Locality'][row] + " | " + unauthorized_df['Type'][row] + " | " + unauthorized_df['Name'][row] + " | " + unauthorized_df['Email Id'][row] + " | Status: " + unauthorized_df['Authorized'][row], bg="#05386b", fg="white", font=("yu gothic ui", 15)))
        authorization_canvas.create_window(authorization_canvas.winfo_screenwidth()*0.01, y+2.5, window=records[row], anchor=NW)
        status_button=Button(authorization_canvas, text="Change Status", bg="#05386b", fg="white", command=partial(change_status, row), border=0, highlightthickness=0, activebackground="#05386b", activeforeground="#5cdb95", font=("yu gothic ui", 15))
        authorization_canvas.create_window(authorization_canvas.winfo_screenwidth()*0.55, y+2.5, window=status_button, anchor=NW)
        line_separator=Frame(authorization_canvas, width=int(authorization_canvas.winfo_screenheight()*1.1), height=2, bg="white")
        authorization_canvas.create_window(0, y+50, window=line_separator, anchor=NW)
        y += 60

    scrollbar = Scrollbar(authorization_canvas, orient=VERTICAL, command=authorization_canvas.yview)
    scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
    authorization_canvas.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))

    show_frame(resource_check_frame)

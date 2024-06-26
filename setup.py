from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd

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

for folder in drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList():
    if folder['title'] == "RRTS":
        print("Folder 'RRTS' already exists")
        exit()

system_specs_dict = {'Folder': '', 'Links_file': '', 'Problem_options': '', 'Raw_Materials': '', 'Machines': '', 'Personnel': ''}
links_dict = {
    'File': [],
    'Link': []
}

file_obj = drive.CreateFile({'title' : 'RRTS', 'mimeType' : 'application/vnd.google-apps.folder'})
file_obj.Upload()
file_obj.InsertPermission({'type': 'anyone', 'value': 'anyone', 'role': 'reader', 'withLink': True})
system_specs_dict['Folder'] = file_obj['id']

localities_list = []
num=int(input("Enter the number of localities: "))
print("Enter the names of the localities")
for i in range(num):
    localities_list.append(input())

num=int(input("Enter the number of types of road problems: "))
print("Enter the names of the types")
for i in range(num):
    if i==0: system_specs_dict['Problem_options']+=input()
    else: system_specs_dict['Problem_options']+=':'+input()

num=int(input("Enter the number of types of raw materials: "))
print("Enter the names of the types")
for i in range(num):
    if i==0: system_specs_dict['Raw_Materials']+=input()
    else: system_specs_dict['Raw_Materials']+=':'+input()

num=int(input("Enter the number of types of machines: "))
print("Enter the names of the types")
for i in range(num):
    if i==0: system_specs_dict['Machines']+=input()
    else: system_specs_dict['Machines']+=':'+input()

num=int(input("Enter the number of types of personnel: "))
print("Enter the names of the types")
for i in range(num):
    if i==0: system_specs_dict['Personnel']+=input()
    else: system_specs_dict['Personnel']+=':'+input()

login_info_dict = {
    'Type': ["Admin","Mayor"],
    'Name': ["City Admin","Mayor"],
    'Locality': ["-","-"],
    'Email Id': [],
    'Password': [],
    'Authorized': ["-","-"]
}
def encrypt(password):
    mod1 = 0
    mod2 = 0
    mod3 = 0
    for i in range(len(password)):
        mod1 = (mod1*97 + ord(password[i]) - 31) % (17)
        mod2 = (mod2*97 + ord(password[i]) - 31) % int(1e9+7)
        mod3 = (mod3*97 + ord(password[i]) - 31) % int((1e18+1)/(1e6+1))
    return str(hex(mod1)) + str(hex(mod2)) + str(hex(mod3))
email=input("Enter the Email Id of the City Admin: ")
login_info_dict['Email Id'].append(email)
password=input("Enter the Password of the City Admin: ")
login_info_dict['Password'].append(encrypt(password))
email=input("Enter the Email Id of the Mayor: ")
login_info_dict['Email Id'].append(email)
password=input("Enter the Password of the Mayor: ")
login_info_dict['Password'].append(encrypt(password))

login_info_df = pd.DataFrame(login_info_dict)
login_info_df.to_csv('temp.csv', index=False)
file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': 'Login Info.csv'})
file_obj.SetContentFile(filename='temp.csv')
file_obj.Upload()
file_obj.DeletePermission('anyoneWithLink')
links_dict['File'].append("Login Info")
links_dict['Link'].append(file_obj['id'])

resources_dict = {
    'Resource Type': [],
    'Name': [],
    'Units Available': [],
    'In Use': []
}
for resource in system_specs_dict['Raw_Materials'].split(':'):
    resources_dict['Resource Type'].append("Raw Materials")
    resources_dict['Name'].append(resource)
    resources_dict['Units Available'].append(0)
    resources_dict['In Use'].append(0)
for resource in system_specs_dict['Machines'].split(':'):
    resources_dict['Resource Type'].append("Machines")
    resources_dict['Name'].append(resource)
    resources_dict['Units Available'].append(0)
    resources_dict['In Use'].append(0)
for resource in system_specs_dict['Personnel'].split(':'):
    resources_dict['Resource Type'].append("Personnel")
    resources_dict['Name'].append(resource)
    resources_dict['Units Available'].append(0)
    resources_dict['In Use'].append(0)
resources_df = pd.DataFrame(resources_dict)
resources_df.to_csv('temp.csv', index=False)
file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': 'Resources.csv'})
file_obj.SetContentFile(filename='temp.csv')
file_obj.Upload()
links_dict['File'].append("Resources")
links_dict['Link'].append(file_obj['id'])

resources_list = system_specs_dict['Raw_Materials'].split(':') + system_specs_dict['Machines'].split(':') + system_specs_dict['Personnel'].split(':')
complaints_df = pd.DataFrame(columns=['Locality','Street','Problem','Reporting Date','Severity','Traffic']+resources_list+['Status','Completion Date'])
complaints_df.to_csv('temp.csv', index=False)
for locality in ["Schedule"]+localities_list:
    file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': locality+'.csv'})
    file_obj.SetContentFile(filename='temp.csv')
    file_obj.Upload()
    links_dict['File'].append(locality)
    links_dict['Link'].append(file_obj['id'])

new_complaints_df=pd.DataFrame(columns=['Locality','Street','Problem','Reporting Date'])
new_complaints_df.to_csv('temp.csv', index=False)
for locality in localities_list:
    file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': 'new '+locality+'.csv'})
    file_obj.SetContentFile(filename='temp.csv')
    file_obj.Upload()
    links_dict['File'].append("new "+locality)
    links_dict['Link'].append(file_obj['id'])

links_df = pd.DataFrame(links_dict)
links_df.to_csv('temp.csv', index=False)
file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': 'Links.csv'})
file_obj.SetContentFile(filename='temp.csv')
file_obj.Upload()
system_specs_dict['Links_file']=file_obj['id']

system_specs_df = pd.DataFrame([system_specs_dict])
system_specs_df.to_csv('temp.csv', index=False)
file_obj = drive.CreateFile({'parents': [{'id': system_specs_dict['Folder']}], 'title': 'System Specs.csv'})
file_obj.SetContentFile(filename='temp.csv')
file_obj.Upload()
file_obj.DeletePermission('anyoneWithLink')
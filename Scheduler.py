from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import pandas as pd
from time import *
from datetime import *
from functools import cmp_to_key

# get authorization
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

# retrieve database
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

localities_list = [x for x in links_df['File'].to_list() if(x[:3]!="new" and x not in ["Schedule", "Resources", "Login Info"])]

# map categories to values
severity_map = {"Critical": 3, "Severe": 2, "Moderate": 1, "Mild": 0}
traffic_map = {"Extreme": 4, "Heavy": 3, "Medium": 2, "Light": 1, "Deserted": 0}
system_specs_df = pd.read_csv('system_specs.csv')
resources_list = system_specs_df['Raw_Materials'][0].split(':') + system_specs_df['Machines'][0].split(':') + system_specs_df['Personnel'][0].split(':')

while True:
    current_date = date.today()
    current_time = datetime.now()

    # schedule tasks every 10 min (assuming 10 min day cycles)
    sleep((10 - current_time.minute % 10)*60 - current_time.second)

    # get complaints
    complaints_df = pd.DataFrame(columns=['Locality','Street','Problem','Reporting Date','Severity','Traffic']+resources_list+['Status','Completion Date'])
    try:
        for locality in localities_list:
            complaints_df = pd.concat([complaints_df,pd.read_csv('https://drive.google.com/uc?id='+database_file[locality])], ignore_index=True)
    except:
        print("Network connection failed")
        exit()

    # get resources
    try:
        resources_df = pd.read_csv('https://drive.google.com/uc?id='+database_file['Resources'])
    except:
        print("Network connection failed")
        exit()
    resources_available = {}
    resources_count = len(resources_df.index)
    for indx in range(resources_count):
        resources_available[resources_df['Name'][indx]] = resources_df['Units Available'][indx]

    # segregate pending and in-progress complaints
    pending_complaints_df = complaints_df[complaints_df['Status']=="Pending"]
    in_progress_tasks_df = complaints_df[complaints_df['Status']=="In Progress"]
    complaints_df.drop(complaints_df[complaints_df['Status']!="Completed"].index, inplace=True)
    pending_complaints_df.reset_index(inplace=True, drop=True)
    in_progress_tasks_df.reset_index(inplace=True, drop=True)


    # create a list of score-bin number and resource-requirement coefficient for pending complaints
    # score = 10*severity + 15*traffic + number of days elapsed since complaint was registered
    # score-bin number = score/10 (creating bins of size 10 for score)
    # resource-requirement coefficient = (total raw materials needed) + 10*(total personnel needed) + 100*(total machines needed)
    pending_scheduler_score = []
    pending_complaint_count = len(pending_complaints_df.index)
    for indx in range(pending_complaint_count):
        score = 10*severity_map[pending_complaints_df['Severity'][indx]] + 15*traffic_map[pending_complaints_df['Traffic'][indx]] + (current_date - datetime.strptime(pending_complaints_df['Reporting Date'][indx], '%Y-%m-%d').date()).days
        resources_req = 0
        for resource in system_specs_df['Raw_Materials'][0].split(':'):
            resources_req += pending_complaints_df[resource][indx]
        for resource in system_specs_df['Personnel'][0].split(':'):
            resources_req += 10 * pending_complaints_df[resource][indx]
        for resource in system_specs_df['Machines'][0].split(':'):
            resources_req += 100 * pending_complaints_df[resource][indx]
        pending_scheduler_score.append((int(score/10),indx,resources_req))

    # sort the list of pending complaints according to higher score-bin number and lower resource-requirement coefficients (for comparison within a bin)
    def compare(item1, item2):
        if item1[0] > item2[0]:
            return -1
        elif item1[0] < item2[0]:
            return 1
        else: 
            return item1[2] - item2[2]
    pending_scheduler_score = sorted(pending_scheduler_score, key=cmp_to_key(compare))

    # create a list of score-bin number for in-progress tasks and sort in descending order
    in_progress_scheduler_score = []
    in_progress_task_count = len(in_progress_tasks_df.index)
    for indx in range(in_progress_task_count):
        score = 10*severity_map[in_progress_tasks_df['Severity'][indx]] + 15*traffic_map[in_progress_tasks_df['Traffic'][indx]] + (datetime.strptime(in_progress_tasks_df['Completion Date'][indx], '%Y-%m-%d').date() - datetime.strptime(in_progress_tasks_df['Reporting Date'][indx], '%Y-%m-%d').date()).days
        in_progress_scheduler_score.append((int(score/10),indx))
    in_progress_scheduler_score.sort(reverse=True)

    # schedule the pending and in-progress tasks
    # iterate over all pending complaints
    # assign resources (if sufficient) to all in-progress tasks belonging to either the score-bin under consideration (to which the pending complaint belongs)
    #  or its next bin (if insufficient resources then mark it as pending complaint, remove completion date)
    # then assign resources (if sufficient) to the pending complaint under consideration
    # change status of pending complaint to in-progress and assign completion date as current date (start date)
    in_progress_index = 0
    for item in pending_scheduler_score:
        while (in_progress_index < in_progress_task_count) and (in_progress_scheduler_score[in_progress_index][0] >= item[0] - 1):
            sufficient = True
            for resource in resources_list:
                if resources_available[resource] < in_progress_tasks_df[resource][in_progress_index]: 
                    sufficient = False
                    break
            if sufficient:
                for resource in resources_list:
                    resources_available[resource] -= in_progress_tasks_df[resource][in_progress_index]
            else:
                in_progress_tasks_df.at[in_progress_index, 'Status'] = "Pending"
                in_progress_tasks_df.at[in_progress_index, 'Completion Date'] = pd.NA
            in_progress_index += 1

        sufficient = True
        for resource in resources_list:
            if resources_available[resource] < pending_complaints_df[resource][item[1]]: 
                sufficient = False
                break
        if sufficient:
            for resource in resources_list:
                resources_available[resource] -= pending_complaints_df[resource][item[1]]
            pending_complaints_df.at[item[1], 'Status'] = "In Progress"
            pending_complaints_df.at[item[1], 'Completion Date'] = str(current_date)

    # assign resources (if sufficient) to all in-progress tasks not considered yet
    while in_progress_index < in_progress_task_count:
        sufficient = True
        for resource in resources_list:
            if resources_available[resource] < in_progress_tasks_df[resource][in_progress_index]: 
                sufficient = False
                break
        if sufficient:
            for resource in resources_list:
                resources_available[resource] -= in_progress_tasks_df[resource][in_progress_index]
        else:
            in_progress_tasks_df.at[in_progress_index, 'Status'] = "Pending"
            in_progress_tasks_df.at[in_progress_index, 'Completion Date'] = pd.NA
        in_progress_index += 1

    # update In-Use resource counts
    for indx in range(resources_count):
        resources_df.at[indx, 'In Use'] = resources_df['Units Available'][indx] - resources_available[resources_df['Name'][indx]]

    # push changes to the databases
    try:
        file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': database_file['Resources']})
        resources_df.to_csv('temp.csv', index=False)
        file_obj.SetContentFile(filename='temp.csv')
        file_obj.Upload()
        
        complaints_df = pd.concat([complaints_df,pending_complaints_df], ignore_index=True)
        complaints_df = pd.concat([complaints_df,in_progress_tasks_df], ignore_index=True)
        file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': database_file['Schedule']})
        complaints_df.to_csv('temp.csv', index=False)
        file_obj.SetContentFile(filename='temp.csv')
        file_obj.Upload()
        for locality in localities_list:
            file_obj = drive.CreateFile({'parents': [{'id': database_folder}], 'id': database_file[locality]})
            complaints_df[complaints_df['Locality']==locality].to_csv('temp.csv', index=False)
            file_obj.SetContentFile(filename='temp.csv')
            file_obj.Upload()
            
    except:
        print("Network connection failed")
        exit()
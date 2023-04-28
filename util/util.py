import os
from projects.project import Project as project

if(not os.path.exists("data")):
    os.mkdir('data')

if(not os.path.exists("data/projects")):
    os.mkdir('data/projects')

auth_menu = {
    1: 'Register',
    2: 'Login',
    3: 'Exit'
}

projects_menu = {
    1: 'Create Project',
    2: 'View All Projects',
    3: 'View Own Projects',
    4: 'Open Project',
    5: 'Exit'
}

project_action_menu = {
    1: 'Update',
    2: 'Delete',
    3: 'Back'
}

def save_file(file_name, data, flag='auth'):
    try:
        f = open("data/"+file_name, "a")
        if(flag == 'auth'):
            f.write(data+"\n")
        else:
            f.write(data)
        f.close()
        print('Data Saved Successfully')
    except Exception as e:
        print(f"Error: {e}")

if(not os.path.exists("data/projects/.schema")):
        data = "pid:uid:title:details:target:start_time:end_time"
        f = open("data/projects/.schema", "a")
        f.write(data)
        f.write("\n0")
        f.close()

def select_item(menu):
    print("------------- Select Action From the Menu -------------")
    for key in menu.keys():
        print(key, '-', menu[key])
    
    while True:        
        try:
            key = int(input('Type action number: '))
            if(key not in menu.keys()):
                print("Please select a valid item")
                continue
            return {"key": key, "value": menu[key]}
        except ValueError as e:
            print(f"Please enter a valid number")
            continue

def convert_tuple_to_dict(tup):
    data = {}
    for index, i in enumerate(tup):
        data[index+1] = i
    return data




    

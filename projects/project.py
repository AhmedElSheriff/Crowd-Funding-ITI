from util import util
from util.validation import Validation
from util.colorprint import ColorPrint as colorPrint
import os, re
from auth.auth import Auth


class Project:
    def __init__(self, uid):
        self.title = ''
        self.details = ''
        self.target = ''
        self.start_time = ''
        self.end_time = ''
        self.uid = uid
        self.pid = ''
        self.start_date = ''
        self.end_date = ''

    project_fillable = (
            'title', 'details', 'target', 'start_time', 'end_time'
        ) 
    
    project_columns = (
        ['pid', 'uid', 'creator', 'title', 'target', 'start_time', 'end_time']
    )

    project_content_columns = (
        ['pid', 'uid', 'title', 'details', 'target', 'start_time', 'end_time']
    )

    # Validations

    def validate_end_time(self, time):
        validate = Validation(time)
        if(validate.is_valid_datetime()):
            if(self.start_time > time):
                colorPrint.print("\nEnd time can NOT be before start time\n", 'error')
                return False
            else:
                return True
        else:
            colorPrint.print("\nInvalid Format, correct format is DD/MM/YYYY H-M\n", 'error')
            return False
        
    def validate_end_date(self, date):
        validate = Validation(date)
        if(validate.is_valid_date()):
            if(self.start_date > date):
                colorPrint.print("\nEnd date can NOT be before start date\n", 'error')
                return False
            else:
                return True
        else:
            colorPrint.print("\nInvalid Format, correct format is DD/MM/YYYY H-M\n", 'error')
            return False
    # Helpers

    @staticmethod
    def get_user_by_id(uid):
        obj = {}
        with open("data/.auth", "r") as f:
            for line in f.readlines():
                arr = line.split(':')
                id = arr[0]
                if(uid == id):
                    for index, key in enumerate(Auth.auth_columns):
                        obj[key] = arr[index].strip('\n')
                    return obj
            return False

        
    @staticmethod
    def get_last_pid():
        try:
            if(os.stat("data/projects").st_size == 0):
                # Empty Directory
                return 0
            with open("data/projects/.schema", "r") as f:
                return int(f.readlines()[-1].strip('\n').split(':')[0])
        except:
            return 0
        
    @staticmethod
    def update_last_pid():
        import fileinput
        for line in fileinput.input("data/projects/.schema", inplace=True):
            if(fileinput.filelineno() == 2):
                print(int(line)+1, end='')
            else:
                print(line, end='')

    @staticmethod
    def list_all_project_ids():
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"[0-9]+$", file)):
                arr.append(int(file))
        return arr
    
    @staticmethod
    def serialize_project(arr):
        obj = {}
        for index, key in enumerate(Project.project_columns):
            obj[key] = arr[index].strip('\n')
        return obj
    
    @staticmethod
    def convert_projectfile_to_object(file_name, cols):
        with open("data/projects/"+str(file_name), "r") as f:
            arr = f.readlines()
            if(len(arr) != len(Project.project_columns)):
                raise Exception(f"Project file doesn't match the number of project columns, fix your file {file_name}")
            obj = {}
            for index, key in enumerate(cols):
                obj[key] = arr[index].strip('\n')
            return obj
        


    @staticmethod
    def get_field_index_from_schema(val):
        with open("data/projects/.schema", "r") as f:
            arr = f.readlines()[0].strip('\n').split(':')
            for index, i in enumerate(arr):
                if(i == val):
                    return index
            return False

    def show_project_content(self):
        obj = self.convert_projectfile_to_object(self.pid, Project.project_content_columns)
        user_object = self.get_user_by_id(obj['uid'])
        colorPrint.print(f"\n---------------------------------------------------\n", 'info')
        print(f"\nProject Title: ", end='')
        colorPrint.print(f"{obj['title'].upper()}", 'success')
        print(f"\n[Start Time: {obj['start_time']}] [End Time: {obj['end_time']}]")
        print(f"\nCreated By: ", end='')
        colorPrint.print(f"{user_object['email']}", 'success')
        print(f"\nTarget: ", end='')
        colorPrint.print(f"{obj['target']} EGP", 'success')
        colorPrint.print(f"\n---------------------------------------------------", 'info')
        print(f"\n{obj['details']}")
        colorPrint.print(f"\n---------------------------------------------------\n", 'info')
        return obj

    def create_or_update(self, item):
        while True:
            n = input(f'Enter the Project {item}: ')
            match item:
                case 'title':
                    validate = Validation(n)
                    if(not validate.is_valid_length(60)):
                        colorPrint.print("\nMaximum title length is 120 characters\n", 'error')
                        continue
                    self.title = n
                    break
                case 'details':
                    validate = Validation(n)
                    if(not validate.is_valid_length(600)):
                        colorPrint.print("\nMaximum details length is 600 characters\n", 'error')
                        continue
                    self.details = n
                    break
                case 'target':
                    validate = Validation(n)
                    if(not validate.is_valid_integer()):
                        colorPrint.print("\nTarget must be a valid number\n", 'error')
                        continue
                    self.target = n
                    break
                case 'start_time':
                    validate = Validation(n)
                    if(not validate.is_valid_datetime()):
                        colorPrint.print("\nInvalid Format, correct format is DD/MM/YYYY H-M\n", 'error')
                        continue
                    self.start_time = n
                    break
                case 'end_time':
                    validated = self.validate_end_time(n)
                    if(not validated):
                        continue
                    self.end_time = n
                    break
        return n

    def create(self):
        for field in self.project_fillable:
            self.create_or_update(field)
        else:
            pid = self.get_last_pid()+1
            data = f"{pid}\n{self.uid}\n{self.title}\n{self.details}\n{self.target}\n{self.start_time}\n{self.end_time}"
            if(util.save_file("projects/"+str(pid), data, 'project')):
                colorPrint.print("\nProject Created Successfully\n", 'success')
                self.update_last_pid()
            else:
                colorPrint.print("\nFailed to Create Project\n", 'error')
            

    def view_all(self):
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"[0-9]+$", file)):
                obj = self.convert_projectfile_to_object(file, Project.project_columns)
                arr_item = list(obj.values())
                #Remove Details from project
                del arr_item[3]
                user_object = self.get_user_by_id(obj['uid'])
                #Insert creator first name and last name
                if(user_object):
                    arr_item.insert(2, str(user_object['first_name']) + " " + str(user_object['last_name']))
                else:
                    arr_item.insert(2, ' ')
                arr.append(arr_item)
        if(len(arr) < 1):
            colorPrint.print("\nThere are no projects to show\n", 'info')
        else:
            util.print_data_in_table(self.project_columns, arr)


    def view_own(self):
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"^[0-9]+$", file)):
                obj = self.convert_projectfile_to_object(file, Project.project_columns)
                user_object = self.get_user_by_id(obj['uid'])
                if(user_object and user_object['uid'] == self.uid):
                    arr_item = list(obj.values())
                    #Remove Details from project
                    del arr_item[3]
                    #Insert creator first name and last name
                    arr_item.insert(2, str(user_object['first_name']) + " " + str(user_object['last_name']))
                    arr.append(arr_item)
                
        if(len(arr) < 1):
            colorPrint.print("\nYou currently don't have any projects to show\n", 'info')
        else:
            util.print_data_in_table(self.project_columns, arr)

    def delete(self):
        try:
            os.remove(f"data/projects/{self.pid}")
            colorPrint.print("\nProject Deleted Successfully\n", 'success')
            return True
        except:
            colorPrint.print("\nFailed to delete project\n", 'error')
            return False
        
    def update(self):
        try:
            item = util.select_item(util.convert_tuple_to_dict(self.project_fillable))
            n = self.create_or_update(item['value'])
            line_no = 0
            match item['value']:
                case 'title':
                    line_no = 2
                case 'details':
                    line_no = 3
                case 'target':
                    line_no = 4
                case 'start_time':
                    line_no = 5
                case 'end_time':
                    line_no = 6
            
            with open(f'data/projects/{str(self.pid)}', 'r') as f:
                lines = f.readlines()
            lines[line_no] = n+"\n"

            with open(f'data/projects/{str(self.pid)}', 'w') as file:
                file.writelines(lines)
            return True
        except Exception as e:
            print(e)
            return False
            
    def open(self):
        while True:
            try:
                n = int(input("Type Project ID: "))
                if(n not in self.list_all_project_ids()):
                    colorPrint.print("\nProject ID NOT Found\n", 'info')
                    break
                self.pid = n
                project_obj = self.show_project_content()
                item = util.select_item(util.project_action_menu)
                match item['key']:
                    case 1:
                        # Update
                        if(project_obj['uid'] != self.uid):
                            colorPrint.print("\nYou can ONLY edit your OWN projects\n", 'error')
                            break
                        updated = self.update()
                        if(updated):
                            colorPrint.print("\nUpdated Successfully\n", 'success')
                        else:
                            colorPrint.print("\nFailed To Update\n", 'error')
                        break
                    case 2:
                        # Delete
                        if(project_obj['uid'] != self.uid):
                            colorPrint.print("\nYou can ONLY delete your OWN projects\n", 'error')
                            break
                        deleted = self.delete()
                        if(deleted):
                            colorPrint.print("\nDeleted Successfully\n", 'success')
                        else:
                            colorPrint.print("\nFailed to Delete\n", 'error')
                        break
                    case 3:
                        # Back
                        break
            except ValueError as e:
                colorPrint.print(f"\nPlease enter a valid number {e}\n", 'error')

    def filter_result(self):
        from datetime import datetime
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"^[0-9]+$", file)):
                obj = self.convert_projectfile_to_object(file, self.project_columns)
                arr_item = list(obj.values())
                project_start_date = datetime.strptime(obj['start_time'][:obj['start_time'].index(' ')], '%d/%m/%Y')
                filter_start_date = datetime.strptime(self.start_date, '%d/%m/%Y')
                filter_end_date = datetime.strptime(self.end_date, '%d/%m/%Y')
                if(filter_start_date <= project_start_date and filter_end_date >= project_start_date):
                    #Remove Details from project
                    del arr_item[3]
                    user_object = self.get_user_by_id(obj['uid'])
                    #Insert creator first name and last name
                    if(user_object):
                        arr_item.insert(2, str(user_object['first_name']) + " " + str(user_object['last_name']))
                    else:
                        arr_item.insert(2, ' ')
                    arr.append(arr_item)
        if(len(arr) < 1):
            colorPrint.print("\nNo data matches your criteria\n", 'info')
        else:
            util.print_data_in_table(self.project_columns, arr)

    def filter(self):
        item = util.select_item(util.project_filter_menu)
        match item['key']:
            case 1:
                # Filter By Date
                while True:
                    n = input("Enter Start Date: ")
                    validate = Validation(n)
                    if(not validate.is_valid_date()):
                        colorPrint.print("\nInvalid Format, correct format is DD/MM/YYYY\n", 'error')
                        continue
                    self.start_date = n
                    break
                    
                while True:
                    n = input("Enter End Date: ")
                    validated = self.validate_end_date(n)
                    if(not validated):
                        continue
                    self.end_date = n
                    break
                self.filter_result()
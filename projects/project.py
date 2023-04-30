from util import util
from util.validation import Validation
from util.colorprint import ColorPrint as colorPrint
import os, re


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
        f = open("data/.auth", "r")
        for line in f.readlines():
            id = line.strip('\n').split(':')[0]
            if(uid == id):
                return line

        
    @staticmethod
    def get_last_pid():
        try:
            if(os.stat("data/projects").st_size == 0):
                # Empty Directory
                return 0
            f = open("data/projects/.schema", "r")
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
            if(re.match(r"[0-9]$", file)):
                arr.append(int(file))
        return arr
    
    @staticmethod
    def serialize_project(arr):
        return {
            "pid": arr[0],
            "uid": arr[1],
            "title": arr[2],
            "details": arr[3],
            "target": arr[4],
            "start_time": arr[5],
            "end_time": arr[6]
        }
    
    @staticmethod
    def get_field_index_from_schema(val):
        f = open("data/projects/.schema", "r")
        arr = f.readlines()[0].strip('\n').split(':')
        for index, i in enumerate(arr):
            if(i == val):
                return index
        return False

    def show_project_content(self, pid):
        f = open("data/projects/"+str(pid), "r")
        data = self.serialize_project(f.readline().strip('\n').split(':'))
        f.close()
        user_object = self.get_user_by_id(data['uid']).split(':')
        colorPrint.print(f"\n---------------------------------------------------\n", 'info')
        print(f"\nProject Title: ", end='')
        colorPrint.print(f"{data['title'].upper()}", 'success')
        print(f"\n[Start Time: {data['start_time']}] [End Time: {data['end_time']}]")
        print(f"\nCreated By: ", end='')
        colorPrint.print(f"{user_object[3]}", 'success')
        print(f"\nTarget: ", end='')
        colorPrint.print(f"{data['target']} EGP", 'success')
        colorPrint.print(f"\n---------------------------------------------------", 'info')
        print(f"\n{data['details']}")
        colorPrint.print(f"\n---------------------------------------------------\n", 'info')


    def create(self):
        for field in self.project_fillable:
            while True:
                n = input(f'Type the project {field}: ')
                match field:
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
        else:
            pid = self.get_last_pid()+1
            data = f"{pid}:{self.uid}:{self.title}:{self.details}:{self.target}:{self.start_time}:{self.end_time}"
            if(util.save_file("projects/"+str(pid), data, 'project')):
                colorPrint.print("\nProject Created Successfully\n", 'success')
                self.update_last_pid()
            else:
                colorPrint.print("\nFailed to Create Project\n", 'error')
            

    def view_all(self):
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"[0-9]$", file)):
                f = open("data/projects/"+file, "r")
                arr_item = f.readline().strip('\n').split(':')
                #Remove Details from project
                del arr_item[3]
                user_object = self.get_user_by_id(arr_item[1]).split(':')
                #Insert creator first name and last name
                arr_item.insert(2, str(user_object[1]) + " " + str(user_object[2]))
                arr.append(arr_item)
                f.close()
        if(len(arr) < 1):
            colorPrint.print("\nThere are no projects to show\n", 'info')
        else:
            util.print_data_in_table(self.project_columns, arr)


    def view_own(self):
        arr = []
        for file in os.listdir('data/projects'):
            if(re.match(r"^[0-9]$", file)):
                f = open("data/projects/"+file, "r")
                arr_item = f.readline().strip('\n').split(':')
                #Remove Details from project
                del arr_item[3]
                if(arr_item[1] == self.uid):
                    user_object = self.get_user_by_id(arr_item[1]).split(':')
                    #Insert creator first name and last name
                    arr_item.insert(2, str(user_object[1]) + " " + str(user_object[2]))
                    arr.append(arr_item)
                f.close()
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
            index = self.get_field_index_from_schema(item['value'])
            f = open("data/projects/"+str(self.pid), "r")
            arr = f.readline().strip('\n').split(':')
            n = input(f'Enter the new {item["value"]}: ')
            arr[index] = n
            line = ':'.join(arr)

            import fileinput
            for ln in fileinput.input("data/projects/"+str(self.pid), inplace=True):
                print(line, end='')
            return True
        except:
            return False
            
    def open(self):
        while True:
            try:
                n = int(input("Type Project ID: "))
                if(n not in self.list_all_project_ids()):
                    colorPrint.print("\nProject ID NOT Found\n", 'info')
                    break
                self.pid = n
                self.show_project_content(n)
                item = util.select_item(util.project_action_menu)
                match item['key']:
                    case 1:
                        # Update
                        updated = self.update()
                        if(updated):
                            colorPrint.print("\nUpdated Successfully\n", 'success')
                        else:
                            colorPrint.print("\nFailed To Update\n", 'error')
                        break
                    case 2:
                        # Delete
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
            if(re.match(r"^[0-9]$", file)):
                f = open("data/projects/"+file, "r")
                arr_item = f.readline().strip('\n').split(':')
                data = self.serialize_project(arr_item)
                project_start_date = datetime.strptime(data['start_time'][:data['start_time'].index(' ')], '%d/%m/%Y')
                filter_start_date = datetime.strptime(self.start_date, '%d/%m/%Y')
                filter_end_date = datetime.strptime(self.end_date, '%d/%m/%Y')
                if(filter_start_date <= project_start_date and filter_end_date >= project_start_date):
                    #Remove Details from project
                    del arr_item[3]
                    user_object = self.get_user_by_id(data['uid']).split(':')
                    #Insert creator first name and last name
                    arr_item.insert(2, str(user_object[1]) + " " + str(user_object[2]))
                    arr.append(arr_item)
                f.close()
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
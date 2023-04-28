from util import util
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

    project_fillable = (
            'title', 'details', 'target', 'start_time', 'end_time'
        ) 
    
    project_fields_dict = {}

    # Validations
    def validate_title():
        pass
    def validate_details():
        pass
    def validate_target():
        pass
    def validate_start_time():
        pass
    def validate_end_time():
        pass

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
    def update_last_pid(pid):
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
        arr = f.readline().strip('\n').split(':')
        print(self.serialize_project(arr))
        # return self.serialize_project(arr)


    def create(self):
        for field in self.project_fillable:
            while True:
                n = input(f'Type the project {field}: ')
                match field:
                    case 'title':
                        # validated = self.validate_title(n)
                        # if(not validated):
                        #     print(f"")
                        #     continue
                        self.title = n
                        break
                    case 'details':
                        # validated = self.validate_details(n)
                        # if(not validated):
                        #     print(f"")
                        #     continue
                        self.details = n
                        break
                    case 'target':
                        # validated = self.validate_target(n)
                        # if(not validated):
                        #     print(f"")
                        #     continue
                        self.target = n
                        break
                    case 'start_time':
                        # validated = self.validate_start_time(n)
                        # if(not validated):
                        #     print(f"")
                        #     continue
                        self.start_time = n
                        break
                    case 'end_time':
                        # validated = self.validate_end_time(n)
                        # if(not validated):
                        #     print(f"")
                        #     continue
                        self.end_time = n
                        break
        else:
            pid = self.get_last_pid()+1
            data = f"{pid}:{self.uid}:{self.title}:{self.details}:{self.target}:{self.start_time}:{self.end_time}"
            util.save_file("projects/"+str(pid), data, 'project')
            self.update_last_pid(pid)

    def view_all(self):
        for file in os.listdir('data/projects'):
            if(re.match(r"[0-9]$", file)):
                f = open("data/projects/"+file, "r")
                arr = f.readline().strip('\n').split(':')
                print(self.serialize_project(arr))

    def view_own(self):
        for file in os.listdir('data/projects'):
            if(re.match(r"^[0-9]$", file)):
                f = open("data/projects/"+file, "r")
                arr = f.readline().strip('\n').split(':')
                data = self.serialize_project(arr)
                if(data['uid'] == self.uid):
                    print(data)

    def delete(self):
        try:
            os.remove(f"data/projects/{self.pid}")
            print("Project Deleted Successfully")
            return True
        except:
            print("Failed to delete project")
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
                    print("Project ID Not Found")
                    continue
                self.pid = n
                self.show_project_content(n)
                item = util.select_item(util.project_action_menu)
                match item['key']:
                    case 1:
                        # Update
                        updated = self.update()
                        if(updated):
                            print("Updated Successfully")
                        else:
                            print("Failed To Update")
                        break
                    case 2:
                        # Delete
                        deleted = self.delete()
                        if(deleted):
                            print("Deleted Successfully")
                        else:
                            print("Failed To Delete")
                        break
                    case 3:
                        # Back
                        break
            except ValueError as e:
                print(f"Please enter a valid number {e}")

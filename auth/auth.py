from util import util
class Auth:
    UID = 0
    def __init__(self):
        self.first_name = ''
        self.last_name = ''
        self.email = ''
        self.password = ''
        self.confirm_password = ''
        self.mobile = ''

    register_fillable = (
            'first_name', 'last_name', 'email', 'password', 'confirm_password', 'mobile'
        )   
    login_fillable = (
            'email', 'password'
        )   

    # Validations
    @staticmethod
    def validate_name(name):
        if(not name.isalpha()):
            return False
        return True
    @staticmethod
    def validate_email(email):
        import re
        email_regex = "^[A-Za-z0-9]+@[A-Za-z0-9]+\.[A-Za-z]+[0-9]*$"
        if(re.search(email_regex, email)):
            return True
        else:
            return False
    def validate_password(self, password):
        if(password == self.password):
            return True
        else:
            return False
    @staticmethod
    def validate_mobile(mobile):
        import re
        mobile_regex = "^01[0125][0-9]{8}$"
        if(re.search(mobile_regex, mobile)):
            return True
        else:
            return False  
    def validate_login(self):
        try:
            f = open("data/auth", "r")
            for line in f.readlines():
                e = line.strip('\n').split(':')[3]
                p = line.strip('\n').split(':')[4]
                uid = line.strip('\n').split(':')[0]
                if(e == self.email and p == self.password):
                    return uid
            return False
        except:
            return False
    @staticmethod
    def get_last_uid():
        import os
        try:
            if(os.stat("data/auth").st_size == 0):
                # Empty file
                return 0
            f = open("data/auth", "r")
            return f.readlines()[-1].strip('\n').split(':')[0]
        except:
            return 0
    @staticmethod
    def email_exists(email):
        import os
        if(not os.path.exists("data/auth")):
            return False
        f = open("data/auth", "r")
        for line in f.readlines():
            e = line.strip('\n').split(':')[3]
            if(email == e):
                return True
        return False
    
    def register(self):
        for field in self.register_fillable:
            while True:
                n = input(f'Type your {field}: ')
                match field:
                    case 'first_name':
                        validated = self.validate_name(n)
                        if(not validated):
                            print(f"{field} must be a valid name")
                            continue
                        self.first_name = n
                        break
                    case 'last_name':
                        validated = self.validate_name(n)
                        if(not validated):
                            print(f"{field} must be a valid name")
                            continue
                        self.last_name = n
                        break
                    case 'email':
                        validated = self.validate_email(n)
                        if(not validated):
                            print(f"{field} must be a valid email")
                            continue
                        if(self.email_exists(n)):
                            print("Email must be unique")
                            continue
                        self.email = n
                        break
                    case 'password':
                        self.password = n
                        break
                    case 'confirm_password':
                        validated = self.validate_password(n)
                        if(not validated):
                            print(f"{field} must match the password")
                            continue
                        self.confirm_password = n
                        break
                    case 'mobile':
                        validated = self.validate_mobile(n)
                        if(not validated):
                            print(f"{field} must be a valid egyptian mobile number")
                            continue
                        self.mobile = n
                        break
        else:
            uid = self.get_last_uid()
            data = f"{int(uid)+1}:{self.first_name}:{self.last_name}:{self.email}:{self.password}:{self.mobile}"
            util.save_file("auth", data)

    def login(self):
        for field in self.login_fillable:
            while True:
                n = input(f'Type your {field}: ')
                match field:
                    case 'email':
                        validated = self.validate_email(n)
                        if(not validated):
                            print(f"{field} must be a valid email")
                            continue
                        self.email = n
                        break
                    case 'password':
                        self.password = n
                        break

        uid = self.validate_login()
        if(not uid):
            print("Incorrect Email or Password")
            return False
        else:
            print("Logged In")
            return uid
                    

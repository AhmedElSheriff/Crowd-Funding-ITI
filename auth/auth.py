from util import util
from util.validation import Validation
from util.colorprint import ColorPrint as colorPrint

class Auth:
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
    def validate_password(self, password):
        if(password == self.password):
            return True
        else:
            return False
        
    def validate_email(self, email):
        validate = Validation(email)
        if(validate.is_valid_email()):
            if(self.email_exists(email)):
                colorPrint.print("\nEmail Already Exists, Please use a different email\n", 'error')
                return False
            else:
                return True
        else:
            colorPrint.print("\nInvalid Email Format\n", 'error')
            return False

    def validate_login(self):
        try:
            f = open("data/.auth", "r")
            for line in f.readlines():
                e = line.strip('\n').split(':')[3]
                p = line.strip('\n').split(':')[4]
                uid = line.strip('\n').split(':')[0]
                if(e == self.email and p == self.password):
                    return uid
            return False
        except:
            return False
    
    # Helpers 
    @staticmethod
    def get_last_uid():
        import os
        try:
            if(os.stat("data/.auth").st_size == 0):
                # Empty file
                return 0
            f = open("data/.auth", "r")
            return f.readlines()[-1].strip('\n').split(':')[0]
        except:
            return 0
        
    @staticmethod
    def email_exists(email):
        import os
        if(not os.path.exists("data/.auth")):
            return False
        f = open("data/.auth", "r")
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
                        validate = Validation(n)
                        if(not validate.is_valid_string()):
                            colorPrint.print("\nInput must only contain Alphabet\n", 'error')
                            continue
                        self.first_name = n
                        break
                    case 'last_name':
                        validate = Validation(n)
                        if(not validate.is_valid_string()):
                            colorPrint.print("\nInput must only contain Alphabet\n", 'error')
                            continue
                        self.last_name = n
                        break
                    case 'email':
                        validated = self.validate_email(n.lower())
                        if(not validated):
                            continue
                        self.email = n.lower()
                        break
                    case 'password':
                        self.password = n
                        break
                    case 'confirm_password':
                        validated = self.validate_password(n)
                        if(not validated):
                            colorPrint.print("\nConfirm password must match the password\n", 'error')
                            continue
                        self.confirm_password = n
                        break
                    case 'mobile':
                        validate = Validation(n)
                        if(not validate.is_valid_mobile()):
                            colorPrint.print("\nMobile number must be a valid egyptian mobile number\n", 'error')
                            continue
                        self.mobile = n
                        break
        else:
            uid = self.get_last_uid()
            import hashlib
            hashed_pass = hashlib.md5(n.encode()).hexdigest()
            data = f"{int(uid)+1}:{self.first_name}:{self.last_name}:{self.email}:{hashed_pass}:{self.mobile}"
            if(util.save_file(".auth", data)):
                colorPrint.print("\nRegistered Successfully\n", 'success')
            else:
                colorPrint.print("\nFailed to Register\n", 'error')

    def login(self):
        for field in self.login_fillable:
            while True:
                n = input(f'Type your {field}: ')
                match field:
                    case 'email':
                        validate = Validation(n)
                        if(not validate.is_valid_email()):
                            colorPrint.print("\nInvalid Email Format\n", 'error')
                            continue
                        self.email = n.lower()
                        break
                    case 'password':
                        import hashlib
                        hashed_pass = hashlib.md5(n.encode()).hexdigest()
                        self.password = hashed_pass
                        break

        uid = self.validate_login()
        if(not uid):
            colorPrint.print("\nIncorrect Email or Password\n", 'error')
            return False
        else:
            colorPrint.print("\nLogged In\n", 'success')
            return uid
                    

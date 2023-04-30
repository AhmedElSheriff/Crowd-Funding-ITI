class Validation:
    def __init__(self, value):
        self.value = value

    def is_valid_integer(self):
        try:
            int(self.value)
            return True
        except ValueError:
            return False

    def is_valid_float(self):
        try:
            float(self.value)
            return True
        except ValueError:
            return False
        
    def is_valid_string(self):
        if(self.value.isalpha()):
            return True
        else:
            return False

    def is_valid_email(self):
        import re
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if re.match(pattern, self.value):
            return True
        else:
            return False

    def is_valid_mobile(self):
        import re
        pattern = r'^01[0125][0-9]{8}$'
        if re.match(pattern, self.value):
            return True
        else:
            return False
        
    def is_valid_length(self, length):
        if(len(self.value) > length):
            return False
        else:
            return True
        
    def is_valid_datetime(date_time):
        import datetime
        try:
            date =  datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M')
            return True
        except Exception as e:
            print("Invalid Format, correct format is YYYY-MM-DD H:M")
            return False
class ColorPrint:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    @staticmethod
    def print(message, message_type):
        if message_type == 'error':
            color = ColorPrint.FAIL
        elif message_type == 'warning':
            color = ColorPrint.WARNING
        elif message_type == 'success':
            color = ColorPrint.OKGREEN
        elif message_type == 'info':
            color = ColorPrint.OKBLUE
        else:
            color = ''

        print(f'{color}{message}{ColorPrint.ENDC}')
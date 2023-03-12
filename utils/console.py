import datetime
import colorama

def print_module_message(module, message, module_color = colorama.Fore.LIGHTBLACK_EX, message_color = colorama.Fore.YELLOW, with_date = True, date_color = colorama.Fore.WHITE):
    return print(f"{date_color}{datetime.datetime.strftime(datetime.datetime.now(), '[%d/%m/%Y %H:%M:%S]') if with_date else ''} {module_color}[{module}] {message_color}{message}")

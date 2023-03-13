import datetime
import colorama

def print_module_message(repository_owner_name, repository_name, module, message, repository_owner_name_color = colorama.Fore.LIGHTBLACK_EX, repository_name_color = colorama.Fore.LIGHTBLACK_EX, date_color = colorama.Fore.WHITE, module_color = colorama.Fore.LIGHTBLACK_EX, message_color = colorama.Fore.YELLOW, with_date = True):
    return print(f"{repository_owner_name_color}[{repository_owner_name}]{repository_name_color}[{repository_name}] {date_color}{datetime.datetime.strftime(datetime.datetime.now(), '[%d/%m/%Y %H:%M:%S]') if with_date else ''} {module_color}[{module}] {message_color}{message}")

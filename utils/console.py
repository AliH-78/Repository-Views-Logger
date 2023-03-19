import sys
import colorama
from . import time

def module_info(repository, module, message, date_color = colorama.Fore.WHITE, module_color = colorama.Fore.LIGHTBLACK_EX, message_color = colorama.Fore.WHITE, with_date = True):
    return sys.stdout.write(f"{colorama.Fore.LIGHTBLACK_EX}[{repository.owner.login}]{colorama.Fore.LIGHTBLACK_EX}[{repository.name}] {date_color}[{time.get_string_date(system_time = True) if with_date else ''}] {module_color}[{module}] {message_color}{message}\n")

def module_error(repository, module, message, date_color = colorama.Fore.WHITE, module_color = colorama.Fore.LIGHTBLACK_EX, message_color = colorama.Fore.RED, with_date = True):
    return sys.stderr.write(f"{colorama.Fore.LIGHTBLACK_EX}[{repository.owner.login}]{colorama.Fore.LIGHTBLACK_EX}[{repository.name}] {date_color}[{time.get_string_date(system_time = True) if with_date else ''}] {module_color}[{module}] {message_color}{message}\n")

def repository_views_logger_message(repository, message, message_color = colorama.Fore.WHITE):
    return module_info(repository, module = "Repository Views Logger", module_color = colorama.Fore.CYAN, message = message, message_color = message_color)

def popular_files_views_logger_message(repository, message, message_color = colorama.Fore.WHITE):
    return module_info(repository, module = "File Views Logger", module_color = colorama.Fore.MAGENTA, message = message, message_color = message_color)

def repository_views_logger_error(repository, message, message_color = colorama.Fore.RED):
    return module_error(repository, module = "Repository Views Logger", module_color = colorama.Fore.CYAN, message = message, message_color = message_color)

def popular_files_views_logger_error(repository, message, message_color = colorama.Fore.RED):
    return module_error(repository, module = "File Views Logger", module_color = colorama.Fore.MAGENTA, message = message, message_color = message_color)

def error_message(error_text, error_color = colorama.Fore.RED):
    return sys.stderr.write(f"{error_color}{error_text}\n")

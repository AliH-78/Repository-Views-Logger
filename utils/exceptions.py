import traceback
import os
from . import console, log, time, constants

def log_module_traceback(module, repository):
    log_traceback(f"{module} {repository.owner.login} {repository.name}")

def log_traceback(filename):
    traceback_log = log.Log(filename = f"{constants.LOG_FOLDER}{os.sep}{filename} {time.get_string_date(for_file = True, system_time = True)}.log") 
    traceback_log.write_error(traceback.format_exc())
    traceback_log.close()

def handle_request_error_traceback():
    console.error_message("An error occured while requesting to GitHub servers. More information available at log file.")

    log_traceback("REQUEST_ERR")

def handle_response_error_traceback(exception):
    if exception.error_code in [401, 403]:
        console.error_message("Token is invalid or token isn't authorized.")
    
    elif exception.error_code == 404:
        console.error_message("The requested page couldn't found.")

    elif exception.error_code // 100 == 3:
        console.error_message("URL Redirection Error.")

    elif exception.error_code // 100 == 5:
        console.error_message("A server-side error occured.")

    log_traceback("GITHUB_RESPONSE_ERR")

def handle_repository_views_exception_traceback(repository):
    console.repository_views_logger_error(repository, message = "[!] An error occured at Repository Views Logger thread. More information available at the log file.")

    log_module_traceback("REPO_VIEWS_LOGGER", repository)

def handle_popular_files_views_exception_traceback(repository):
    console.popular_files_views_logger_error(repository, message = "[!] An error occured at Popular Files' Views Logger thread. More information available at the log file.")

    log_module_traceback("FILE_VIEWS_LOGGER", repository)

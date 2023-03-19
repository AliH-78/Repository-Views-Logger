import traceback
import os
from . import console, log, time, constants

def log_traceback(module, repository):
    traceback_log = log.Log(filename = f"{constants.LOG_FOLDER}{os.sep}{module} {repository.owner.login} {repository.name} {time.get_string_date(for_file = True, system_time = True)}.log") 
    traceback_log.write_error(traceback.format_exc())
    traceback_log.close()

def log_repository_views_traceback(repository):
    console.repository_views_logger_error(repository, message = "[!] An error occured at Repository Views Logger thread. More information available at the log file.")

    log_traceback("REPO_VIEWS_LOGGER", repository)

def log_popular_files_views_traceback(repository):
    console.popular_files_views_logger_error(repository, message = "[!] An error occured at Popular Files' Views Logger thread. More information available at the log file.")

    log_traceback("FILE_VIEWS_LOGGER", repository)
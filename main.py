import sys
import os
import time
import argparse
import threading
import view_logger.github
import view_logger.db
import utils.console
import utils.exceptions
import utils.time
import utils.constants
import colorama


def log_repository_views(account, repository, at_exception = None, at_exception_args = (), at_exception_kwargs = None):
    if at_exception_kwargs is None:
        at_exception_kwargs = {}

    def _log_repository_views(account, repository):
        db_handle = view_logger.db.DBHandle(f"{utils.constants.USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}{utils.constants.REPO_VIEWS_DB_NAME}")
        db_handle.create_table("REPO_VIEWS", ("TIMESTAMP", "VIEWS", "UNIQUES"))

        while True:
            utils.console.repository_views_logger_message(repository, message = "[i] Getting repository views...")

            view_values = db_handle.read_value("REPO_VIEWS", many = 15, sort_reverse = True)
            new_view_values = account.get_view_count(repository)
            view_values_to_write = [i for i in new_view_values if i[0] not in [i[0] for i in view_values]]

            utils.console.repository_views_logger_message(repository, message = "[i] Repository views has been handled.")
            utils.console.repository_views_logger_message(repository, message = "[i] Repository views are writting to database...")

            for view_value in view_values_to_write:
                db_handle.insert_value("REPO_VIEWS", view_value)

            utils.console.repository_views_logger_message(repository, message = "[i] Repository views are written.")
            utils.console.repository_views_logger_message(repository, message = "[i] Waiting for next day...")

            time.sleep(60 * 60 * 24)
    
    try:
        return _log_repository_views(account, repository)
    
    except:
        if not at_exception:
            raise
        
        at_exception(*at_exception_args, **at_exception_kwargs)

def log_popular_files_views(account, repository, at_exception = None, at_exception_args = (), at_exception_kwargs = None):
    if at_exception_kwargs is None:
        at_exception_kwargs = {}

    def _log_popular_files_views(account, repository):
        db_handle = view_logger.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}{utils.constants.FILE_VIEWS_DB_NAME}")
        db_handle.create_table("FILE_VIEWS", ("START_DATE_TIMESTAMP", "END_DATE_TIMESTAMP", "FILE", "VIEWS", "UNIQUES"))

        while True:
            utils.console.popular_files_views_logger_message(repository, message = "[i] Getting repository files' views...")

            new_view_values = account.get_popular_files_views(repository)
            
            current_time = utils.time.get_utc_timestamp()
            last_log_date = db_handle.read_value("FILE_VIEWS", ("END_DATE_TIMESTAMP",), many = 1, sort_reverse = True)
            last_log_date = current_time if not last_log_date else last_log_date[0][0]

            time_for_sleep = 60*60*24*15 - (current_time - last_log_date)

            if time_for_sleep <= 0:
                utils.console.popular_files_views_logger_message(repository, message = "[i] Repository file views are writting to database...")

                for new_view_value in new_view_values:
                    db_handle.insert_value("FILE_VIEWS", new_view_value)
            
            if time_for_sleep > 0:
                utils.console.popular_files_views_logger_message(repository, message = "[i] Checking any additional file different from database...")

                for new_view_value in new_view_values:
                    query_is_file_exists = db_handle.read_value("FILE_VIEWS", ("FILE",), condition = f"WHERE FILE = '{new_view_value[2]}'")

                    if not query_is_file_exists:
                        utils.console.popular_files_views_logger_message(repository, message = "[i] Different file view data found. Writing to database...")
                        db_handle.insert_value("FILE_VIEWS", new_view_value)

                utils.console.popular_files_views_logger_message(repository, message = f"[i] Waiting for {time_for_sleep//60//60//24} days...")

                time.sleep(time_for_sleep)
    
    try:
        return _log_popular_files_views(account, repository)
    
    except:
        if not at_exception:
            raise
        
        at_exception(*at_exception_args, **at_exception_kwargs)
        

def main():
    try:
        github_account = view_logger.github.GitHubAccount(token = cmdline_arguments.token)
        selected_repository = github_account.select_repository(cmdline_arguments.repository_name)

    except view_logger.exceptions.GitHubRequestError as exc:
        utils.console.error_message("An error occured while requesting to GitHub servers. More information available at log file.")

        sys.exit(1)

    except view_logger.exceptions.GitHubResponseError as exc:
        if exc.error_code in [401, 403]:
            utils.console.error_message("Token is invalid or token isn't authorized.")
        
        elif exc.error_code == 404:
            utils.console.error_message("The requested page couldn't found.")

        elif exc.error_code // 100 == 3:
            utils.console.error_message("URL Redirection Error.")

        elif exc.error_code // 100 == 5:
            utils.console.error_message("A server-side error occured.")

        sys.exit(1)

    if cmdline_arguments.log_repository_views and cmdline_arguments.log_popular_files_views:
        log_repository_views_thread = threading.Thread(target = log_repository_views, args = (github_account, selected_repository, utils.exceptions.log_repository_views_traceback, (selected_repository,)), daemon = True)
        log_popular_files_views_thread = threading.Thread(target = log_popular_files_views, args = (github_account, selected_repository, utils.exceptions.log_popular_files_views_traceback, (selected_repository,)), daemon = True)

        log_repository_views_thread.start()
        log_popular_files_views_thread.start()

    elif cmdline_arguments.log_repository_views:
        log_repository_views_thread = threading.Thread(target = log_repository_views, args = (github_account, selected_repository, utils.exceptions.log_repository_views_traceback, (selected_repository,)), daemon = True)

        log_repository_views_thread.start()

    elif cmdline_arguments.log_popular_files_views:
        log_popular_files_views_thread = threading.Thread(target = log_popular_files_views, args = (github_account, selected_repository, utils.exceptions.log_popular_files_views_traceback, (selected_repository,)), daemon = True)

        log_popular_files_views_thread.start()

    else:
        utils.console.error_message("Not enough argument.")
        sys.exit(1)

    try:
       input()

    except KeyboardInterrupt:
        pass

    os.system("clear")
    utils.console.error_message("Process terminated.")
    sys.exit(0)


if __name__ == "__main__":
    colorama.init(autoreset = True)
    USERS_FOLDER = "users"

    argument_parser = argparse.ArgumentParser(prog = "Repository Views Logger")

    argument_parser.add_argument("--token", required = True)
    argument_parser.add_argument("--repository-name", required = True)
    argument_parser.add_argument("--log-repository-views", action = "store_true")
    argument_parser.add_argument("--log-popular-files-views", action = "store_true")

    cmdline_arguments = argument_parser.parse_args()

    main()




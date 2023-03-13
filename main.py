import sys
import os
import time
import datetime
import argparse
import threading
import api.github
import api.db
import utils.console
import colorama

def log_repository_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}views.db")
    db_handle.create_table("REPO_VIEWS", ("DATE", "VIEWS", "UNIQUES"))

    while True:
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "REPOSITORY VIEW LOGGER", message = "[i] Getting repository views...")

        view_values = db_handle.read_value("REPO_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(date, view_dict["view_count"], view_dict["unique_views"])
                            for date, view_dict
                            in api.github.handle_traffic_information(account.get_view_count(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values if i[0] not in [i[0] for i in view_values]])

        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "REPOSITORY VIEW LOGGER", message = "[i] Repository views has been handled.")
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "REPOSITORY VIEW LOGGER", message = "[i] Repository views are writting to database...")

        for view_value in view_values_to_write:
            db_handle.insert_value("REPO_VIEWS", view_value)

        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "REPOSITORY VIEW LOGGER", message = "[i] Repository views are written.")
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "REPOSITORY VIEW LOGGER", message = "[i] Waiting for next day...")

        time.sleep(60 * 60 * 24)

def log_popular_files_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}file_views.db")
    db_handle.create_table("FILE_VIEWS", ("START_DATE", "END_DATE", "FILE", "VIEWS", "UNIQUES"))

    while True:
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "FILE VIEWS LOGGER", module_color = colorama.Fore.LIGHTCYAN_EX, message = "[i] Getting repository files' views...")

        current_time = datetime.datetime.now()

        view_values = db_handle.read_value("FILE_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(datetime.datetime.strftime(current_time - datetime.timedelta(days = 15), "%Y-%m-%dT%H:%M:%SZ"),
                            datetime.datetime.strftime(current_time, "%Y-%m-%dT%H:%M:%SZ"),
                            file, view_dict["view_count"], view_dict["unique_views"]) for file, view_dict in
                            api.github.handle_popular_files_information(account.get_popular_files_views(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values
                                       if (i[0].split("T")[0], i[1].split("T")[0]) not in
                                       [(i[0].split("T")[0], i[1].split("T")[0]) for i in view_values] or i[3] not in [i[3] for i in view_values]])

        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "FILE VIEWS LOGGER", module_color = colorama.Fore.LIGHTCYAN_EX, message = "[i] Repository file views has been handled.")
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "FILE VIEWS LOGGER", module_color = colorama.Fore.LIGHTCYAN_EX, message = "[i] Repository file views are writting to database...")

        for view_value in view_values_to_write:
            db_handle.insert_value("FILE_VIEWS", view_value)

        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "FILE VIEWS LOGGER", module_color = colorama.Fore.LIGHTCYAN_EX, message = "[i] Repository file views are written.")
        utils.console.print_module_message(repository_name = repository.name, repository_owner_name = repository.owner.login, module = "FILE VIEWS LOGGER", module_color = colorama.Fore.LIGHTCYAN_EX, message = "[i] Waiting for next two weeks...")

        time.sleep(60 * 60 * 24 * 15)

def main():
    try:
        github_account = api.github.GitHubAccount(token = cmdline_arguments.token)
        selected_repository = github_account.select_repository(cmdline_arguments.repository_name)

    except api.exceptions.GitHubRequestError as exc:
        if exc.error_code in [401, 403]:
            print(f"{colorama.Fore.RED}Token is invalid or token isn't authorized.")

        elif exc.error_code // 100 == 3:
            print(f"{colorama.Fore.RED}URL Redirection Error.")

        elif exc.error_code // 100 == 5:
            print(f"{colorama.Fore.RED}A server-side error occured.")

        sys.exit(1)

    if cmdline_arguments.log_repository_views and cmdline_arguments.log_popular_files_views:
        log_repository_views_thread = threading.Thread(target = log_repository_views, args = (github_account, selected_repository), daemon = True)
        log_popular_files_views_thread = threading.Thread(target = log_popular_files_views, args = (github_account, selected_repository), daemon = True)

        log_repository_views_thread.start()
        log_popular_files_views_thread.start()

    elif cmdline_arguments.log_repository_views:
        log_repository_views_thread = threading.Thread(target = log_repository_views, args = (github_account, selected_repository), daemon = True)

        log_repository_views_thread.start()

    elif cmdline_arguments.log_popular_files_views:
        log_popular_files_views_thread = threading.Thread(target = log_popular_files_views, args = (github_account, selected_repository), daemon = True)

        log_popular_files_views_thread.start()

    else:
        sys.stderr.write("Not enough argument.\n")
        sys.exit(1)

    try:
       input()

    except KeyboardInterrupt:
        pass

    os.system("clear")
    print(f"{colorama.Fore.RED}Process terminated.")
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




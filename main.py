import sys
import os
import time
import datetime
import api.github
import api.db

def log_repository_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}views.db")
    db_handle.create_table("REPO_VIEWS", ("DATE", "VIEWS", "UNIQUES"))

    while True:
        print("[i] Getting repository views...")

        view_values = db_handle.read_value("REPO_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(date, view_dict["view_count"], view_dict["unique_views"])
                            for date, view_dict
                            in api.github.handle_traffic_information(account.get_view_count(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values if i not in view_values])

        print("[i] Repository views has been handled.")
        print("[i] Repository views are writing to database...")

        for view_value in view_values_to_write:
            db_handle.insert_value("REPO_VIEWS", view_value)

        print("[i] Repository views are written.")
        print("[i] Waiting for next day...")

        time.sleep(60 * 60 * 24)

def log_popular_files_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}file_views.db")
    db_handle.create_table("FILE_VIEWS", ("START_DATE", "END_DATE", "FILE", "VIEWS", "UNIQUES"))

    while True:
        print("[i] Getting repository files' views...")

        current_time = datetime.datetime.now()

        view_values = db_handle.read_value("FILE_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(datetime.datetime.strftime(current_time - datetime.timedelta(days = 15), "%Y-%m-%dT%H:%M:%SZ"),
                            datetime.datetime.strftime(current_time, "%Y-%m-%dT%H:%M:%SZ"),
                            file, view_dict["view_count"], view_dict["unique_views"]) for file, view_dict in 
                            api.github.handle_popular_files_information(account.get_popular_files_views(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values if (i[0], i[1]) not in [(i[0], i[1]) for i in view_values]])

        print("[i] Repository file views has been handled.")
        print("[i] Repository file views are writing to database...")

        for view_value in view_values_to_write:
            db_handle.insert_value("FILE_VIEWS", view_value)

        print("[i] Repository file views are written.")
        print("[i] Waiting for next two week...")

        time.sleep(60 * 60 * 24 * 15)

USERS_FOLDER = "users"

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python main.py <token> <repository_name> <method>")
        exit(1)

    github_account = api.github.GitHubAccount(token = sys.argv[1])
    selected_repository = github_account.select_repository(sys.argv[2])

    if sys.argv[3].lower() == "log_repo_view":
        log_repository_views(github_account, selected_repository)

    elif sys.argv[3].lower() == "log_files_view":
        log_popular_files_views(github_account, selected_repository)




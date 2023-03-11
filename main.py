import sys
import os
import time
import multiprocessing
import api.github
import api.db

def log_repository_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}views.db")
    db_handle.create_table("REPO_VIEWS", ("DATE", "VIEWS", "UNIQUES"))

    while True:
        view_values = db_handle.read_value("REPO_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(date, view_dict["view_count"], view_dict["unique_views"]) 
                            for date, view_dict 
                            in api.github.handle_traffic_information(account.get_view_count(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values if i not in view_values])
        
        for view_value in view_values_to_write:
            db_handle.insert_value("REPO_VIEWS", view_value)

        time.sleep(60 * 60 * 24)

def log_popular_files_views(account, repository):
    db_handle = api.db.DBHandle(f"{USERS_FOLDER}{os.sep}{account.user_information.login}{os.sep}{repository.name}{os.sep}file_views.db")
    db_handle.create_table("FILE_VIEWS", ("FILE", "VIEWS", "UNIQUES"))

    while True:
        view_values = db_handle.read_value("FILE_VIEWS", many = 15, sort_reverse = True)
        new_view_values = [(file, view_dict["view_count"], view_dict["unique_views"]) 
                            for file, view_dict 
                            in api.github.handle_popular_files_information(account.get_popular_files_views(repository)).items()]
        view_values_to_write = sorted([i for i in new_view_values if i not in view_values])
        
        for view_value in view_values_to_write:
            db_handle.insert_value("FILE_VIEWS", view_value)

        time.sleep(60 * 60 * 24 * 15)

USERS_FOLDER = "users"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        exit(1)
    
    github_account = api.github.GitHubAccount(token = sys.argv[1])
    selected_repository = github_account.select_repository(sys.argv[2])

    log_repository_views(github_account, selected_repository)




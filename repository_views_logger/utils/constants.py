import platform

SYSTEM = platform.system().lower()

USERS_FOLDER = "repository_views"
LOG_FOLDER = "log"

REPO_VIEWS_DB_FILE_NAME = "views.db"
FILE_VIEWS_DB_FILE_NAME = "file_views.db"

REPO_VIEWS_DB_TABLE_NAME = "REPO_VIEWS"
FILE_VIEWS_DB_TABLE_NAME = "FILE_VIEWS"

REPO_VIEWS_DB_COLUMNS = ("TIMESTAMP", "VIEWS", "UNIQUES")
FILE_VIEWS_DB_COLUMNS = ("START_DATE_TIMESTAMP", "END_DATE_TIMESTAMP", "FILE", "VIEWS", "UNIQUES")

GENERAL_DATE_PATTERN = "%d/%m/%Y %H:%M:%S"
FILE_DATE_PATTERN = "%d.%m.%Y %H.%M.%S"

CLEAR_COMMAND = "cls" if SYSTEM == "windows" else "clear"
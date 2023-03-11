class GitHubRequestError(Exception):
    def __init__(self, status_code, message):
        self.error_code = status_code

        super().__init__(message)
        
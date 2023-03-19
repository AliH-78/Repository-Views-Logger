import requests
from . import exceptions
import utils.time

class GitHubRequestSession(requests.Session):
    def __init__(self, token, *args, **kwargs):
        self.token = token
    
        super().__init__(*args, **kwargs)

        self.headers = {"Accept" : "application/vnd.github+json",
                        "X-GitHub-Api-Version" : "2022-11-28",
                        "Authorization" : f"Bearer {self.token}"}
    
    def request(self, *args, **kwargs):
        try:
            request = super().request(*args, **kwargs)
        
        except:
            raise exceptions.GitHubRequestError()

        if request.status_code // 100 != 2:
            raise exceptions.GitHubResponseError(request.status_code, f"[{request.status_code}] {request.json()['message']}")
        
        return request

class DictClass:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

        for key, value in self.kwargs.items():
            setattr(self, key, value if not isinstance(value, dict) else DictClass(**value))
    
    def __dict__(self):
        return self.kwargs
        

class Repository(DictClass):
    def __eq__(self, obj):
        if not isinstance(obj, type(self)):
            return False
        
        return self.name == obj.name and self.owner.login == obj.owner.login
   
    def __hash__(self):
        return None

class GitHubUserInformation(DictClass):
    pass

def handle_traffic_information(traffic_information):
    return tuple((utils.time.github_date_string_to_timestamp(i["timestamp"]), i["count"], i["uniques"]) for i in traffic_information["views"][:-1])

def handle_popular_files_information(traffic_information):
    return tuple((utils.time.get_utc_timestamp() - utils.time.to_seconds(days = 15),
                  utils.time.get_utc_timestamp(), i["path"], i["count"], i["uniques"]) for i in traffic_information)

class GitHubAccount:
    def __init__(self, **kwargs):
        if "token" not in kwargs:
            raise ValueError("Account token isn't defined.")
            
        self.user_token = kwargs["token"]
        
        self.github_request_session = GitHubRequestSession(token = self.user_token)

        self.user_information = {}
        self.user_repositories = {}
        
        
        self.query_user_token()

    def query_user_token(self):
        user_api_request = self.github_request_session.get("https://api.github.com/user")
        
        self.user_information = GitHubUserInformation(**user_api_request.json())
    
    def list_all_repositories(self):
        repo_query_api_request = self.github_request_session.get(self.user_information.repos_url)

        self.user_repositories = repo_query_api_request.json()
        self.user_repositories = [Repository(**repository) for repository in self.user_repositories]

        return self.user_repositories
    
    def select_repository(self, repository_name):
        repository_query_request =  self.github_request_session.get(f"https://api.github.com/repos/{self.user_information.login}/{repository_name}")
        
        return Repository(**repository_query_request.json())
    
    def get_view_count(self, repository):
        scrape_traffic_view_request = self.github_request_session.get(f"{repository.url}/traffic/views")

        return handle_traffic_information(scrape_traffic_view_request.json())
    
    def get_popular_files_views(self, repository):
        scrape_traffic_view_request = self.github_request_session.get(f"{repository.url}/traffic/popular/paths")

        return handle_popular_files_information(scrape_traffic_view_request.json())

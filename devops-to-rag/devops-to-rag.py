import os  
import requests  
import zipfile  
from datetime import datetime  
from requests.auth import HTTPBasicAuth  
from requests.adapters import HTTPAdapter  
from urllib3.util.retry import Retry  
  
class DevOpsRepoManager:  
    def __init__(self, organization, project, pat):  
        assert isinstance(organization, str), "organization must be a string"  
        assert isinstance(project, str), "project must be a string"  
        assert isinstance(pat, str), "pat must be a string"  
          
        self.organization = organization  
        self.project = project  
        self.pat = pat  
        self.base_url = f'https://dev.azure.com/{self.organization}/{self.project}/_apis/git'  
        self.auth = HTTPBasicAuth('', self.pat)  
        self.headers = {  
            'Content-Type': 'application/json'  
        }  
  
        self.session = requests.Session()  
        retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])  
        self.session.mount('https://', HTTPAdapter(max_retries=retries))  
  
    def download_repo(self, repo_name, branch_name, download_path):  
        """ This method downloads a repository from Azure DevOps to the specified path.  
        Inputs:  
            repo_name(str): The name of the repository to download.  
            branch_name(str): The name of the branch to download.  
            download_path(str): The path where the repository will be downloaded.  
        Outputs:  
            None  
        """  
        assert isinstance(repo_name, str), "repo_name must be a string"  
        assert isinstance(branch_name, str), "branch_name must be a string"  
        assert os.path.isdir(download_path), "download_path must be a valid directory"  
  
        repo_url = f'https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories/{repo_name}/items/items?path=/&versionDescriptor[versionOptions]=0&versionDescriptor[versionType]=0&versionDescriptor[version]={branch_name}&resolveLfs=true&$format=zip&api-version=5.0&download=true'  
  
        response = self.session.get(repo_url, auth=self.auth, headers=self.headers)  
  
        if response.status_code == 200:  
            zip_path = os.path.join(download_path, f'{repo_name}.zip')  
            with open(zip_path, 'wb') as file:  
                file.write(response.content)  
            print(f'Repository {repo_name} downloaded successfully to {zip_path}')  
  
            # Unzipping the repository  
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
                zip_ref.extractall(f"{download_path}/{repo_name}")  
            print(f'Repository {repo_name} unzipped successfully to {download_path}')  
  
            # Deleting the zip file after unzipping  
            os.remove(zip_path)  
            print(f'Zip file {zip_path} deleted successfully')  
        else:  
            print(f'Failed to download repository {repo_name}: {response.status_code} - {response.text}')  
  
    def list_repos(self):  
        """ This method lists all the repositories in the project.  
        Inputs:  
            None  
        Outputs:  
            repositories(List[str]): A list of the repositories in the project."""  
        repos_url = f'{self.base_url}/repositories?api-version=6.0'  
  
        response = self.session.get(repos_url, auth=self.auth, headers=self.headers)  
  
        if response.status_code == 200:  
            repos = response.json()['value']  
            print('Successfully retrieved repositories')  
            for repo in repos:  
                print(f"- {repo['name']}")  
        else:  
            print(f'Failed to list repositories: {response.status_code} - {response.text}')  
            repos = []  
        return [repo['name'] for repo in repos]  
  
    def crawl_and_ingest_files(self, downloaded_directory_path, repository_name, allowed_file_extensions):  
        """  
        This method crawls a directory and ingests all files with a specific extension into a list of dictionaries. The aim of this method to parse all the relevant information in a given repository into a format that can easily be further processed and provided as a input to a RAG application.  
        Inputs:  
         - volume_path(string): The path to the ingested repository  
         - repository_name(string): The name of the repository  
         - file_extension(List[string]): A list of file extensions to be ingested. Any file that doesn't have the given extension is ignored by the method.  
        """  
        assert os.path.isdir(downloaded_directory_path), "volume_path must be a valid directory"  
        assert isinstance(repository_name, str), "repository_name must be a string"  
        assert isinstance(allowed_file_extensions, list) and all(isinstance(ext, str) for ext in allowed_file_extensions), "allowed_file_extensions must be a list of strings"  
  
        directory_path = f"{downloaded_directory_path}/{repository_name}"  
        ingested_files = []  
  
        ingestion_date = datetime.now()  
        for root, _, files in os.walk(directory_path):  
            for file in files:  
                file_extension = file.split('.')[-1]  
                if file_extension in allowed_file_extensions:  
                    file_path = os.path.join(root, file)  
                    relative_path = os.path.relpath(file_path, directory_path)  
  
                    with open(file_path, 'r', encoding='utf-8') as f:  
                        content = f.read()  
  
                    ingested_files.append({  
                        'repository_name' : repository_name,  
                        'path': relative_path,  
                        'content': content,  
                        'ingestion_date': ingestion_date  
                    })  
        return ingested_files  

import requests  
import os  
from requests.auth import HTTPBasicAuth  
import zipfile

from datetime import datetime
  
class DevOpsRepoManager:  
    def __init__(self, organization, project, pat):  
        self.organization = organization  
        self.project = project  
        self.pat = pat  
        self.base_url = f'https://dev.azure.com/{self.organization}/{self.project}/_apis/git'  
        self.auth = HTTPBasicAuth('', self.pat)  
        self.headers = {  
            'Content-Type': 'application/json'  
        }

      
    def download_repo(self, repo_name, branch_name, databricks_volume_path):  
        repo_url = f'https://dev.azure.com/{self.organization}/{self.project}/_apis/git/repositories/{repo_name}/items/items?path=/&versionDescriptor[versionOptions]=0&versionDescriptor[versionType]=0&versionDescriptor[version]={branch}&resolveLfs=true&$format=zip&api-version=5.0&download=true'
        response = requests.get(repo_url, auth=self.auth, headers=self.headers)  
        
          
        if response.status_code == 200:  
            zip_path = os.path.join(databricks_volume_path, f'{repo_name}.zip')  
            with open(zip_path, 'wb') as file:  
                file.write(response.content)  
            print(f'Repository {repo_name} downloaded successfully to {zip_path}')  
              
            # Unzipping the repository  
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:  
                zip_ref.extractall(f"{databricks_volume_path}/{repo_name}")  
            print(f'Repository {repo_name} unzipped successfully to {databricks_volume_path}')  
              
            # Deleting the zip file after unzipping  
            os.remove(zip_path)  
            print(f'Zip file {zip_path} deleted successfully')  
        else:  
            print(f'Failed to download repository {repo_name}: {response.status_code} - {response.text}')    
      
    def list_repos(self):  
        repos_url = f'{self.base_url}/repositories?api-version=6.0'  
        response = requests.get(repos_url, auth=self.auth, headers=self.headers)  
          
        if response.status_code == 200:  
            repos = response.json()['value']  
            print('Repositories in the project:')  
            for repo in repos:  
                print(f"- {repo['name']}")  
        else:  
            print(f'Failed to list repositories: {response.status_code} - {response.text}')
# DevOpsConnector README  
   
## Overview  
   
`devops_to_rag` is a Python class designed to interact with Azure DevOps repositories for providing the information in a format that can easily be ingested for a vector search database. It provides methods to list repositories, download repositories, and ingest files from a repository. <b> Note: The current version only works with Azure DevOps 
   
   
## Usage  
   
### Initialization  
   
To use the `devops_to_rag`, you need to initialize it with your Azure DevOps organization name, project name, and Personal Access Token (PAT).  
   
```python  
from devops_to_rag import DevOpsConnector  
   
# Replace with your Azure DevOps organization, project, and PAT  
organization = 'your_organization'  
project = 'your_project'  
pat = 'your_pat'  
   
connector = DevOpsConnector(organization, project, pat)  
```  
   
### List Repositories  
   
To list all repositories in the specified project:  
   
```python  
repositories = connector.list_repos()  
print(repositories)  
```  
   
### Download Repository  
   
To download a specified repository and branch to a local directory:  
   
```python  
repo_name = 'your_repo_name'  
branch_name = 'your_branch_name'  
download_path = 'path/to/download/directory'  
   
connector.download_repo(repo_name, branch_name, download_path)  
```  
   
### Ingest Files  
   
To ingest files with specific extensions from the downloaded repository:  
   
```python  
downloaded_directory_path = 'path/to/download/directory'  
repository_name = 'your_repo_name'  
allowed_file_extensions = ['py', 'md']  # List of allowed file extensions  
   
ingested_files = connector.crawl_and_ingest_files(downloaded_directory_path, repository_name, allowed_file_extensions)  
print(ingested_files)  
```  
   
## Methods  
   
### `__init__(self, organization, project, pat)`  
   
Initializes the `DevOpsConnector` instance.  
   
- **organization (str)**: The name of the Azure DevOps organization.  
- **project (str)**: The name of the Azure DevOps project.  
- **pat (str)**: The Personal Access Token for authentication.  
   
### `download_repo(self, repo_name, branch_name, download_path)`  
   
Downloads a repository from Azure DevOps to the specified path.  
   
- **repo_name (str)**: The name of the repository to download.  
- **branch_name (str)**: The name of the branch to download.  
- **download_path (str)**: The path where the repository will be downloaded.  
   
### `list_repos(self)`  
   
Lists all the repositories in the project.  
   
- **Returns (List[str])**: A list of the repositories in the project.  
   
### `crawl_and_ingest_files(self, downloaded_directory_path, repository_name, allowed_file_extensions)`  
   
Crawls a directory and ingests all files with specific extensions into a list of dictionaries.  
   
- **downloaded_directory_path (str)**: The path to the downloaded repository.  
- **repository_name (str)**: The name of the repository.  
- **allowed_file_extensions (List[str])**: A list of file extensions to be ingested.  
   
- **Returns (List[Dict])**: A list of dictionaries containing the ingested files' information.  
   
## Examples  
   
Here are a few examples to demonstrate the usage of the `DevOpsConnector` class.  
   
### Example 1: List Repositories  
   
```python  
connector = DevOpsConnector('your_organization', 'your_project', 'your_pat')  
repositories = connector.list_repos()  
for repo in repositories:  
    print(repo)  
```  
   
### Example 2: Download Repository  
   
```python  
connector = DevOpsConnector('your_organization', 'your_project', 'your_pat')  
connector.download_repo('your_repo_name', 'your_branch_name', '/path/to/download/directory')  
```  
   
### Example 3: Ingest Files  
   
```python  
connector = DevOpsConnector('your_organization', 'your_project', 'your_pat')  
ingested_files = connector.crawl_and_ingest_files('/path/to/download/directory', 'your_repo_name', ['py', 'md'])  
for file in ingested_files:  
    print(file)  
```  
   
## Error Handling  
   
The class methods print error messages if they fail to perform the intended operations. Ensure that the provided organization, project, PAT, repository name, branch name, and paths are correct to avoid errors.  
   
## Contributions  
   
Contributions are welcome! Please fork the repository and submit a pull request.  
   
## License  
   
This project is licensed under the GNU GENERAL PUBLIC LICENSE Version 3 .  
   

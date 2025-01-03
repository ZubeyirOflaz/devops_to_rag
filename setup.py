from setuptools import setup, find_packages  
  
setup(  
    name='devops-to-rag',  
    version='0.1.0',  
    author='Zübeyir Oflaz',  
    author_email='zubeyir.oflaz@gmail.com',  
    description='A Python library to manage Azure DevOps repositories.',  
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',  
    url='https://github.com/ZubeyirOflaz/devops_to_rag',  
    packages=find_packages(),  
    install_requires=[  
        'requests',  
    ],  
    classifiers=[  
        'Programming Language :: Python :: 3',  
        'License :: OSI Approved :: MIT License',  
        'Operating System :: OS Independent',  
    ],  
    python_requires='>=3.10',  
)  
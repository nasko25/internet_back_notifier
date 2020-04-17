## Description
A simple python script that will hopefully run in the background and checks if the host is connected to the internet. If there is a network problem, the script will notify the user when the connection is back up. For now the script only works if there is not internet and exits when the connection is back up.
    
Article/url resource downloader will be added in the future.
## How to run it
First clone the repository
```bash
git clone $url_of_repo
```
Go in the repo folder, give permissions to execute the script, and execute it
```bash
cd <repo_name>
chmod +x when_is_my_wifi_back
./wifi_notifier.py
``` 

## Requirements 
`python3.7` or later and `pip`
To download the requirements run
```
pip install -r requirements.txt
```

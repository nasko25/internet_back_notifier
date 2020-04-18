## Description
A simple python script that checks if the clinet is connected to the internet. If there is a network problem, the script will notify the user when the connection is back up. Since I occasionally have network connectivity issues, I decided to write this script to tell me whenever my internet connection is back, so I don't have to constantly try to access some internet resource myself to find if the internet is back.
    
I also figured that while I have no network connection, I cannot read online blogposts or articles, so I decided to add a feature that downloads the html files from given urls, so that I can access them offline if at some point I get disconnected from the internet. 
    
The script will download html files linked in the `urls_to_download.txt` file and will delete them, when they are deleted from the file. 
You could also specify your own file with urls and output directory (see the help page for more information and the comments in the `urls_to_download.txt` file).

## How to run it
First clone the repository
```bash
git clone $url_of_repo
```
Go in the repo folder, give permissions to execute the script, and execute it
```bash
cd internet_back_notifier
chmod +x wifi_notifier.py
./wifi_notifier.py
``` 
You can also type 
```bash
./wifi_notifier.py --help
```
to see the help page and find more information about the parameters that you can use.

## Requirements 
`python3` or later and `pip`
To download the requirements run
```
pip install -r requirements.txt
```

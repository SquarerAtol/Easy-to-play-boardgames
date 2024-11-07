# Flask web service upload and play html5 games
Developed by [SquarerAtol](github.com/SquarerAtol)

## Caution
Upload file allowed "html,css,js,jpeg,jpg,png"

If you upload any file in this project
then make new directory ```src/files/game_file```
### Mac/Linux
```
$ python3 -m venv venv
$ source venv/bin/activate
```
### Windows
```
> PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser
```
```
> python -m venv venv
> venv\Scripts\Activate.ps1
```
### INI
```
$ pip install -r requirements.txt
```
### DB init
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
### Run
```
$ flask run
```

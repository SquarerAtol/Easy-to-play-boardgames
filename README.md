# flask web service upload and play html5 games
developed by [SquarerAtol](github.com/SquarerAtol)

## caution
upload file allowed "html,css,js,jpeg,jpg,png"

file path: src/files/game_file
### mac/linux
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
### ini
```
$ cp -p .env.local .env
```
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

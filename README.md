# Flask web platform service for HTML5 games
2024 capstone design

## Caution
게임을 업로드하기 위해 디렉토리를 생성해야 합니다. ```src/files/game_file```

#### Single HTML file
단일 HTML 파일에 포함된 간단한 프로젝트의 경우 압축하지 않고 파일을 직접 업로드할 수 있습니다.

#### Zip file
게임이 단일 파일 이상인 경우 zip 파일로 업로드해야 합니다. zip 파일의 최상위 폴더에 게임의 진입점인 index.html 파일이 포함되어야 합니다. zip 파일에는 게임을 실행하는 데 필요한 모든 파일도 포함되어야 합니다.



## Instruction
project 실행 설명서
### VENV
Mac/Linux
```
$ python3 -m venv venv
$ source venv/bin/activate
```
Windows
```
> PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser
```
```
> python -m venv venv
> venv\Scripts\Activate.ps1
```
### installation
Python의 설치를 필요로 합니다.
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

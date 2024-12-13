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
## feature
src/app.py : 어플리케이션 실행 파일입니다.


src/config.py : 환경설정 파일입니다.


src/*/views.py : 비즈니스 도메인에 따라 분류하여 도메인의 기능 작동을 기술한 파일입니다.


src/*/templates/*.py : 화면에 출력 될 Jinja 기반의 html 파일입니다.


src/*/model.py : 데이터베이스에 입력 할 테이블 설정입니다.
### 15주차 수정사항


forum의 게시물에 답글을 적을 수 있는 reply 기능을 추가했습니다.


forum의 게시물을 5개까지 표현하고 다음 페이지로 넘기는 paging 처리를 추가했습니다.
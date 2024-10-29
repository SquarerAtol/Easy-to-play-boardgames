$ python3 -m venv venv
$ source venv/bin/activate

> PowerShell Set-ExecutionPolicy RemoteSigned CurrentUser

> py -m venv venv
> venv\Scripts\Activate.ps1

$ cp -p .env.local .env

(venv) $ pip install -r requirements.txt

(venv) $ flask db init
(venv) $ flask db migrate
(venv) $ flask db upgrade
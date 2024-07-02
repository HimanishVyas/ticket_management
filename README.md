# NuVu Conair CRM
### Main repo of NuVu Conair CRM Project

![https://github.com/ambv/black](https://img.shields.io/badge/code%20style-black-000000.svg)
[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
![interrogate]()

![pre-commit_flow](https://user-images.githubusercontent.com/28834720/132936889-b12582e3-02dd-49b6-81cd-a50fc5b18c7c.png)


## commands for project setup

#### to store git password in your system
```
git config --global credential.helper store
```
#### then perform any remote command it will automatically store creds
```
git clone 
```

```
cd nvc_crm
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```
### paste .env file in the level of the ```manage.py``` file

#### check whether project is running
```
./manage.py runserver
```
```
pre-commit autoupdate
pre-commit install
```
### output should be
```pre-commit installed at .git/hooks/pre-commit```

### note: to skip pre-commit check (only in exceptional cases)
```
git commit -m 'message' --no-verify
```

### create a new local branch from remote branch
#### work in your personal branch only
```
git fetch origin
git checkout -b name-dev origin/name-dev
```


## Postman collection


## Figma link
[![Figma](https://www.figma.com/file/0FWgdCasp0EvH0NSOAcFnW/Nu-Vu-ConAir?type=design&node-id=0-1&t=AF7zfMM0RqyPrAqU-0)
[![Figma](https://www.figma.com/file/0FWgdCasp0EvH0NSOAcFnW/Nu-Vu-ConAir?type=design&node-id=0-1&t=0QgfsOgMggtJJAIm-0)

## Flowchart
#### (https://miro.com/app/board/uXjVMaGnb7o=/)

## FRD
#### (https://docs.google.com/document/d/1blF_fabMS5MA0yTPd1mHpyyfBldp-KfaWtRJ9gEaI1c/edit#heading=h.20tf212ky5fh)
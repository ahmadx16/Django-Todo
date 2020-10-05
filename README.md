# TODO Application

## Instructions

Following are the instructions that you need perform in order to run the application

1. [Clone the repository](#cloning-the-repository)
1. [Python Environment Setup](#python-environment-setup)
1. [Launching the Application](#launching-the-application)

## Cloning the Repository

Clone this repository and switch to the `ahmedhasan-todolist` branch as it currently contains the latest code. Run the following commands on your shell

``` shell
git clone https://github.com/ahmadx16/Django-Todo.git
cd Django-Todo/
git checkout custom-user-authentication
```

The above commands will download the repository and switch the branch.

## Python Environment Setup

It is recommended to create a virtual environment before installing django. This project uses [virtualenv](https://pypi.org/project/virtualenv/) for this purpose. You can create a python virtual environment by giving path where you want to create a virtual environment and run following commands.

``` shell
python3 -m venv /path-to-new-virtual-environment
source /path-to-new-virtual-environment/bin/activate
```
The above commands will create and activate a new virtual environment. Learn more about virtual environment virtualenv [here](https://pypi.org/project/virtualenv/).

Now install application requirements using following command.

``` shell
pip install -r requirements.txt
```

## Launching the Application

Before launching the application run the following command on terminal.

``` shell
python manage.py migrate
```

This command will create the database tables that we have specified in the models of our application.

Now run command.

``` shell
python manage.py runserver
```

This command will start the application server at 127.0.0.1:8000

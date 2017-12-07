start venv
~/workspace/sahola/
        . venv/bin/activate

start flask
~/workspace/sahola/app/
        FLASK_APP=__init__.py
        flask run

start phpliteadmin
~/workspace/sahola/
        phpliteadmin app.db

create datebase
chmod a+x db_create.py

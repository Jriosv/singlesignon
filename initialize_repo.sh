#!/bin/sh -e

if [ $# -eq 0 ]; then
  ve_dir=ve
else
  ve_dir="$1"
fi

if [ ! -d "$ve_dir" ]; then
  python -m venv "$ve_dir"
fi

"$ve_dir"/Scripts/pip install -r requirements.txt

ve/Scripts/python mysite/manage.py migrate
ve/Scripts/python mysite/manage.py flush
ve/Scripts/python mysite/manage.py loaddata mysite/fixtures/data.json


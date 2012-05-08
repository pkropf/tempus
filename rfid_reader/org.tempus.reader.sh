#! /bin/sh 

export WORKON_HOME=~/.virtualenvs
export PYTHONPATH=/usr/local/lib/python2.7/site-packages
export VIRTUALENVWRAPPER_PYTHON=/opt/homebrew/bin/python
. /opt/homebrew/share/python/virtualenvwrapper.sh
workon tempus

cd /Users/peter/projects/tempus/rfid_reader
exec python reader.py

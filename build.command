#! /bin/bash

cd -- "$(dirname "$BASH_SOURCE")"

Clear

rm setup.py
py2applet --make-setup photo_organiser.py /usr/local/bin/exiftool --iconfile PhotoOrganiser.icns


rm -rf build dist
python3 setup.py py2app -A --emulate-shell-environment 

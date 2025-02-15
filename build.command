#! /bin/bash

cd -- "$(dirname "$BASH_SOURCE")"

Clear

pyinstaller --clean --noconfirm --noconsole --icon 'Photo Organiser.png' photo_organiser.py

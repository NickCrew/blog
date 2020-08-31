#!/bin/sh

if ! command -v pelican
then
	source ~/.virtualenvs/pelican/bin/activate
fi
pelican content -s publishconf.py
rsync -avc --delete output/ piggah.xyz:/var/www/html/
deactivate

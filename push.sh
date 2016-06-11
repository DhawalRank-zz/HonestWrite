#!/bin/bash

now=`date`
git init
git add .
git commit -m "$now"
if [ `git remote -v` ]; then
	git push -f origin master
else
	git remote add origin https://github.com/DhawalRank/HonestWrite.git
	git push -f origin master
fi


#!/bin/bash

now=`date`
git init
git add .
git commit -m "$now"
git remote add origin https://github.com/DhawalRank/HonestWrite.git
git push -f origin master

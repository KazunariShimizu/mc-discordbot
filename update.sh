#!/bin/bash

git checkout .
git checkout master
git pull --prune
echo "Please run pip3 install -r requirements.txt"

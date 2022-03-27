#!/usr/bin/env bash

rm -rf booklog.egg-info
pip install --upgrade pip
pip install -r requirements.txt
pip install -e .

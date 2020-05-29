#!/bin/bash

pip3 install -r requirements.txt
nodemon --exec python migrate-service.py
#!/bin/bash

# Script for remote DO builds

set -e

virtualenv virtualenv
source virtualenv/bin/activate
pip install -r requirements.txt
cp ../../../lib/*.py .
deactivate
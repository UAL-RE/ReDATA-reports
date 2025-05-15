#!/bin/bash

doctl serverless deploy . --remote-build --env packages/redata_reports/run/secrets.py
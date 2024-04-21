#!/bin/bash
source venv/bin/activate
exec gunicorn -b 0.0.0.0:8080 index:server
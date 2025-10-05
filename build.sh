#!/usr/bin/env bash
# exit on error
set -o errexit

# Upgrade pip first
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Fix psycopg2 compatibility issue with Python 3.13
pip uninstall -y psycopg2-binary
pip install psycopg2-binary --no-cache-dir

# Initialize database
python init_db.py

#!/usr/bin/env bash
# exit on error
set -o errexit

echo "===== Starting build process ====="

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database
echo "Initializing database..."
python init_db.py || echo "WARNING: Database initialization failed, but continuing..."

echo "===== Build process completed ====="

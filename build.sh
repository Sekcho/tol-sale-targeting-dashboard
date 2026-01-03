#!/usr/bin/env bash
# Don't exit on error for database init
set -o errexit

echo "===== Starting build process ====="

# Upgrade pip first
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Initialize database (allow failure but show warning)
echo "Initializing database..."
if python init_db.py; then
    echo "[OK] Database initialized successfully!"
else
    echo "=========================================="
    echo "WARNING: Database initialization failed!"
    echo "This may cause login errors at runtime."
    echo "Check DATABASE_URL environment variable."
    echo "=========================================="
fi

echo "===== Build process completed ====="

#!/bin/bash
# Stop on error
set -e

echo "🧹 Cleaning public directory..."
rm -rf public

echo "🏗️ Building Hugo site with local base URL..."
# We build with base URL set to localhost:1313 so links don't break during local testing
hugo --baseURL "http://localhost:1313/"

echo "🔒 Running encryption script..."
python3 encrypt.py

echo "🚀 Starting test server on http://localhost:1313/ ..."
python3 -m http.server 1313 -d public

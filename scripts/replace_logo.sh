#!/bin/bash

# Script to replace the old logo files with the new ones

# Make backup directory if it doesn't exist
mkdir -p backup/images
mkdir -p backup/favicon

# Backup existing logo files
echo "Backing up original logo files..."
cp static/images/logo.* backup/images/
cp static/favicon/* backup/favicon/

# Replace logo files in images directory
echo "Replacing logo files in images directory..."
cp static/images/new.logo.svg static/images/logo.svg
cp static/images/new.logo.png static/images/logo.png
cp static/images/new.logo.small.png static/images/logo.small.png

# Replace favicon files
echo "Replacing favicon files..."
cp static/favicon/new/favicon.svg static/favicon/favicon.svg
cp static/favicon/new/favicon.ico static/favicon/favicon.ico
cp static/favicon/new/favicon-16x16.png static/favicon/favicon-16x16.png
cp static/favicon/new/favicon-32x32.png static/favicon/favicon-32x32.png
cp static/favicon/new/android-chrome-192x192.png static/favicon/android-chrome-192x192.png
cp static/favicon/new/android-chrome-512x512.png static/favicon/android-chrome-512x512.png
cp static/favicon/new/apple-touch-icon.png static/favicon/apple-touch-icon.png

echo "Logo replacement complete!"
echo "The old files have been backed up to the backup directory."
echo "If you need to revert, you can run: cp -r backup/* static/" 
#!/bin/bash

# Script to convert the new logo to all necessary formats for the website

# Create output directory if it doesn't exist
mkdir -p static/favicon/new

# Convert SVG to PNG for various favicon sizes
echo "Converting logo to favicon formats..."

# Use Inkscape to convert SVG to PNG (if available), otherwise try convert from ImageMagick
if command -v inkscape &> /dev/null; then
    echo "Using Inkscape for conversion..."
    # Main logo PNG
    inkscape -w 512 -h 512 static/images/new.logo.svg -o static/images/new.logo.png
    
    # Favicons
    inkscape -w 16 -h 16 static/images/new.logo.svg -o static/favicon/new/favicon-16x16.png
    inkscape -w 32 -h 32 static/images/new.logo.svg -o static/favicon/new/favicon-32x32.png
    inkscape -w 192 -h 192 static/images/new.logo.svg -o static/favicon/new/android-chrome-192x192.png
    inkscape -w 512 -h 512 static/images/new.logo.svg -o static/favicon/new/android-chrome-512x512.png
    inkscape -w 180 -h 180 static/images/new.logo.svg -o static/favicon/new/apple-touch-icon.png
    
    # Small logo variant
    inkscape -w 150 -h 150 static/images/new.logo.svg -o static/images/new.logo.small.png
elif command -v convert &> /dev/null; then
    echo "Using ImageMagick for conversion..."
    # Main logo PNG
    convert -background none -resize 512x512 static/images/new.logo.svg static/images/new.logo.png
    
    # Favicons
    convert -background none -resize 16x16 static/images/new.logo.svg static/favicon/new/favicon-16x16.png
    convert -background none -resize 32x32 static/images/new.logo.svg static/favicon/new/favicon-32x32.png
    convert -background none -resize 192x192 static/images/new.logo.svg static/favicon/new/android-chrome-192x192.png
    convert -background none -resize 512x512 static/images/new.logo.svg static/favicon/new/android-chrome-512x512.png
    convert -background none -resize 180x180 static/images/new.logo.svg static/favicon/new/apple-touch-icon.png
    
    # Small logo variant
    convert -background none -resize 150x150 static/images/new.logo.svg static/images/new.logo.small.png
else
    echo "Error: Neither Inkscape nor ImageMagick (convert) are available. Cannot convert images."
    exit 1
fi

# Copy the SVG to favicon directory
cp static/images/new.logo.svg static/favicon/new/favicon.svg

# Generate ICO file (requires ImageMagick)
if command -v convert &> /dev/null; then
    echo "Creating favicon.ico..."
    convert static/favicon/new/favicon-16x16.png static/favicon/new/favicon-32x32.png static/favicon/new/favicon.ico
else
    echo "Warning: ImageMagick not available. Skipping favicon.ico generation."
fi

echo "Conversion complete. New files created in static/favicon/new/"
echo "Please check the generated files and then replace the existing ones if they look good." 
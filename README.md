# Tracking Visual Similarity in Digital Images

This project demonstrates a Python-based prototype for comparing different versions of digital images using perceptual hashing.

## What it does

- Loads multiple versions of an image
- Computes perceptual hashes using ImageHash
- Compares images based on visual similarity
- Outputs results in JSON format
- Generates a webpage to visualize comparisons

## Files

- `versioning_demo.py` — main Python script
- `images/` — input image files
- `version_results.json` — comparison results
- `results.html` — visual output page

## Tools used

- Python
- ImageHash
- Pillow

## How to run

pip install ImageHash Pillow  
python3 versioning_demo.py

## Why this project

This project explores how computational tools can help identify visually similar versions of digital images. This is relevant for digital art, archives, and image version tracking.
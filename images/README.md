# Image Versioning and Visual Similarity Analysis

This project is a Python-based prototype that compares digital images using perceptual hashing in order to measure visual similarity across image versions and unrelated images.

## Project Overview

Digital images often exist in multiple forms, including resized, compressed, edited, or recreated versions. At the same time, visually unrelated images may circulate alongside them. This project explores how computational methods can distinguish between:

- true versions of the same image  
- altered or recreated images  
- completely unrelated images from different genres  

The project focuses on building a ranked comparison centered on a single reference image.

## What the Program Does

The script performs the following steps:

1. Loads a set of images from a folder  
2. Generates a perceptual hash for each image  
3. Compares all images to a designated original image  
4. Calculates similarity using hash distance  
5. Produces a ranked list from most similar to least similar  
6. Outputs results as:
   - a JSON file  
   - a visual HTML webpage  

## Key Concept: Perceptual Hashing

Perceptual hashing creates a visual fingerprint of an image. Unlike traditional file hashing, it measures how an image looks rather than whether two files are identical.

- Distance = 0 → nearly identical  
- Small distance → very similar  
- Large distance → visually different  

## Dataset

The dataset includes:

- Original image  
- Modified versions (resized, compressed, recreated)  
- Unrelated images from different genres such as photography, painting, and digital illustration  

This allows the project to test similarity within and across image categories.

## Output

### 1. Ranked List (Primary Output)

A ranked list comparing all images to the original image, sorted from:

- most similar → least similar  

This helps identify:

- likely versions of the original  
- altered variants  
- unrelated images  

### 2. Web Visualization

The program generates an HTML page (`index.html`) that displays:

- image pairs  
- similarity distance  
- descriptive labels  
- ranking order  

## Technologies Used

- Python  
- Pillow (image processing)  
- ImageHash (perceptual hashing)  
- GitHub (version control and publication)  

## How to Run

## Research Relevance

This project relates to digital humanities and digital art history by addressing the problem of image variation, transformation, and comparison in digital environments.

It demonstrates how computational methods can support:

- visual analysis  
- image version tracking  
- questions of digital provenance  

## Author

Ganiyu Jimoh  ( Jimga )
PhD Candidate, History of Art and Architecture
University of Virginia
Install dependencies:

```bash
pip install pillow imagehash
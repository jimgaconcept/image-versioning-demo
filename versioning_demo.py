from PIL import Image
import imagehash
import os
import json

# Folder containing images
folder = "images"

# List of image records
images = [
    {"filename": "original.jpg", "relation": "original", "genre": "digitized cartoon"},
    {"filename": "resized.jpg", "relation": "version of original", "genre": "ddigitized cartoon"},
    {"filename": "compressed.jpg", "relation": "version of original", "genre": "digitized cartoon"},
    {"filename": "digitally_recreated.jpg", "relation": "recreated image", "genre": "digital cartoon"},
    {"filename": "davidzinyama.jpg", "relation": "unrelated", "genre": "photomontage"},
    {"filename": "stefano.menicagli_artist.jpg", "relation": "unrelated", "genre": "digital illustration"},
    {"filename": "game_of_throne_kano_emirate.jpg", "relation": "unrelated", "genre": "digital cartoon"}
]

results = []

print("\nGenerating perceptual hashes...\n")

# Step 1: Generate a perceptual hash for each image
for item in images:
    file = item["filename"]
    path = os.path.join(folder, file)

    img = Image.open(path)
    phash = imagehash.phash(img)

    results.append({
        "filename": file,
        "relation": item["relation"],
        "genre": item["genre"],
        "phash": str(phash)
    })

    print(f"{file}: {phash}")

# Step 2: Find the original image hash
original_file = "original.jpg"
original_hash = None

for item in results:
    if item["filename"] == original_file:
        original_hash = imagehash.hex_to_hash(item["phash"])
        break

# Step 3: Compare all images to the original
original_ranked = []

if original_hash is not None:
    for item in results:
        if item["filename"] == original_file:
            continue

        current_hash = imagehash.hex_to_hash(item["phash"])
        distance = int(original_hash - current_hash)

        if distance == 0:
            note = "Nearly identical to original"
        elif distance <= 5:
            note = "Very similar to original"
        elif distance <= 10:
            note = "Somewhat similar to original"
        else:
            note = "Different from original"

        original_ranked.append({
            "filename": item["filename"],
            "relation": item["relation"],
            "genre": item["genre"],
            "distance": distance,
            "note": note
        })

# Step 4: Sort from lowest distance to highest
original_ranked.sort(key=lambda x: x["distance"])

# Step 5: Print ranked list in terminal
print("\nRanked list: all images compared to the original\n")

for i, item in enumerate(original_ranked, start=1):
    print(f"{i}. {item['filename']} -> distance {item['distance']} ({item['note']})")

# Step 6: Save results to JSON
output = {
    "hashes": results,
    "original_ranked": original_ranked
}

with open("version_results.json", "w") as f:
    json.dump(output, f, indent=4)

# Step 7: Create HTML page
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image Similarity Ranking</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
            line-height: 1.6;
        }
        h1, h2 {
            text-align: center;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #555;
            margin-top: -10px;
            margin-bottom: 30px;
        }
        .intro {
            background: white;
            padding: 25px;
            margin-bottom: 30px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .comparison {
            background: white;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
            max-width: 900px;
            margin-left: auto;
            margin-right: auto;
        }
        .images {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            margin-bottom: 15px;
            flex-wrap: wrap;
            justify-content: center;
        }
        .images div {
            text-align: center;
            width: 320px;
        }
        img {
            max-width: 300px;
            max-height: 300px;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        .score {
            font-size: 18px;
            font-weight: bold;
            text-align: center;
        }
        .note {
            font-size: 16px;
            color: #333;
            margin-bottom: 10px;
            text-align: center;
        }
        .meta {
            font-size: 14px;
            color: #555;
        }
        ul {
            max-width: 800px;
            margin: 0 auto;
        }
    </style>
</head>
<body>

    <h1>Image Similarity Ranking</h1>
    <p class="subtitle">A computational approach to visual similarity and digital image transformation</p>

    <div class="intro">
        <h2>Project Overview</h2>
        <p>
            This project compares a set of digital images to a single reference image called <strong>original.jpg</strong>.
            It uses perceptual hashing to measure visual similarity and ranks all other images from the most similar
            to the least similar.
        </p>

        <h2>How to Read the Results</h2>
        <p>
            Each comparison is based on a distance score. A lower distance means that the image is more visually similar
            to the original. A higher distance means that the image is more visually different.
        </p>
        <ul>
            <li><strong>0</strong> = nearly identical to the original</li>
            <li><strong>1–5</strong> = very similar to the original</li>
            <li><strong>6–10</strong> = somewhat similar to the original</li>
            <li><strong>Above 10</strong> = different from the original</li>
        </ul>

        <h2>Research Relevance</h2>
        <p>
            This project relates to digital humanities and digital art history by addressing how digital images circulate in multiple
            versions and how computational methods can help distinguish close variants from unrelated works. It demonstrates how
            perceptual hashing can support visual analysis, image version tracking, and broader questions of transformation and
            digital provenance.
        </p>
    </div>
"""

for idx, item in enumerate(original_ranked, start=1):
    html += f"""
    <div class="comparison">
        <div class="score">Rank: {idx}</div>
        <div class="score">Distance from original: {item['distance']}</div>
        <div class="note">{item['note']}</div>
        <div class="images">
            <div>
                <p><strong>original.jpg</strong></p>
                <img src="images/original.jpg" alt="original.jpg">
                <p class="meta">Relation: original</p>
                <p class="meta">Genre: digital artwork</p>
            </div>
            <div>
                <p><strong>{item['filename']}</strong></p>
                <img src="images/{item['filename']}" alt="{item['filename']}">
                <p class="meta">Relation: {item['relation']}</p>
                <p class="meta">Genre: {item['genre']}</p>
            </div>
        </div>
    </div>
    """

html += """
</body>
</html>
"""

with open("index.html", "w") as f:
    f.write(html)

print("\nSaved results to version_results.json")
print("Saved web page to index.html\n")
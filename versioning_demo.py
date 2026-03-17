from PIL import Image
import imagehash
import os
import json

folder = "images"

files = [
    "original.jpg",
    "resized.jpg",
    "digitally_recreated.jpg",
    "compressed.jpg"
]

results = []

print("\nGenerating perceptual hashes...\n")

for file in files:
    path = os.path.join(folder, file)

    img = Image.open(path)
    phash = imagehash.phash(img)

    results.append({
        "filename": file,
        "phash": str(phash)
    })

    print(f"{file}: {phash}")

print("\nComparing images...\n")

comparisons = []

for i in range(len(results)):
    for j in range(i + 1, len(results)):
        file1 = results[i]["filename"]
        file2 = results[j]["filename"]

        hash1 = imagehash.hex_to_hash(results[i]["phash"])
        hash2 = imagehash.hex_to_hash(results[j]["phash"])

        distance = int(hash1 - hash2)

        if distance == 0:
            note = "Nearly identical"
        elif distance <= 5:
            note = "Very similar"
        elif distance <= 10:
            note = "Somewhat similar"
        else:
            note = "Different"

        comparisons.append({
            "file1": file1,
            "file2": file2,
            "distance": distance,
            "note": note
        })

        print(f"{file1} vs {file2} -> {distance} ({note})")

comparisons.sort(key=lambda x: x["distance"], reverse=True)

output = {
    "hashes": results,
    "comparisons": comparisons
}

with open("version_results.json", "w") as f:
    json.dump(output, f, indent=4)

html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Image Comparison Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }
        h1 {
            text-align: center;
        }
        .comparison {
            background: white;
            padding: 20px;
            margin-bottom: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }
        .images {
            display: flex;
            gap: 20px;
            margin-top: 15px;
            margin-bottom: 15px;
        }
        .images div {
            text-align: center;
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
        }
        .note {
            font-size: 16px;
            color: #333;
        }
    </style>
</head>
<body>
    <h1>Image Version Comparison Results</h1>
"""

for item in comparisons:
    html += f"""
    <div class="comparison">
        <div class="score">Distance: {item['distance']}</div>
        <div class="note">{item['note']}</div>
        <div class="images">
            <div>
                <p>{item['file1']}</p>
                <img src="images/{item['file1']}" alt="{item['file1']}">
            </div>
            <div>
                <p>{item['file2']}</p>
                <img src="images/{item['file2']}" alt="{item['file2']}">
            </div>
        </div>
    </div>
    """

html += """
</body>
</html>
"""

with open("results.html", "w") as f:
    f.write(html)

print("\nSaved results to version_results.json")
print("Saved web page to results.html\n")
import xml.etree.ElementTree as ET
import time
import csv
import os

def parse_dom(xml_path):
    start = time.time()

    tree = ET.parse(xml_path)
    root = tree.getroot()

    nodeList = []

    for node in root.findall("node"):
        tags = {}
        for tag in node.findall("tag"):
            tags[tag.get("k")] = tag.get("v")

        # ✅ MESMO FILTRO
        if "amenity" in tags and "name" in tags:
            nodeList.append({
                "name": tags["name"],
                "amenity": tags["amenity"],
                "lat": float(node.get("lat")),
                "lon": float(node.get("lon"))
            })

    elapsed = time.time() - start
    return nodeList, elapsed


def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "amenity", "lat", "lon"])
        writer.writeheader()
        writer.writerows(data)


def main():
    base_dir = os.path.dirname(__file__)
    xml_path = os.path.join(base_dir, "resources", "map2.xml")
    
    print("🔄 Running DOM...")
    dom_data, dom_time = parse_dom(xml_path)

    print(f"✔ DOM encontrou {len(dom_data)} estabelecimentos")
    print(f"⏱ Tempo DOM: {dom_time:.4f}s")

    save_csv(dom_data, "dom_output.csv")


if __name__ == "__main__":
    main()
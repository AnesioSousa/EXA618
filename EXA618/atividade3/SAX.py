import os
import xml.sax
import csv
import time

class Listener(xml.sax.ContentHandler):
    def __init__(self):
        self.nodeList = []
        self.currentNode = None

    def startElement(self, tag, attributes):
        if tag == "node":
            self.currentNode = {
                "id": attributes.get("id"),
                "lat": float(attributes.get("lat")),
                "lon": float(attributes.get("lon")),
                "tags": {}
            }

        elif tag == "tag" and self.currentNode:
            k = attributes.get("k")
            v = attributes.get("v")
            self.currentNode["tags"][k] = v

    def endElement(self, tag):
        if tag == "node":
            tags = self.currentNode["tags"]

            # ✅ FILTRO PRINCIPAL
            if "amenity" in tags and "name" in tags:
                self.nodeList.append({
                    "name": tags["name"],
                    "amenity": tags["amenity"],
                    "lat": self.currentNode["lat"],
                    "lon": self.currentNode["lon"]
                })

            self.currentNode = None


def parse_sax(xml_path):
    start = time.time()

    parser = xml.sax.make_parser()
    handler = Listener()
    parser.setContentHandler(handler)
    parser.parse(xml_path)

    elapsed = time.time() - start
    return handler.nodeList, elapsed


def save_csv(data, filename):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "amenity", "lat", "lon"])
        writer.writeheader()
        writer.writerows(data)


def main():
    base_dir = os.path.dirname(__file__)
    xml_path = os.path.join(base_dir, "resources", "map2.xml")

    print("🔄 Running SAX...")
    sax_data, sax_time = parse_sax(xml_path)

    print(f"✔ SAX encontrou {len(sax_data)} estabelecimentos")
    print(f"⏱ Tempo SAX: {sax_time:.4f}s")

    if len(sax_data) < 100:
        print("⚠️ Arquivo não tem 100 estabelecimentos com amenity + name")

    save_csv(sax_data, "sax_output.csv")


if __name__ == "__main__":
    main()
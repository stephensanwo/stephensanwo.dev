import datetime
from xml.etree import ElementTree as ET
import os
from pathlib import Path


def generate_sitemap(
        urls: list[str],
        output_dir: str) -> None:
    # Create the sitemap XML structure
    xml_root = ET.Element('urlset')
    xml_root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')

    print("Generating sitemap...")
    # Loop through the URLs and add each one to the sitemap XML
    for url in urls:
        xml_url = ET.SubElement(xml_root, 'url')
        ET.SubElement(xml_url, 'loc').text = url
        ET.SubElement(
            xml_url, 'lastmod').text = datetime.date.today().isoformat()

    # Store the sitemap XML in a dist
    ROOT = os.path.dirname(os.path.abspath("./web"))
    Path(os.path.join(ROOT, output_dir)).mkdir(parents=True, exist_ok=True)
    with open(os.path.join(ROOT, output_dir, 'sitemap.xml'), 'w+') as f:
        f.write(ET.tostring(
            xml_root,
            encoding='UTF-8',
            method='xml', xml_declaration=True).decode('UTF-8'),
        )

import datetime
import os
import xml.etree.ElementTree as ET


class RSS():

    def __init__(self):
        # Create the root element of the RSS feed
        self.rss = ET.Element('rss')
        self.rss.set('version', '2.0')

        # Create the channel element
        self.channel = ET.SubElement(self.rss, 'channel')

        # Set the channel metadata
        title = ET.SubElement(self.channel, 'title')
        title.text = "Stephen Sanwo - Engineering Blog"

        link = ET.SubElement(self.channel, 'link')
        link.text = 'https://stephensanwo.dev'

        language = ET.SubElement(self.channel, 'language')
        language.text = 'en-US'

        description = ET.SubElement(self.channel, 'description')
        description.text = 'I write about Distributed Software Systems, \
        APIs and Microservices, Software Development, Machine Learning, \
        Deep Learning & Artificial intelligence, Web & Mobile Development'

        lastBuildDate = ET.SubElement(self.channel, 'lastBuildDate')
        lastBuildDate.text = datetime.datetime.now(
        ).strftime('%a, %d %b %Y %H:%M:%S %Z')

    def generate_rss(self, title: str, link: str, description: str) -> None:
        # Create an item
        item = ET.SubElement(self.channel, 'item')
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = link
        ET.SubElement(item, 'language').text = 'en-US'
        ET.SubElement(item, 'description').text = description
        ET.SubElement(item, 'pubDate').text = datetime.datetime.now().strftime(
            '%a, %d %b %Y %H:%M:%S %Z')

    async def build_rss(self, output_dir: str) -> None:
        # Store the sitemap XML in a s3
        with open(os.path.join(output_dir, 'rss.xml'), 'w+') as f:
            f.write(ET.tostring(
                self.rss,
                encoding='UTF-8',
                method='xml',
                xml_declaration=True).decode('UTF-8'))

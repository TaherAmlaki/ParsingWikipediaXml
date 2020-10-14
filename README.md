# Parsing Wikipedia Xml Dump

In this small project, I created a pipeline using multiprocessing and threading packages in Python, in order
to parse english wikipedia's xml dump file, process the articles and store the result in text files for later usage.
For parser I have xml.sax ContentHandler and xml.etree.ElementTree iterparser, both can be used. The design of my pipeline is as follows:

![Wikipedia Xml Dump Pipeline](https://github.com/TaherAmlaki/ParsingWikipediaXml/blob/main/wiki_xml_pipeline.png?raw=true)

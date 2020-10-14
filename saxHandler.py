import xml.sax


class CustomContentHandler(xml.sax.handler.ContentHandler):
    def __init__(self, queue, shutdown_event):
        self._queue = queue 
        self._shutdown_event = shutdown_event
        self._page = None
        self._tags_stack = None
        self._ns = None 

    def startElement(self, name, attrs):
        if name == "page":
            self._page = ""
            self._tags_stack = []

        if self._page is not None:
            self._tags_stack.append(name)

    def endElement(self, name):
        if self._page is not None:
            if self._tags_stack[-1] == "page":
                if self._ns is not None and self._ns == 0:
                    self._queue.put(self._page)
                self._page = None 
                self._tags_stack = None 
                self._ns = None 
            else:
                del self._tags_stack[-1]

    def characters(self, content):
        if self._page is not None:
            if self._tags_stack[-1] == "text":
                self._page += content
            elif self._tags_stack[-1] == "ns":
                self._ns = int(content)

    def endDocument(self):
        self._shutdown_event.set()

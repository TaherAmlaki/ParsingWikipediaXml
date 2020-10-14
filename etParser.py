import xml.etree.ElementTree as ET


class ETParser:
    def __init__(self, file_obj, queue, shutdown_event):
        self._file_obj = file_obj
        self._queue = queue 
        self._shutdown_event = shutdown_event
        self._page = None
        self._ns = None 
        self._tags_stack = None

    def parse(self):
        for event, element in ET.iterparse(self._file_obj, events=('start', 'end')):
            tag_name = element.tag.rsplit("}", 1)[-1].strip()

            if event == "start":
                if tag_name == "page":
                    self._page = ""
                    self._tags_stack = []

                if self._page is not None:
                    self._tags_stack.append(tag_name) 
            else:

                if self._page is not None:
                    if self._tags_stack[-1] == "text":
                        text = element.text 
                        if text is not None:
                            self._page += element.text 
                    elif self._tags_stack[-1] == "ns": 
                        if element.text is not None:
                            self._ns = int(element.text)
                    
                    if self._tags_stack[-1] == "page":
                        if self._page is not None and self._ns is not None and self._ns == 0:
                            self._queue.put(self._page)
                        self._page = None 
                        self._ns = 0
                        self._tags_stack = None 
                    else:
                        del self._tags_stack[-1]
            element.clear()

        print("===> shutdown event is being set in et parser...")
        self._shutdown_event.set()


import re 


def process_entries(read_queue_, output_queue_, shutdown_event):
    avoid_characters = ('[', '*', '-', '|', '=', '<', '{', '!', '}', '#', ':', ';')
    redirect_pattern = re.compile("#REDIRECT", re.IGNORECASE)

    while not (shutdown_event.is_set() and read_queue_.empty()):
        if not read_queue_.empty():
            page = read_queue_.get()
            if not bool(redirect_pattern.match(page)):
                for line in page.split("\n"):
                    line = line.strip()
                    if line and line[0] not in avoid_characters:
                        output_queue_.put((line, False))
                output_queue_.put(("", True)) 
    print("==> exiting from process page while loop")       

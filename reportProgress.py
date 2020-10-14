import time 
from datetime import timedelta


def print_info(report_queue, process_shutdown_event):

    start = time.time()
    print("starting with reading, processing and writting ...")
    number_of_pages = 0

    while not (process_shutdown_event.is_set() and report_queue.empty()):
        if not report_queue.empty():
            number_of_pages += report_queue.get()
            if number_of_pages % 10000 == 0 and number_of_pages != 0:
                now = time.time()
                delta = now - start
                velocity = number_of_pages / delta  
                remainig_time = (20_620_000 - number_of_pages) / velocity
                delta = str(timedelta(seconds=delta))
                remainig_time = str(timedelta(seconds=remainig_time))
                print(f"{number_of_pages} pages are written to file in {delta} seconds, expected remaining={remainig_time}") 

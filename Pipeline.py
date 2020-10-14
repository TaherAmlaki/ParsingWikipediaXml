import os
import sys
from multiprocessing import Manager, Process, cpu_count, Event
from threading import Thread
from bz2file import BZ2File
import xml.sax
from saxHandler import CustomContentHandler
from etParser import ETParser
from ProcessRawPages import process_entries
from writeToFile import write_to_file
from reportProgress import print_info
 

# wikipedia dump  https://dumps.wikimedia.org/enwiki/20200920/
if __name__ == "__main__":
    queue_manager = Manager()
    read_queue = queue_manager.Queue(maxsize=2000)
    output_queue = queue_manager.Queue(maxsize=2000)
    report_queue = queue_manager.Queue(maxsize=1000)

    process_shutdown_event = Event()
    write_shutdown_event = Event()

    processes = []
    num_workers = max(1, cpu_count() - 1)
    for p in range(num_workers):
        p = Process(target=process_entries, 
                    args=(read_queue, output_queue, process_shutdown_event))
        p.start()
        processes.append(p)

    cur_dir = os.path.dirname(os.path.realpath(__file__))
    output_files = [open(os.path.join(cur_dir, "./wikipedia_sentences_1.txt"), "w", encoding="utf-8"),
                    open(os.path.join(cur_dir, "./wikipedia_sentences_2.txt"), "w", encoding="utf-8")]

    output_threads = [Thread(target=write_to_file, 
                             args=(output_file, output_queue, report_queue, 
                                   write_shutdown_event, process_shutdown_event)) 
                     for output_file in output_files]
                     
    print_info_thread = Thread(target=print_info, 
                               args=(report_queue, process_shutdown_event))
    
    for output_thread in output_threads:
        output_thread.start()
        
    print_info_thread.start()
    
    wiki_file_obj = BZ2File(os.path.join(cur_dir, "./enwiki-20200920-pages-articles-multistream.xml.bz2"))

    # parsing with xml.sax
    # handler = CustomContentHandler(read_queue, write_shutdown_event)
    # xml.sax.parse(wiki_file_obj, handler)
    
    # parsing with xml.etree.ElementTree 
    et_wiki_parser = ETParser(wiki_file_obj, read_queue, write_shutdown_event)
    et_wiki_parser.parse()

    
    for thread in output_threads:
        thread.join()

    for p in processes:
        p.join()

    print_info_thread.join()


def write_to_file(output_file, output_queue, report_queue,
                  write_shutdown_event, process_shutdown_event):

    while not (write_shutdown_event.is_set() and output_queue.empty()):
        if not output_queue.empty():
            new_line, is_last_line = output_queue.get()
            if is_last_line:
                report_queue.put(1)
            else:
                output_file.write(new_line+"\n")
               
    print("==> exiting write while loop and closing the file")
    output_file.close()
    process_shutdown_event.set()

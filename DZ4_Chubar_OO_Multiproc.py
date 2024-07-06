import multiprocessing
import os
import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def search_keywords_in_files(files, keywords, queue):
    name = multiprocessing.current_process().name
    logger.debug(f'{name} started...')
    results = {keyword: [] for keyword in keywords}
    for file in files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                for keyword in keywords:
                    if keyword in text:
                        results[keyword].append(file)
        else:
            logger.debug(f"File not found: {file}")
    queue.put(results)
    logger.debug(f'{name} finished.')

def multiprocess_search(file_list, keywords):
    processes = []
    queue = multiprocessing.Queue()
    num_processes = min(4, len(file_list))  # Задаємо кількість процесів

    for i in range(num_processes):
        process_files = file_list[i::num_processes]  # Розподіляємо файли між процесами
        process = multiprocessing.Process(target=search_keywords_in_files, args=(process_files, keywords, queue), name=f'Process-{i+1}')
        processes.append(process)
        process.start()

    combined_results = {keyword: [] for keyword in keywords}
    for process in processes:
        process.join()
        results = queue.get()
        for keyword in keywords:
            combined_results[keyword].extend(results[keyword])

    return combined_results

if __name__ == "__main__":
    # Приклад файлів та ключових слів
    file_list = [r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file1.txt", 
                 r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file2.txt", 
                 r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file3.txt"]
    keywords = ["keyword1", "keyword2", "keyword3"]

    start_time = time.time()
    results = multiprocess_search(file_list, keywords)
    end_time = time.time()

    print("Multiprocess results:", results)
    print(f"Multiprocess execution time: {end_time - start_time:.2f} seconds")

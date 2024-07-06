import threading
import os
import time
import logging

logger = logging.getLogger()
stream_handler = logging.StreamHandler()
logger.addHandler(stream_handler)
logger.setLevel(logging.DEBUG)

def search_keywords_in_files(files, keywords, results):
    name = threading.current_thread().name
    logger.debug(f'{name} started...')
    for file in files:
        if os.path.exists(file):
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                for keyword in keywords:
                    if keyword in text:
                        results[keyword].append(file)
        else:
            logger.debug(f"File not found: {file}")
    logger.debug(f'{name} finished.')

def multithreaded_search(file_list, keywords):
    threads = []
    results = {keyword: [] for keyword in keywords}
    num_threads = min(4, len(file_list))  # Задаємо кількість потоків

    for i in range(num_threads):
        thread_files = file_list[i::num_threads]  # Розподіляємо файли між потоками
        thread = threading.Thread(target=search_keywords_in_files, args=(thread_files, keywords, results), name=f'Thread-{i+1}')
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return results

if __name__ == "__main__":
    # Приклад файлів та ключових слів
    file_list = [r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file1.txt", 
                 r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file2.txt", 
                 r"C:\Users\sansa\Repository2024\goit-cs-hw-04\file3.txt"]
    keywords = ["keyword1", "keyword2", "keyword3"]

    start_time = time.time()
    results = multithreaded_search(file_list, keywords)
    end_time = time.time()

    print("Multithreaded results:", results)
    print(f"Multithreaded execution time: {end_time - start_time:.2f} seconds")

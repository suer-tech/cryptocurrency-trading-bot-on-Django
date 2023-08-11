import threading

threads = threading.enumerate()

print("Активные потоки:")
for thread in threads:
    # thread.join()
    print(thread.name)

from threading import Lock

# concurrency.py

# Lock for manipulating reveals (globally accessible)
reveal_lock = Lock()

from threading import Lock

# concurrency.py

# Lock for manipulating reveals (globally accessible)
reveal_lock = Lock()

# Lock for manipulating the rooms data structure
connection_lock = Lock()

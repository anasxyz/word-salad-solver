import nltk
import requests
from nltk.corpus import words
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from collections import deque
import time

# Download necessary resources
nltk.download('words')

# Define grid
grid = [
    ['V', 'E', 'N', 'U'],
    ['P', 'T', 'A', 'S'],
    ['Y', 'U', 'R', 'M'],
    ['R', 'C', 'N', 'E']
]

# Load dictionary words
valid_words = set(word.lower() for word in words.words())
valid_words_by_length = {length: set(word for word in valid_words if len(word) == length) for length in range(1, 16)}

# Directions for BFS (up, down, left, right, and diagonals)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Function to check if a position is valid in the grid
def is_valid(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

# Optimized Trie implementation for storing valid words
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True

# Build Trie for valid words
trie = Trie()
for word in valid_words:
    trie.insert(word)

# Function to perform BFS and find words
def find_words_bfs(x, y, min_length, max_length):
    found_words = set()
    queue = deque([(x, y, grid[x][y].lower(), set([(x, y)]))])  # (x, y, current_word, visited)
    
    while queue:
        cx, cy, current_word, visited = queue.popleft()
        
        # If the current word is valid, add it to found words
        if min_length <= len(current_word) <= max_length and trie.search(current_word):
            found_words.add(current_word)
        
        # Prune exploration if the prefix is invalid
        if len(current_word) > max_length or not trie.starts_with(current_word):
            continue

        # Explore neighbors
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if is_valid(nx, ny) and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny, current_word + grid[nx][ny].lower(), visited.copy()))  # Add the next step to the queue
                visited.remove((nx, ny))  # Remove the visited cell after processing

    return found_words

# Function to perform the word search on the grid using BFS
def word_search(min_length=1, max_length=15):
    global found_words
    found_words = set()

    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                futures.append(executor.submit(find_words_bfs, i, j, min_length, max_length))
        
        # Wait for all the futures to complete
        for future in as_completed(futures):
            found_words.update(future.result())

    return found_words

# Function to check if a word is related to a theme using ConceptNet (caching and optimization)
@lru_cache(maxsize=10000)  # Cache results for efficiency
def is_word_related_to_theme_conceptnet(word, theme, threshold=1):
    url = f"http://api.conceptnet.io/query?node=/c/en/{word}&other=/c/en/{theme}"
    response = requests.get(url).json()
    return len(response.get('edges', [])) > 0

# Function to filter words based on their relation to the theme using multithreading
def filter_words_by_theme(words_list, theme, threshold=1):
    related_words = []
    
    # Using ThreadPoolExecutor to parallelize the checks
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(is_word_related_to_theme_conceptnet, word, theme, threshold): word for word in words_list}
        for future in as_completed(futures):
            word = futures[future]
            if future.result():  # If the word is related to the theme
                related_words.append(word)
                
    return related_words

# Example usage
min_length = 3
max_length = 16
theme = "planet"  # The theme to filter words by

# Find words in the grid using BFS
words_found = word_search(min_length, max_length)
print(f"Words found (length {min_length}-{max_length}):", words_found)

# Filter words based on their relation to the theme
start_time = time.time()
filtered_words = filter_words_by_theme(words_found, theme)
end_time = time.time()
print(f"Words related to the theme '{theme}':", filtered_words)
print(f"Filtering time: {end_time - start_time:.2f} seconds")

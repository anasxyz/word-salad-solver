import nltk
import requests
from nltk.corpus import words
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
from collections import defaultdict
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
valid_words_by_length = defaultdict(set)
for word in valid_words:
    valid_words_by_length[len(word)].add(word)

# Directions for DFS (up, down, left, right, and diagonals)
directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

# Function to check if a position is valid in the grid
def is_valid(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

# Function to search for words starting from a given grid position
def find_words(x, y, current_word, visited, min_length, max_length, found_words):
    if min_length <= len(current_word) <= max_length and current_word in valid_words_by_length[len(current_word)]:
        found_words.add(current_word)

    if len(current_word) > max_length:
        return
  
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and (nx, ny) not in visited:
            visited.add((nx, ny))
            find_words(nx, ny, current_word + grid[nx][ny].lower(), visited, min_length, max_length, found_words)
            visited.remove((nx, ny))

# Function to perform the word search on the grid
def word_search(min_length=1, max_length=15):
    found_words = set()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            visited = set([(i, j)])
            find_words(i, j, grid[i][j].lower(), visited, min_length, max_length, found_words)

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

# Optimized function to reduce redundant requests and speed up filtering
def filter_words_optimized(words_list, theme, threshold=1):
    # Group words by their length (cache hits)
    cached_results = {}
    related_words = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {}
        for word in words_list:
            if word not in cached_results:
                futures[executor.submit(is_word_related_to_theme_conceptnet, word, theme, threshold)] = word

        # Check results for all submitted futures
        for future in as_completed(futures):
            word = futures[future]
            result = future.result()
            cached_results[word] = result
            if result:
                related_words.append(word)

    return related_words

# Example usage
min_length = 3
max_length = 16
theme = "planet"  # The theme to filter words by

# Find words in the grid
words_found = word_search(min_length, max_length)
print(f"Words found (length {min_length}-{max_length}):", words_found)

# Filter words based on their relation to the theme
start_time = time.time()
filtered_words = filter_words_optimized(words_found, theme)
end_time = time.time()
print(f"Words related to the theme '{theme}':", filtered_words)
print(f"Filtering time: {end_time - start_time:.2f} seconds")

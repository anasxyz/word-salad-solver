from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import words
import nltk
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

# Download the words corpus if not already downloaded
nltk.download('words')

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests

# Load the NLTK words into a set for faster look-up
valid_words = set(word.lower() for word in words.words())
valid_words_by_length = {length: set(word for word in valid_words if len(word) == length) for length in range(1, 16)}

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_valid(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def find_words(x, y, current_word, visited, min_length, max_length, grid, found_words):
    if min_length <= len(current_word) <= max_length and current_word in valid_words_by_length[len(current_word)]:
        found_words.add(current_word)

    if len(current_word) > max_length:
        return
  
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny, grid) and (nx, ny) not in visited:
            visited.add((nx, ny))
            find_words(nx, ny, current_word + grid[nx][ny].lower(), visited, min_length, max_length, grid, found_words)
            visited.remove((nx, ny))

def word_search(grid, min_length=1, max_length=15):
    found_words = set()

    # Process the grid as a 4x4 matrix (2D list)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            
            visited = set([(i, j)])
            find_words(i, j, grid[i][j].lower(), visited, min_length, max_length, grid, found_words)

    return found_words

# Function to check if a word is related to a theme using ConceptNet (caching and optimization)
@lru_cache(maxsize=10000)  # Cache results for efficiency
def is_word_related_to_theme_conceptnet(word, theme, threshold=0.5):
    url = f"http://api.conceptnet.io/query?node=/c/en/{word}&other=/c/en/{theme}"
    response = requests.get(url).json()
    return len(response.get('edges', [])) > 0

# Function to filter words based on their relation to the theme using multithreading
def filter_words_by_theme(words_list, theme, threshold=0.5):
    related_words = []
    
    # Using ThreadPoolExecutor to parallelize the checks
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(is_word_related_to_theme_conceptnet, word, theme, threshold): word for word in words_list}
        for future in as_completed(futures):
            word = futures[future]
            if future.result():  # If the word is related to the theme
                related_words.append(word)
                
    return related_words

@app.route('/solve', methods=['POST'])
def solve():
    # Get the grid of letters and word length range from the request
    data = request.json
    grid = data.get("grid", [])
    min_length = data.get("min_length", 3)
    max_length = data.get("min_length", 16)

    theme = data.get("theme", "")  # Extract the theme from the frontend request

    if not theme:
        return jsonify({"error": "Theme is required"}), 400  # Return an error if the theme is not provided

    # Convert the flat grid (1D array) into a 2D grid (4x4)
    grid_2d = [grid[i:i+4] for i in range(0, len(grid), 4)]

    # Print the grid to the console (for debugging)
    print("Received grid:")
    for row in grid_2d:
        print(row)

    # Call the word search function to find valid words
    found_words = word_search(grid_2d, min_length, max_length)
    filtered_words = filter_words_by_theme(found_words, theme)

    # Return the valid words as a response
    return jsonify({"words": list(filtered_words)})

if __name__ == '__main__':
    app.run(debug=True)

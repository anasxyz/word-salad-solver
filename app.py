from flask import Flask, request, jsonify
from flask_cors import CORS
import nltk
from nltk.corpus import words

# Initialize Flask app
app = Flask(__name__)

# Enable CORS
CORS(app)

# Load the word dictionary
nltk.download('words')
english_words = set(words.words())

def is_valid_word(word):
    return word.lower() in english_words

def get_neighbors(x, y, grid_size):
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in directions if 0 <= x + dx < grid_size and 0 <= y + dy < grid_size]

def find_words(grid):
    found_words = set()
    grid_size = len(grid)

    def dfs(x, y, path, visited):
        word = ''.join(grid[i][j] for i, j in path)
        if len(word) > 1 and is_valid_word(word):
            found_words.add(word)
        if len(word) > max(len(w) for w in english_words):
            return
        for nx, ny in get_neighbors(x, y, grid_size):
            if (nx, ny) not in visited:
                dfs(nx, ny, path + [(nx, ny)], visited | {(nx, ny)})

    for i in range(grid_size):
        for j in range(grid_size):
            dfs(i, j, [(i, j)], {(i, j)})

    return sorted(found_words)

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Log raw request data to check if it's empty or malformed
        print("Request data (raw):", request.data.decode('utf-8'))
        
        data = request.get_json()
        print("Decoded JSON data:", data)

        if not data or 'grid' not in data:
            raise ValueError("Grid is missing or not in the correct format.")

        grid = data.get('grid')
        if not isinstance(grid, list):
            raise ValueError("Grid must be a list.")

        grid_size = len(grid)
        if any(len(row) != grid_size for row in grid):
            raise ValueError("Grid must be square.")

        words = find_words(grid)
        print("Found words:", words)

        return jsonify({"words": words})

    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "Error solving the puzzle. Please try again."}), 500



if __name__ == '__main__':
    app.run(debug=True)

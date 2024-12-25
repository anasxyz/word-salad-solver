import nltk
from nltk.corpus import words

nltk.download('words')

grid = [
    ['P', 'A', 'W', 'E'],
    ['O', 'G', 'N', 'E'],
    ['H', 'I', 'K', 'U'],
    ['T', 'S', 'B', 'Q']
]

valid_words = set(word.lower() for word in words.words())
valid_words_by_length = {length: set(word for word in valid_words if len(word) == length) for length in range(1, 16)}

directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def is_valid(x, y):
    return 0 <= x < len(grid) and 0 <= y < len(grid[0])

def find_words(x, y, current_word, visited, min_length, max_length):
    if min_length <= len(current_word) <= max_length and current_word in valid_words_by_length[len(current_word)]:
        found_words.add(current_word)

    if len(current_word) > max_length:
        return
  
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if is_valid(nx, ny) and (nx, ny) not in visited:
            visited.add((nx, ny))
            find_words(nx, ny, current_word + grid[nx][ny].lower(), visited, min_length, max_length)
            visited.remove((nx, ny))

def word_search(min_length=1, max_length=15):
    global found_words
    found_words = set()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            
            visited = set([(i, j)])
            find_words(i, j, grid[i][j].lower(), visited, min_length, max_length)

    return found_words

min_length = 3  
max_length = 6  
words_found = word_search(min_length, max_length)

print(f"Words found (length {min_length}-{max_length}):", words_found)



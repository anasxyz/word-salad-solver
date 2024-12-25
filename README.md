# Overview

This project is a Word Search Solver built using Python and Flask. It takes a grid of letters and searches for all valid words of a given length range within the grid, considering different traversal directions (up, down, left, right, and diagonals). The solver then filters the found words based on their relevance to a specific theme, using ConceptNet for semantic word relationships.

The project is designed to be accessible as a web service, allowing users to send requests to the API with a letter grid, word length range, and a theme. The server responds with a list of words that match the criteria, further filtered by theme relevance.

# Technology Stack
Frontend:
  The frontend could be any web application (such as HTML/JavaScript) that makes API requests to the Flask backend,
  though this project currently focuses on the backend API.

Backend:
  - Python: The primary programming language used for logic and API development.
  - Flask: A lightweight web framework for building RESTful APIs.
  - NLTK (Natural Language Toolkit): Used for the words corpus to validate the words found in the grid.
  - Requests: Used to make HTTP requests to ConceptNet for theme-based filtering.
  - ThreadPoolExecutor: Used to parallelize the word search process for efficiency.
  - ConceptNet API: An external semantic API used for checking word relationships to a given theme.

Data Structures:
  - Trie: An efficient tree-based data structure used to store and search for words. It is optimized for quick prefix-based searches, reducing the overall time complexity of word lookups.

Caching:
  - LRU Cache (lru_cache from functools): Used to cache results of semantic word relationship checks with ConceptNet to   minimize redundant API calls.

Concurrency:
  - Multi-threading for parallelizing the DFS search and the theme-based filtering.

# Key Features
Word Search: 
- The application performs a depth-first search (DFS) over the grid to find valid words by traversing neighboring cells in multiple directions (horizontal, vertical, and diagonal).
- Uses an optimized Trie data structure to efficiently store and search for valid words, reducing the complexity of lookups.
  
Multi-threading:
- The word search process is parallelized using multi-threading with Python's `ThreadPoolExecutor` to handle large grids efficiently and speed up the search process.

Word Validation:
- The project uses a large set of valid English words from **NLTK's** `words` corpus.
- It filters words based on their length (min/max) and checks if they are part of the dictionary.

Theme-based Filtering:
- After finding words, the application filters them based on their relevance to a provided theme using ConceptNet, a semantic network that determines word relationships.
- Theme relevance is determined by making API requests to ConceptNet and checking for connections between the words found in the grid and the theme.

Flask Web Service:
- The application is exposed as a REST API using Flask, allowing users to send POST requests with a grid of letters, word length range, and theme.
- The server returns a JSON response with the valid words that match the search criteria and the theme.

# Example Request and Response:

Request (POST to /solve):

`{
  "grid": ["V", "E", "N", "U", "P", "T", "A", "S", "Y", "U", "R", "M", "R", "C", "N", "E"],
  "min_length": 3,
  "max_length": 16,
  "theme": "planet"
}`

Response:

`{
  "words": ["venus", "planet", "saturn", "mars"]
}`

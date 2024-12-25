# world-salad-solver

This project is a Word Search Solver built using Python and Flask. It takes a grid of letters and searches for all valid words of a given length range within the grid, considering different traversal directions (up, down, left, right, and diagonals). The solver then filters the found words based on their relevance to a specific theme, using ConceptNet for semantic word relationships.

The project is designed to be accessible as a web service, allowing users to send requests to the API with a letter grid, word length range, and a theme. The server responds with a list of words that match the criteria, further filtered by theme relevance.

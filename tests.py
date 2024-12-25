import requests

theme = "air"
word = "plane"

url = f"http://api.conceptnet.io/c/en/{word.lower()}"
response = requests.get(url)


if response.status_code == 200:
    data = response.json()
    
    # # Print the full JSON response for debugging
    # print(data)
    
    # Now check if "chess" appears in any part of the JSON response
    found_theme = False
    for edge in data.get('edges', []):  # 'edges' contains the relationships between concepts
        # Check if 'chess' is in any of the related concepts (start or end)
        if theme in str(edge.get('start', '')) or theme in str(edge.get('end', '')):
            found_theme = True
            break
    
    if found_theme:
        print(f"The word '{theme}' appears in the JSON response.")
    else:
        print(f"The word '{theme}' does not appear in the JSON response.")


#####################################################################################################################


import nltk
from nltk.corpus import wordnet as wn

# Ensure necessary NLTK resources are downloaded
nltk.download('wordnet', quiet=True)
nltk.download('omw-1.4', quiet=True)

# Function to check if a word is related to a theme
def is_word_related_to_theme(word, theme_synsets, threshold=3):
    """
    Check if a word is related to a theme using WordNet definitions and relationships.
    """
    word_synsets = wn.synsets(word)
    if not word_synsets:
        return False

    # Check direct relationships or definition overlap
    for word_synset in word_synsets:
        for theme_synset in theme_synsets:
            # Check for direct synonyms
            if word_synset == theme_synset:
                return True
            
            # Check for shared hypernyms
            if theme_synset in word_synset.hypernyms() or word_synset in theme_synset.hypernyms():
                return True
            
            # Check definition overlap
            word_definition = set(word_synset.definition().lower().split())
            theme_definition = set(theme_synset.definition().lower().split())
            if len(word_definition & theme_definition) >= threshold:
                return True

    return False

# Function to filter words by theme
def filter_words_by_theme(words_list, theme, threshold=3):
    """
    Filter a list of words based on their relationship to a theme using WordNet.
    """
    # Precompute synsets for the theme
    theme_synsets = wn.synsets(theme)
    if not theme_synsets:
        print(f"No synsets found for the theme '{theme}'.")
        return []

    related_words = []
    for word in words_list:
        if is_word_related_to_theme(word, theme_synsets, threshold):
            related_words.append(word)

    return related_words

# Example usage
if __name__ == "__main__":
    words_found = ["pawn"]
    theme = "chess"
    threshold = 3  # Adjust this value to control strictness

    # Filter words based on the theme
    print(f"Filtering words related to the theme '{theme}'...")
    filtered_words = filter_words_by_theme(words_found, theme, threshold=threshold)

    # Output the results
    print(f"Words related to the theme '{theme}': {filtered_words}")


######################################################################################################################

import requests

def is_word_related_to_theme_conceptnet(word, theme):
    """
    Use ConceptNet to check if a word is related to a theme.
    """
    url = f"http://api.conceptnet.io/query?node=/c/en/{word}&other=/c/en/{theme}"
    response = requests.get(url).json()
    return len(response.get('edges', [])) > 0

# Example usage
word = "fly"
theme = "plane"
print(is_word_related_to_theme_conceptnet(word, theme))  # True for related, False otherwise

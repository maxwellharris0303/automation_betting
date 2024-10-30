import re

def remove_parentheses(text):
    pattern = r"\([^()]*\)"
    modified_text = re.sub(pattern, "", text)
    return modified_text.strip()

# # Example usage
# original_string = "DraftKings (Illinois)"
# modified_string = remove_parentheses(original_string)

# print(modified_string)
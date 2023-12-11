import sys
from collections import Counter

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.count = 0

def insert_word(root, word):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True
    node.count += 1

def build_trie(words):
    root = TrieNode()
    for word in words:
        insert_word(root, word)
    return root

def traverse_trie(node, prefix=[]):
    results = []
    if node.is_end_of_word:
        results.append((''.join(prefix), node.count))
    for char, child_node in node.children.items():
        results.extend(traverse_trie(child_node, prefix + [char]))
    return results

def find_most_common_words(text, n):
    words = text.split()
    trie_root = build_trie(words)
    word_count_tuples = traverse_trie(trie_root)
    sorted_tuples = sorted(word_count_tuples, key=lambda x: x[1], reverse=True)
    return sorted_tuples[:n]

if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file_path> <output_file_path>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    output_file_path = sys.argv[2]


    try:
        with open(input_file_path, 'r') as input_file:
            text = input_file.read()

        n = int(sys.argv[3])

        result = find_most_common_words(text, n)

        with open(output_file_path, 'w') as output_file:
            for word, count in result:
                output_file.write(f"{word}: {count}\n")

        print(f"The {n} most common words have been written to {output_file_path}")

    except FileNotFoundError:
        print("File not found. Please check the file path.")
        sys.exit(1)
    except ValueError: #triggers when too many titles (>25) in file?
        print("Invalid value for n. Please enter a valid integer.")
        sys.exit(1)

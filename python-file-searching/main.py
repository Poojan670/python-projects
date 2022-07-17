import os
from fuzzywuzzy import fuzz

root_dir = input("Enter the root directory for your search: ")
file_types = input("Enter the file endings to look for -separate by spaces- (Blank=All) :")
fuzzy_search_query = input("Enter the fuzzy search query(Blank=None) :")

file_types = file_types.split(" ")

if __name__ == "__main__":
    for root, dirs, files in os.walk(root_dir):
        for name in files:
            if name.endswith(tuple(ft for ft in file_types)) or file_types[0] == "":
                if fuzz.token_sort_ratio(fuzzy_search_query.lower(), name.lower()) > 50 or fuzzy_search_query == "":
                    print(root + os.sep + name)

import os
import re

# Define the path to the /docs folder
docs_path = r'c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr\docs'

# Regular expression to match leading numbers followed by a period
pattern = re.compile(r'^\d+\.')

def rename_files(path):
    """Rename files based on the specified rules."""
    for root, _, files in os.walk(path, topdown=True):
        for file_name in files:
            old_file_path = os.path.join(root, file_name)

            # Rule 1: Rename README.md to overview.md
            if file_name == "README.md":
                new_file_path = os.path.join(root, "overview.md")
                if not os.path.exists(new_file_path):  # Avoid conflicts
                    os.rename(old_file_path, new_file_path)
                    print(f'Renamed file: {old_file_path} -> {new_file_path}')
                continue

            # Rule 2: Remove leading numbers and periods from .md files
            if file_name.endswith('.md'):
                new_name = re.sub(pattern, '', file_name)
                if new_name != file_name:
                    new_file_path = os.path.join(root, new_name)
                    if not os.path.exists(new_file_path):  # Avoid conflicts
                        os.rename(old_file_path, new_file_path)
                        print(f'Renamed file: {old_file_path} -> {new_file_path}')

# Run the file renaming function
if __name__ == "__main__":
    rename_files(docs_path)
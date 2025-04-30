import os
import re

# Define the path to the /docs folder
docs_path = r'c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr\docs'

# Regular expression to match leading numbers followed by a period
pattern = re.compile(r'^\d+\.')

def rename_folders_in_place(path):
    """Rename folders in place by removing leading numbers and periods."""
    # Traverse the directory structure bottom-up to rename deeper folders first
    for root, dirs, _ in os.walk(path, topdown=False):
        for dir_name in dirs:
            # Generate the new folder name
            new_name = re.sub(pattern, '', dir_name)
            if new_name != dir_name:
                old_dir_path = os.path.join(root, dir_name)
                new_dir_path = os.path.join(root, new_name)
                # Rename the folder only if the new name doesn't already exist
                if not os.path.exists(new_dir_path):
                    os.rename(old_dir_path, new_dir_path)
                    print(f'Renamed folder: {old_dir_path} -> {new_dir_path}')
                else:
                    print(f"Skipping rename due to conflict: {old_dir_path} -> {new_dir_path}")

# Run the folder renaming function
if __name__ == "__main__":
    rename_folders_in_place(docs_path)
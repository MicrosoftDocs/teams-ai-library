import os
import re

# Define the folder path
folder_path = r"c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr\docs\how-to"

# Iterate through all .md files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the content of the file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
        
        # Find the first H1 marker and extract its content
        title = None
        for line in content:
            if line.startswith("# "):  # H1 marker
                title = line.strip("# ").strip()
                break
        
        # Replace the `title: PLACEHOLDER` line if a title was found
        if title:
            updated_content = []
            for line in content:
                if line.startswith("title: PLACEHOLDER"):
                    updated_content.append(f"title: {title}\n")
                else:
                    updated_content.append(line)
            
            # Write the updated content back to the file
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(updated_content)

print("Title replacement completed for all .md files in the /how-to folder.")
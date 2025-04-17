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
        
        # Reformat H3 lines with markdown links
        updated_content = []
        for line in content:
            # Match H3 lines with markdown links (e.g., ### [Text](#text))
            match = re.match(r"(###)\s+\[(.+?)\]\(.*?\)", line)
            if match:
                # Replace with stripped link formatting (e.g., ### Text)
                updated_content.append(f"{match.group(1)} {match.group(2)}\n")
            else:
                updated_content.append(line)
        
        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_content)

print("H3 headings with markdown links reformatted in all .md files in the /how-to folder.")
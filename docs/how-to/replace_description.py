import os

# Define the folder path
folder_path = r"c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr\docs\how-to"

# Iterate through all .md files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        file_path = os.path.join(folder_path, filename)
        
        # Read the content of the file
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.readlines()
        
        # Find the title and replace the description
        title = None
        updated_content = []
        for line in content:
            if line.startswith("title:"):
                title = line.strip().replace("title:", "").strip()
            if line.startswith("description: PLACEHOLDER") and title:
                updated_content.append(f"description: {title}\n")
            else:
                updated_content.append(line)
        
        # Write the updated content back to the file
        with open(file_path, "w", encoding="utf-8") as file:
            file.writelines(updated_content)

print("Description replacement completed for all .md files in the /how-to folder.")
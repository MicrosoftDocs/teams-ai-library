import os
import re

# Define the root directory of the codebase and the snippets directory
codebase_root = r"c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr"
snippets_dir = os.path.join(codebase_root, "docs", "assets", "generated-snippets", "ts")

# Regex to match TypeScript code blocks with snippet references
codeblock_pattern = re.compile(r"```ts(.*?)```", re.DOTALL)
snippet_reference_pattern = re.compile(r"\{\{#include\s+([^\s]+)\s*\}\}")

def replace_snippet_references(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    # Find all TypeScript code blocks
    matches = codeblock_pattern.findall(content)
    for match in matches:
        # Check for snippet references within the code block
        snippet_match = snippet_reference_pattern.search(match)
        if snippet_match:
            snippet_path = snippet_match.group(1).replace("../../../generated-snippets/ts/", "")
            snippet_file_path = os.path.join(snippets_dir, snippet_path)

            # Read the content of the referenced snippet file
            if os.path.exists(snippet_file_path):
                with open(snippet_file_path, "r", encoding="utf-8") as snippet_file:
                    snippet_content = snippet_file.read()

                # Replace the reference with the snippet content
                updated_codeblock = match.replace(snippet_match.group(0), snippet_content)
                content = content.replace(match, updated_codeblock)

    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

def process_codebase():
    for root, _, files in os.walk(codebase_root):
        for file in files:
            if file.endswith(".md"):  # Assuming the files to process are Markdown files
                file_path = os.path.join(root, file)
                replace_snippet_references(file_path)

if __name__ == "__main__":
    process_codebase()
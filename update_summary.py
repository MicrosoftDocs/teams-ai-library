import re

# Define the path to the SUMMARY.md file
summary_file_path = r'c:\Users\edoyle\Documents\GitHub\teams-ai-library-pr\docs\SUMMARY.md'

# Regular expressions to match patterns
leading_numbers_pattern = re.compile(r'/\d+\.(?=[^/]+)')  # Matches leading numbers and periods in paths
readme_pattern = re.compile(r'README\.md')  # Matches "README.md"

def update_summary_file(file_path):
    """Update the SUMMARY.md file based on the specified rules."""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Rule 1: Strip leading numbers and periods from folder and file names
    updated_content = re.sub(leading_numbers_pattern, '/', content)

    # Rule 2: Replace "README.md" with "overview.md"
    updated_content = re.sub(readme_pattern, 'overview.md', updated_content)

    # Write the updated content back to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(updated_content)

    print(f"Updated {file_path} successfully.")

# Run the function to update the SUMMARY.md file
if __name__ == "__main__":
    update_summary_file(summary_file_path)
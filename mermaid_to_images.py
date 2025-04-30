import os
import re
import subprocess

# Define paths
codebase_dir = "."  # Root directory of your codebase
output_dir = ".\\docs\\assets\\diagrams"  # Directory to save rendered diagrams

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Regex to match Mermaid code blocks
mermaid_block_pattern = re.compile(r"```mermaid\n(.*?)\n```", re.DOTALL)

def process_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    matches = mermaid_block_pattern.findall(content)
    if not matches:
        return  # No Mermaid code blocks found

    updated_content = content
    diagram_counter = 1

    for match in matches:
        # Generate output file name
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        output_file = f"{base_name}-{diagram_counter}.png"
        output_path = os.path.join(output_dir, output_file)

        # Write the Mermaid content to a temporary file
        temp_mermaid_file = "temp.mmd"
        with open(temp_mermaid_file, "w", encoding="utf-8") as temp_file:
            temp_file.write(match)

        # Render the Mermaid diagram using mermaid-cli
        try:
            subprocess.run(
                ["mmdc", "-i", temp_mermaid_file, "-o", output_path],
                check=True,
                shell=True,
            )

        except subprocess.CalledProcessError as e:
            print(f"Error rendering Mermaid diagram: {e}")
            continue
        finally:
            os.remove(temp_mermaid_file)  # Clean up temporary file

        # Replace the Mermaid code block with a Markdown image reference
        image_reference = f"![alt-text for {output_file}](~/assets/diagrams/{output_file})"
        updated_content = updated_content.replace(f"```mermaid\n{match}\n```", image_reference)

        diagram_counter += 1

    # Write the updated content back to the file
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(updated_content)

def search_and_process_codebase(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):  # Process only Markdown files
                file_path = os.path.join(root, file)
                process_file(file_path)

if __name__ == "__main__":
    search_and_process_codebase(codebase_dir)
    print("Processing complete.")
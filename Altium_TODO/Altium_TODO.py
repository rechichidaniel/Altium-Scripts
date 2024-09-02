import os
import re
import sys

# ANSI escape codes for coloring
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"  # Standard cyan for broad compatibility
RESET = "\033[0m"

def find_todos_in_schdoc(file_path):
    todos = []

    # Regular expression to match the TODO pattern with or without a description
    todo_pattern = re.compile(r'\|Text=(TODO[^~|]*)~?([^|]*)\|')

    try:
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read()
            matches = todo_pattern.findall(content)
            for match in matches:
                todo_colored = f"{RED}{match[0]}{RESET}"
                description_color = CYAN if '_' in match[0] else GREEN
                # Remove leading numbers from each line of the description
                description = re.sub(r'\n\d+', '\n', match[1].replace("~", "\n")).lstrip('0123456789')
                todos.append((os.path.basename(file_path), todo_colored, description, description_color))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return todos

def search_todos_in_directory(directory):
    all_todos = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.SchDoc'):
                file_path = os.path.join(root, file)
                todos = find_todos_in_schdoc(file_path)
                if todos:
                    all_todos.extend(todos)
    return all_todos

def main():
    # Allow the user to provide a directory path as a command-line argument
    if len(sys.argv) > 1:
        directory = sys.argv[1]
    else:
        directory = input("Enter the directory path to search for .SchDoc files: ")

    todos_found = search_todos_in_directory(directory)

    if todos_found:
        # Find the maximum lengths for each column to align the output
        max_filename_len = max(len(todo[0]) for todo in todos_found)
        max_todo_len = max(len(todo[1]) for todo in todos_found)

        current_file = ""
        print("\nTODOs found:")
        for todo in todos_found:
            if current_file != todo[0]:
                current_file = todo[0]
                print(f"\n{current_file}")  # New line and print the filename

            # Split the description into lines and properly indent each line after the first
            description_lines = todo[2].split("\n")
            description_colored = f"{todo[3]}{description_lines[0]}{RESET}"
            for line in description_lines[1:]:
                description_colored += f"\n{' ' * (max_filename_len + max_todo_len + 6)}{todo[3]}{line}{RESET}"
                
            print(f"{' ' * (max_filename_len + 3)}| {todo[1].ljust(max_todo_len)} | {description_colored}")
        
        # Print the total number of TODOs found in red
        print(f"\n{RED}Total TODOs found: {len(todos_found)}{RESET}")
    else:
        print("No TODOs found.")

if __name__ == "__main__":
    main()

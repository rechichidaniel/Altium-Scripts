import os
import re
import sys

# ANSI escape codes for coloring
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"  # Standard cyan for broad compatibility
RESET = "\033[0m"

def find_todos_in_schdoc(file_path):
    """
    Searches a given .SchDoc file for TODO messages and their descriptions.
    
    Args:
        file_path (str): The path to the .SchDoc file.

    Returns:
        list: A list of tuples, each containing the filename, the TODO message, 
              the description, and the description's color (either green or cyan).
    """
    todos = []

    # Regular expression to match the TODO pattern with or without a description
    todo_pattern = re.compile(r'\|Text=(TODO[^~|]*)~?([^|]*)\|')

    try:
        # Read the .SchDoc file content
        with open(file_path, 'r', errors='ignore') as file:
            content = file.read()
            matches = todo_pattern.findall(content)
            for match in matches:
                # Color the TODO message in red
                todo_colored = f"{RED}{match[0]}{RESET}"
                # Use cyan for descriptions if TODO has a suffix, otherwise use green
                description_color = CYAN if '_' in match[0] else GREEN
                # Replace '~' with newline and remove leading numbers from each line
                description = re.sub(r'\n\d+', '\n', match[1].replace("~", "\n")).lstrip('0123456789')
                todos.append((os.path.basename(file_path), todo_colored, description, description_color))
    except Exception as e:
        print(f"Error reading {file_path}: {e}")

    return todos

def search_todos_in_directory(directory):
    """
    Recursively searches all .SchDoc files in a given directory for TODO messages.
    
    Args:
        directory (str): The path to the directory to search.

    Returns:
        list: A list of tuples containing TODO information from all found files.
    """
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
    """
    The main function that executes the script. It either accepts a directory path 
    as a command-line argument or prompts the user to enter one, then searches for 
    TODO messages in .SchDoc files within that directory and prints the results.
    """
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
                
            # Print TODO message and description with proper alignment and color
            print(f"{' ' * (max_filename_len + 3)}| {todo[1].ljust(max_todo_len)} | {description_colored}")
        
        # Print the total number of TODOs found in red
        print(f"\n{RED}Total TODOs found: {len(todos_found)}{RESET}")
    else:
        print("No TODOs found.")

if __name__ == "__main__":
    main()

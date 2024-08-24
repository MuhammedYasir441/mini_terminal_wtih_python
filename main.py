import os

def terminal():
    while True:
        # Get the current working directory
        current_directory = os.getcwd()
        # Prompt the user for input
        command = input(f"{current_directory} >> ")

        # Exit the terminal if the user types 'exit'
        if command.strip().lower() == 'exit':
            print("Exiting...")
            break

        # Provide help information
        elif command.strip().lower() == 'help':
            print("Python Terminal is running. Type 'exit' to quit.")
            print("You can use the 'echo [message]' command.")
            print("Create a folder with 'mkdir [name]'.")
            print("Change directory with 'cd [new directory]'.")
            print("List files and folders in the current directory with 'ls'.")
            print("Display the current directory with 'pwd'.")
            print("Delete a file or folder with 'rm -rf [name]'.")
            print("Create a file with 'touch [file path]'.")
            print("View file contents with 'cat [file path]'.")

        # Echo command: print the provided message
        elif command.strip().lower().startswith('echo '):
            message = command[5:].strip()
            print(message)

        # Create a new directory
        elif command.strip().lower().startswith('mkdir '):
            folder_name = command[6:].strip()
            try:
                if not os.path.exists(folder_name):
                    os.makedirs(folder_name)
                    print(f"Folder '{folder_name}' created.")
                else:
                    print(f"Folder '{folder_name}' already exists.")
            except Exception as e:
                print(f"Error: {e}")

        # Delete a file or directory
        elif command.strip().lower().startswith('rm -rf '):
            target = command[7:].strip()
            try:
                if os.path.exists(target):
                    if os.path.isdir(target):
                        # If it's a directory
                        os.rmdir(target)
                        print(f"Folder '{target}' deleted.")
                    else:
                        # If it's a file
                        os.remove(target)
                        print(f"File '{target}' deleted.")
                else:
                    print(f"'{target}' not found.")
            except Exception as e:
                print(f"Error: {e}")

        # Change the current directory
        elif command.strip().lower().startswith('cd '):
            new_dir = command[3:].strip()
            try:
                os.chdir(new_dir)
                print(f"Current directory changed to '{os.getcwd()}'.")
            except Exception as e:
                print(f"Error: {e}")

        # List files and directories in the current directory
        elif command.strip().lower() == 'ls':
            try:
                files = os.listdir()
                if files:
                    print("Files and folders in the current directory:")
                    for file in files:
                        print(file)
                else:
                    print("No files or folders in this directory.")
            except Exception as e:
                print(f"Error: {e}")

        # Print the current working directory
        elif command.strip().lower() == 'pwd':
            print(f"Current directory: {os.getcwd()}")

        # Create a new file or update the timestamp of an existing file
        elif command.strip().lower().startswith('touch '):
            file_path = command[6:].strip()
            try:
                with open(file_path, 'a'):
                    pass
                print(f"File '{file_path}' created.")
            except Exception as e:
                print(f"Error: {e}")

        # Display the contents of a file
        elif command.strip().lower().startswith('cat '):
            file_path = command[4:].strip()
            try:
                with open(file_path, 'r') as file:
                    print(file.read())
            except Exception as e:
                print(f"Error: {e}")

        # Handle unknown commands
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    terminal()

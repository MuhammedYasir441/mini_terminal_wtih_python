import os
import psutil
import zipfile
import platform
import subprocess

def uname():
    # Get OS name and version
    uname_info = platform.uname()
    print(f"System: {uname_info.system}")
    print(f"Node Name: {uname_info.node}")
    print(f"Release: {uname_info.release}")
    print(f"Version: {uname_info.version}")
    print(f"Machine: {uname_info.machine}")
    print(f"Processor: {uname_info.processor}")

def ipconfig():
    # Display IP configuration based on OS
    if os.name == 'nt':  # Windows
        os.system('ipconfig')
    elif os.name == 'posix':  # Unix-like
        os.system('ifconfig' if subprocess.call(['which', 'ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0 else 'ip addr show')

def print_help():
    help_text = """
    Available commands:
    
    echo <message>
        Prints the provided message to the terminal.
    
    mkdir <folder_name>
        Creates a new directory with the specified name.
    
    rmdir <folder_name>
        Removes an empty directory with the specified name.
    
    rm -rf <target>
        Deletes a file or directory (non-empty directories).
    
    cd <directory>
        Changes the current working directory to the specified directory.
    
    ls
        Lists all files and directories in the current working directory.
    
    pwd
        Prints the current working directory.
    
    touch <file_path>
        Creates a new file or updates the timestamp of an existing file.
    
    cat <file_path>
        Displays the contents of the specified file.
    
    mv <source> <destination>
        Moves (renames) a file or directory from source to destination.
    
    ps
        Lists all running processes with their PID and name.
    
    killall <process_name>
        Terminates all processes with the specified name.
    
    uname
        Prints information about the operating system.
    
    ipconfig
        Displays IP configuration (Windows) or network interfaces (Unix-like).
    
    zip <zipfile_name> <file_or_directory1> <file_or_directory2> ...
        Zips the specified files or directories into a single zip file.
    
    exit
        Exits the terminal.
    """
    print(help_text)

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
            print_help()

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

        # Remove an empty directory
        elif command.strip().lower().startswith('rmdir '):
            folder_name = command[6:].strip()
            try:
                if os.path.isdir(folder_name):
                    os.rmdir(folder_name)
                    print(f"Empty folder '{folder_name}' removed.")
                else:
                    print(f"'{folder_name}' is not a directory or does not exist.")
            except OSError as e:
                print(f"Error: {e}")

        # Delete a file or directory
        elif command.strip().lower().startswith('rm -rf '):
            target = command[7:].strip()
            try:
                if os.path.exists(target):
                    if os.path.isdir(target):
                        os.rmdir(target)
                        print(f"Folder '{target}' deleted.")
                    else:
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

        # Move (rename) a file or directory
        elif command.strip().lower().startswith('mv '):
            parts = command[3:].split()
            if len(parts) == 2:
                src = parts[0].strip()
                dst = parts[1].strip()
                try:
                    if os.path.exists(src):
                        os.rename(src, dst)
                        print(f"'{src}' moved to '{dst}'.")
                    else:
                        print(f"'{src}' not found.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Usage: mv <source> <destination>")

        # List running processes
        elif command.strip().lower() == 'ps':
            try:
                # Get the list of all running processes
                for proc in psutil.process_iter(['pid', 'name']):
                    print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
            except Exception as e:
                print(f"Error: {e}")

        # Kill all processes with a given name
        elif command.strip().lower().startswith('killall '):
            process_name = command[8:].strip()
            try:
                killed = False
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'] == process_name:
                        proc.terminate()  # or proc.kill() for forceful termination
                        killed = True
                        print(f"Terminated process '{process_name}' with PID {proc.info['pid']}.")
                if not killed:
                    print(f"No processes with name '{process_name}' found.")
            except Exception as e:
                print(f"Error: {e}")

        # Print OS name and more details (uname)
        elif command.strip().lower() == 'uname':
            uname()

        # Display IP configuration
        elif command.strip().lower() == 'ipconfig':
            ipconfig()

        # Zip files or directories
        elif command.strip().lower().startswith('zip '):
            zip_command = command[4:].strip()
            parts = zip_command.split()
            if len(parts) >= 2:
                zip_filename = parts[0].strip()
                targets = parts[1:]
                try:
                    with zipfile.ZipFile(zip_filename, 'w') as zipf:
                        for target in targets:
                            if os.path.exists(target):
                                if os.path.isdir(target):
                                    for foldername, subfolders, filenames in os.walk(target):
                                        for filename in filenames:
                                            file_path = os.path.join(foldername, filename)
                                            zipf.write(file_path, os.path.relpath(file_path, target))
                                else:
                                    zipf.write(target)
                            else:
                                print(f"'{target}' not found.")
                    print(f"Files and folders zipped into '{zip_filename}'.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print("Usage: zip <zipfile_name> <file_or_directory1> <file_or_directory2> ...")

        # Handle unknown commands
        else:
            print(f"Unknown command: {command}")

if __name__ == "__main__":
    terminal()

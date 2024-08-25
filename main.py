import os
import shutil
import psutil
import zipfile
import platform
import subprocess

# Global variable to store the copied file or directory
copied_item = None

def uname():
    uname_info = platform.uname()
    print(f"System: {uname_info.system}")
    print(f"Node Name: {uname_info.node}")
    print(f"Release: {uname_info.release}")
    print(f"Version: {uname_info.version}")
    print(f"Machine: {uname_info.machine}")
    print(f"Processor: {uname_info.processor}")

def ipconfig():
    if os.name == 'nt':
        os.system('ipconfig')
    else:
        subprocess.run(['ifconfig'] if subprocess.call(['which', 'ifconfig'], stdout=subprocess.PIPE, stderr=subprocess.PIPE) == 0 else ['ip', 'addr', 'show'])

def print_help():
    help_text = """
    Available commands:

    echo <message>              Prints the provided message to the terminal.
    mkdir <folder_name>         Creates a new directory with the specified name.
    rmdir <folder_name>         Removes an empty directory with the specified name.
    rm -rf <target>             Deletes a file or directory (non-empty directories).
    cd <directory>             Changes the current working directory to the specified directory.
    ls                         Lists all files and directories in the current working directory.
    pwd                        Prints the current working directory.
    touch <file_path>          Creates a new file or updates the timestamp of an existing file.
    cat <file_path>            Displays the contents of the specified file.
    mv <source> <destination>  Moves (renames) a file or directory from source to destination.
    ps                         Lists all running processes with their PID and name.
    killall <process_name>     Terminates all processes with the specified name.
    uname                      Prints information about the operating system.
    ipconfig                   Displays IP configuration (Windows) or network interfaces (Unix-like).
    zip <zipfile_name> <file_or_directory1> <file_or_directory2> ...  Zips the specified files or directories into a single zip file.
    cp <source> <destination>  Copies a file or directory from source to destination.
    paste                      Pastes the copied file or directory to the current directory.
    find <directory> <pattern> Finds files or directories matching the pattern within the specified directory.
    chmod <permissions> <file_or_directory>  Changes the permissions of a file or directory.
    exit                       Exits the terminal.
    """
    print(help_text)

def copy(source):
    global copied_item
    if os.path.exists(source):
        copied_item = source
        print(f"Copied '{source}'")
    else:
        print(f"'{source}' not found.")

def paste(destination):
    global copied_item
    if copied_item is None:
        print("No item has been copied.")
        return

    if os.path.exists(copied_item):
        try:
            if os.path.isdir(copied_item):
                shutil.copytree(copied_item, os.path.join(destination, os.path.basename(copied_item)), dirs_exist_ok=True)
                print(f"Directory '{copied_item}' pasted into '{destination}'.")
            else:
                shutil.copy2(copied_item, destination)
                print(f"File '{copied_item}' pasted into '{destination}'.")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print(f"'{copied_item}' not found.")

def find(directory, pattern):
    matches = [os.path.join(root, name)
               for root, dirs, files in os.walk(directory)
               for name in files + dirs if pattern in name]
    return matches

def chmod(permissions, path):
    try:
        perms = int(permissions, 8)  # Convert octal string to integer
        os.chmod(path, perms)
        print(f"Permissions for '{path}' changed to '{permissions}'.")
    except ValueError:
        print(f"Invalid permissions format: '{permissions}'. Use octal format.")
    except Exception as e:
        print(f"Error: {e}")

def execute_command(command):
    """Executes a single command and returns its success status."""
    global copied_item

    if command == 'exit':
        print("Exiting...")
        return False

    elif command == 'help':
        print_help()

    elif command.startswith('echo '):
        print(command[5:].strip())

    elif command.startswith('mkdir '):
        folder_name = command[6:].strip()
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
            print(f"Folder '{folder_name}' created.")
        else:
            print(f"Folder '{folder_name}' already exists.")

    elif command.startswith('rmdir '):
        folder_name = command[6:].strip()
        if os.path.isdir(folder_name):
            try:
                os.rmdir(folder_name)
                print(f"Empty folder '{folder_name}' removed.")
            except OSError as e:
                print(f"Error: {e}")
        else:
            print(f"'{folder_name}' is not a directory or does not exist.")

    elif command.startswith('rm -rf '):
        target = command[7:].strip()
        if os.path.exists(target):
            try:
                if os.path.isdir(target):
                    shutil.rmtree(target)
                    print(f"Folder '{target}' deleted.")
                else:
                    os.remove(target)
                    print(f"File '{target}' deleted.")
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"'{target}' not found.")

    elif command.startswith('cd '):
        new_dir = command[3:].strip()
        try:
            os.chdir(new_dir)
            print(f"Current directory changed to '{os.getcwd()}'.")
        except Exception as e:
            print(f"Error: {e}")

    elif command == 'ls':
        try:
            files = os.listdir()
            if files:
                print("Files and folders in the current directory:")
                print('\n'.join(files))
            else:
                print("No files or folders in this directory.")
        except Exception as e:
            print(f"Error: {e}")

    elif command == 'pwd':
        print(f"Current directory: {os.getcwd()}")

    elif command.startswith('touch '):
        file_path = command[6:].strip()
        try:
            open(file_path, 'a').close()
            print(f"File '{file_path}' created.")
        except Exception as e:
            print(f"Error: {e}")

    elif command.startswith('cat '):
        file_path = command[4:].strip()
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    print(file.read())
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"'{file_path}' not found.")

    elif command.startswith('mv '):
        parts = command[3:].split()
        if len(parts) == 2:
            src, dst = map(str.strip, parts)
            if os.path.exists(src):
                try:
                    os.rename(src, dst)
                    print(f"'{src}' moved to '{dst}'.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"'{src}' not found.")
        else:
            print("Usage: mv <source> <destination>")

    elif command == 'ps':
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}")
        except Exception as e:
            print(f"Error: {e}")

    elif command.startswith('killall '):
        process_name = command[8:].strip()
        try:
            killed = False
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] == process_name:
                    proc.terminate()
                    killed = True
                    print(f"Terminated process '{process_name}' with PID {proc.info['pid']}.")
            if not killed:
                print(f"No processes with name '{process_name}' found.")
        except Exception as e:
            print(f"Error: {e}")

    elif command == 'uname':
        uname()

    elif command == 'ipconfig':
        ipconfig()

    elif command.startswith('zip '):
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

    elif command.startswith('cp '):
        parts = command[3:].split()
        if len(parts) == 2:
            src, dst = map(str.strip, parts)
            if os.path.exists(src):
                try:
                    if os.path.isdir(src):
                        shutil.copytree(src, dst, dirs_exist_ok=True)
                        print(f"Directory '{src}' copied to '{dst}'.")
                    else:
                        shutil.copy2(src, dst)
                        print(f"File '{src}' copied to '{dst}'.")
                except Exception as e:
                    print(f"Error: {e}")
            else:
                print(f"'{src}' not found.")
        else:
            print("Usage: cp <source> <destination>")

    elif command.startswith('paste'):
        paste(os.getcwd())

    elif command.startswith('find '):
        parts = command[5:].split()
        if len(parts) == 2:
            directory, pattern = map(str.strip, parts)
            matches = find(directory, pattern)
            if matches:
                print("Found:")
                print('\n'.join(matches))
            else:
                print(f"No matches found for pattern '{pattern}' in '{directory}'.")
        else:
            print("Usage: find <directory> <pattern>")

    elif command.startswith('chmod '):
        parts = command[6:].split()
        if len(parts) == 2:
            permissions, path = map(str.strip, parts)
            chmod(permissions, path)
        else:
            print("Usage: chmod <permissions> <file_or_directory>")

    else:
        print(f"Command '{command}' not recognized.")

    return True

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input(">>> ")
        if not execute_command(user_input):
            break

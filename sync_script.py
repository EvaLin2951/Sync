import os
import subprocess
import shlex
import getpass

# Configuration settings for SSH connection
username = 'your_username'  # Enter your SSH username
hostname = 'your_hostname'  # Enter your SSH hostname
port = 22  # Enter your SSH port number if different from 22
remote_directory = '/path/to/remote/directory'  # Specify the remote directory path
local_directory = '/path/to/local/directory'  # Specify the local directory path
ssh_key_path = '/path/to/your/private/key'  # Specify the path to your SSH private key
exclude_directories = {'/path/to/exclude1', '/path/to/exclude2'}  # Specify directories to exclude

def execute_ssh_command(command):
    """ Execute an SSH command and return the output or 0 on failure. """
    if ssh_key_path and os.path.exists(ssh_key_path):
        full_command = f"ssh -i {ssh_key_path} {username}@{hostname} -p {port} {command}"
    else:
        password = getpass.getpass("SSH Password: ")
        full_command = f"sshpass -p {password} ssh {username}@{hostname} -p {port} {command}"
    
    result = subprocess.run(full_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode('utf-8').strip() if result.returncode == 0 else None


def get_remote_mod_time(remote_path):
    """Retrieve the modification time of a file on the remote system."""
    command = f"stat -c %Y {shlex.quote(remote_path)}"
    return int(execute_ssh_command(command)) if execute_ssh_command(command) else 0

def sync_directory_structure():
    """ Ensure that the directory structure of the remote is mirrored locally. """
    all_local_dirs = set()
    for dirpath, dirnames, _ in os.walk(local_directory):
        all_local_dirs.add(dirpath)
        for dirname in dirnames:
            all_local_dirs.add(os.path.join(dirpath, dirname))

    all_remote_dirs = set()
    for dirpath, dirnames, _ in os.walk(remote_directory):
        if dirpath in exclude_directories:
            continue
        local_path = os.path.join(local_directory, os.path.relpath(dirpath, remote_directory))
        all_remote_dirs.add(local_path)
        for dirname in dirnames:
            dir_full_path = os.path.join(dirpath, dirname)
            if dir_full_path in exclude_directories:
                continue
            local_dir_path = os.path.join(local_directory, os.path.relpath(dir_full_path, remote_directory))
            all_remote_dirs.add(local_dir_path)
            if not os.path.exists(local_dir_path):
                os.makedirs(local_dir_path)

    for local_dir in sorted(all_local_dirs - all_remote_dirs, reverse=True):
        if not os.listdir(local_dir):
            os.rmdir(local_dir)

def is_excluded_directory(dirpath):
    return any(os.path.commonpath([dirpath, ex_dir]) == ex_dir for ex_dir in exclude_directories)

def get_file_list(directory):
    """ Retrieve the list of all file paths in a directory excluding specified subdirectories. """
    file_paths = []
    for dirpath, _, filenames in os.walk(directory):
        if is_excluded_directory(dirpath):
            continue
        for filename in filenames:
            if filename == '.DS_Store':
                continue
            file_path = os.path.join(dirpath, filename)
            file_paths.append(file_path)
    return file_paths

def sync_check(remote_files, local_files):
    """ Verify that the number and size of files in the remote and local directories are the same. """
    total_remote_size = sum(os.path.getsize(f) for f in remote_files)
    total_local_size = sum(os.path.getsize(f) for f in local_files)

    if len(remote_files) == len(local_files) and total_remote_size == total_local_size:
        print("🎉 Sync complete!")
    else:
        print("🆘 Sync failed!")

def sync_files():
    """ Synchronize files from the remote directory to the local directory. """
    sync_directory_structure()

    remote_files = get_file_list(remote_directory)
    adjusted_remote_files = {os.path.join(local_directory, os.path.relpath(path, remote_directory)) for path in remote_files}

    for remote_file_path in remote_files:
        local_file_path = os.path.join(local_directory, os.path.relpath(remote_file_path, remote_directory))
        remote_mod_time = get_remote_mod_time(remote_file_path)
        local_mod_time = os.path.getmtime(local_file_path) if os.path.exists(local_file_path) else None
        
        if local_mod_time is None or remote_mod_time > local_mod_time:
            print(f"Downloading {remote_file_path} to {local_file_path}")
            command = f"scp -i {ssh_key_path} -P {port} {username}@{hostname}:{shlex.quote(remote_file_path)} {shlex.quote(local_file_path)}"
            subprocess.run(command, shell=True)
        else:
            print(f"Skipping {remote_file_path}")

    updated_local_files = get_file_list(local_directory)

    for local_file in updated_local_files:
        if local_file not in adjusted_remote_files:
            print(f"Deleting local file {local_file}")
            os.remove(local_file)

    sync_check(remote_files, updated_local_files)


if __name__ == "__main__":
    sync_files()

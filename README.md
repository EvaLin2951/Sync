# Directory Sync Script

This Python script provides a quick way to synchronize file directories between a local machine and a remote server over SSH, ensuring that both locations maintain identical copies of all files, except for those explicitly excluded via the configuration. The script utilizes secure SSH protocols to transfer data, protecting your information during transit.

## Features

- **Secure Data Transfer**: Uses SSH for secure file synchronization, ensuring that your data is protected during transmission.
- **Automatic Directory Matching**: Automatically creates or removes directories on the local machine to match the remote structure, ensuring a true mirror image between the two.
- **Selective Synchronization**: Offers the flexibility to exclude specific files and directories from synchronization, allowing for customized syncing that suits your specific needs.
- **Efficient Updates**: Only transfers files that are newer than those in the destination directory, this ensures that the synchronization process only updates files that have been modified, keeping your directories up-to-date without unnecessary data transfer.

## Usage

### Running the Script

To synchronize your directories using this script, follow these steps:

1. **Configure the Script**: Before running the script, ensure all configuration settings are correctly set in the script file. This includes setting your SSH username, hostname, remote and local directories, SSH key path, and any directories you wish to exclude from syncing.

2. **Open Terminal**: Open your terminal or command prompt.

3. **Navigate to the Script Directory**: Use the `cd` command to change to the directory where the script is located. For example:
   ```bash
   cd path/to/your/sync-script

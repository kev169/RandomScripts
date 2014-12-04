#!/usr/bin/env python
import os
import paramiko
import sys
import getopt


def aboutMenu():
    print("-l /path/to/file.txt -d /path/on/server.txt -h pi@192.168.1.2 -p 3456")


def main(args):
    print(args)
    #try:
    opts, args = getopt.getopt(args, "l:d:h:p:")
    #except getopt.GetoptError:
    #  aboutMenu()
    #  sys.exit()
    localfile = ""
    destfile = ""
    host = ""
    user = ""
    port = 22
    for opt,arg in opts:
        if opt == "-l":
            localfile = arg
        elif opt == "-d":
            destfile = arg
        elif opt == "-h":
            user = arg.split("@")[0]
            host = arg.split("@")[1]
        elif opt == "-p":
            port = int(arg)
    if localfile == "" or destfile == "" or host == "" or user == "":
        print("argument not met.")
        sys.exit()
    else:
        print("success")
    transport = paramiko.Transport((host, port))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    #Download piece
    filepath = '/etc/passwd'
    localpath = '/home/remotepasswd'
    sftp.get(filepath, localpath)

    # Upload
    filepath = '/home/foo.jpg'
    localpath = '/home/pony.jpg'
    sftp.put(localpath, filepath)

    # Close
    sftp.close()
    transport.close()
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Not enough arguments");
        aboutMenu()
        sys.exit()
    main(sys.argv[1:])

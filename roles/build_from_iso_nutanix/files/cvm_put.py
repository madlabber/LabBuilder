#!/usr/bin/env python3
"""Copy one file to a Nutanix CVM over SFTP with a password.

Usage: cvm_put.py HOST PORT USER LOCAL_FILE REMOTE_PATH
The password is read from the CVM_PASSWORD environment variable. A copy that
already has the same size is left alone. Prints "copied" or "present".
"""
import os
import sys

import paramiko

host, port, user, local, remote = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4], sys.argv[5]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(host, port=port, username=user, password=os.environ["CVM_PASSWORD"],
               look_for_keys=False, allow_agent=False, timeout=20, banner_timeout=30, auth_timeout=30)
sftp = client.open_sftp()
size = os.path.getsize(local)
try:
    if sftp.stat(remote).st_size == size:
        print("present")
        sys.exit(0)
except IOError:
    pass
sftp.put(local, remote + ".part")
sftp.posix_rename(remote + ".part", remote)
print("copied")
client.close()

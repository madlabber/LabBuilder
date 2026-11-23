#!/usr/bin/env python3
"""Run one command on a Nutanix CVM over SSH with a password, retrying until it
exits 0 or the time runs out. The CVM reboots during its first boot, so a
dropped or refused connection is retried like any other failure.

Usage: cvm_ssh.py HOST PORT USER TIMEOUT_SECONDS COMMAND
The password is read from the CVM_PASSWORD environment variable.
Prints the command's output and exits 0 on success; prints the last error and
exits 1 once TIMEOUT_SECONDS have passed (0 means a single attempt).
"""
import os
import sys
import time

import paramiko

host, port, user, timeout, command = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), sys.argv[5]
deadline = time.time() + timeout
last = ""

while True:
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, port=port, username=user, password=os.environ["CVM_PASSWORD"],
                       look_for_keys=False, allow_agent=False,
                       timeout=20, banner_timeout=30, auth_timeout=30)
        _, out, err = client.exec_command(command)
        stdout, stderr = out.read().decode(), err.read().decode()
        rc = out.channel.recv_exit_status()
        client.close()
        if rc == 0:
            sys.stdout.write(stdout)
            sys.exit(0)
        last = "exit %d\n%s%s" % (rc, stdout, stderr)
    except Exception as ex:  # connection refused, timeout, reset during reboot...
        last = "%s: %s" % (type(ex).__name__, ex)
    if time.time() >= deadline:
        sys.stderr.write(last)
        sys.exit(1)
    time.sleep(20)

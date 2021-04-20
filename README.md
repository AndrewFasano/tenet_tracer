TENET Tracer
----

Simple container to run [PANDA](https://panda.re)s' [Tenet](https://github.com/gaasedelen/tenet) trace collection [plugin](https://github.com/panda-re/panda/tree/master/panda/plugins/trace) on a target program and also log the load address of your target program.


## Example usage.
If you want to trace the program `ls` running with arguments `-al` and inside a directory with a file called `foo`:
```
mkdir testdir
cp /bin/ls ./testdir
touch ./testdir/foo

./run.sh x86_64 ./testdir ls -al
```

Output:
```
Sending build context to Docker daemon  5.632kB
Step 1/5 : FROM pandare/pandadev:latest
...
Successfully tagged tenet_tracer:latest
+ docker run --rm -v /home/user/git/tenet_trace/testdir:/home/user/git/tenet_trace/testdir tenet_tracer x86_64 /home/user/git/tenet_trace/testdir ls -al
PANDA[core]:...
using generic 86_64
Qcow bionic-server-cloudimg-amd64-noaslr-nokaslr.qcow2 doesn't exist. Downloading from https://panda-re.mit.edu. Thanks MIT!
...
./ls loaded at 0x7ffff7dd6090
total 12036
drwxr-xr-x 2 root root     4096 Apr 10 19:33 .
drwxr-xr-x 4 root root     4096 Apr 10 19:33 ..
-rw-r--r-- 1 root root        0 Apr 10 19:33 foo
-rwxr-xr-x 1 root root   133792 Apr 10 19:33 ls
-rw-r--r-- 1 root root 12176870 Apr 10 19:33 ls.log
```


## Supported architectures
Just `x86` / `x86_64` for now. It would be pretty easy to expand the PANDA plugin and this repo to support additional architectures if you want to submit a PR.

## Implementation Overview
We use PANDA's generic qcows to fetch a virtual machine of the requested archtiecture. Then we use PANDA's `copy_to_guest`
functionality to copy a directory from our container into the guest and run the target program with the trace collection plugin loaded.
The only tricky thing here is mapping host directories into the container and then copying those into the guest virtual machine.

## Current status
The dockerfile building will go much faster once the tracer plugin is merged into PANDA's main branch. The outputs from the PANDA tracing plugin haven't yet been tested extensively with TENET.

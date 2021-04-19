TENET Tracer
----

Simple container to run [PANDA](https://panda.re)s' TENET trace collection plugin on a target program.


## Example usage.
```
mkdir testdir
cp /bin/ls ./testdir

./run.sh x86_64 testdir ls -al
```


## Supported architecture
Just `x86` / `x86_64` for now. It would be pretty easy to expand the PANDA plugin and this repo to support additional architectures if you wants to submit a PR.

## Implementation Overview
We use PANDA's generic qcows to fetch a virtual machine of the requested archtiecture. Then we use PANDA's `copy_to_guest`
functionality to copy a directory from our container into the guest and run the target program with the trace collection plugin loaded.
The only tricky thing here is mapping host directories into the container and then copying those into the guest virtual machine.

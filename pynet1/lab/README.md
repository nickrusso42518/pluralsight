# Course background information
This file contains background information about the course, including
configuration files and versions.

Please contact me on Twitter `@nickrusso42518` or in the course
discussion with any questions you have.

## Development machine
I used an Amazon Linux platform on EC2 for this course, but any Linux
device will do. I'd also suggest setting up a Python virtual
environment (`venv`) to ensure there are no collisions with Python
packages between this course and the system Python instance.

The following packages are not required but may be useful to you. You
may install them using your OS package manager, such as `yum` or `apt`.
Some of these may come as default options in your distribution are they
are all common.

```
vim-enhanced
tree
make
git
```

## Network details
I used Cisco CSR1000v and Cisco XRv9000 in this network, as explained in
the Globomantics background. Software versions are shown below.

```
CSR1000v - Cisco IOS XE Software, Version 16.09.02
XRv9000 - Cisco IOS XR Software, Version 6.3.1
```

Configurations for R1, R2, and R3 are included in the `configs/` directory.
You may load these up ahead of time, and given the usage of GRE tunnels to
interconnect one another, they should work in most public cloud environments.

## Python details
I used Python 3.7.3 for this course. Python 3.6 is the absolute minimum,
and in that case, you won't be able to use `breakpoint()` to invoke `pdb`.
This is explained in the course video content. You can install the newest
Python version here: `https://www.python.org/downloads/`

```
$ python --version
Python 3.7.3
```

Below is the full list of Python packages in my `venv` with their versions.
I've also included a `requirements.txt` which you can use to get started
quickly using `pip install -r requirements.txt`

```
$ pip list
Package           Version 
----------------- --------
appdirs           1.4.3   
asn1crypto        0.24.0  
astroid           2.2.5   
atomicwrites      1.3.0   
attrs             19.1.0  
bcrypt            3.1.6   
black             19.3b0  
certifi           2019.3.9
cffi              1.12.3  
chardet           3.0.4   
Click             7.0     
colorama          0.4.1   
cryptography      2.4.2   
future            0.17.1  
idna              2.8     
isort             4.3.20  
Jinja2            2.10.1  
junos-eznc        2.2.1   
lazy-object-proxy 1.4.1   
lxml              4.3.3   
MarkupSafe        1.1.1   
mccabe            0.6.1   
more-itertools    7.0.0   
mypy-extensions   0.4.1   
napalm            2.4.0   
ncclient          0.6.4   
netaddr           0.7.19  
netmiko           2.3.3   
nornir            2.2.0   
nxapi-plumbing    0.5.2   
paramiko          2.4.2   
pathspec          0.5.9   
pip               19.1.1  
pluggy            0.11.0  
py                1.8.0   
pyasn1            0.4.5   
pycparser         2.19    
pydantic          0.18.2  
pyeapi            0.8.2   
pyIOSXR           0.53    
pylint            2.3.0   
PyNaCl            1.3.0   
pyserial          3.4     
pytest            4.5.0   
PyYAML            5.1     
requests          2.22.0  
ruamel.yaml       0.15.96 
scp               0.13.2  
setuptools        40.8.0  
six               1.12.0  
textfsm           0.4.1   
toml              0.10.0  
typed-ast         1.3.5   
urllib3           1.25.2  
wcwidth           0.1.7   
wrapt             1.11.1  
yamllint          1.15.0  
```

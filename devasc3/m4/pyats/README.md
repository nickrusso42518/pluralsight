# Cisco pyATS and Genie Demo
These files are included for reference to give you a minimum
working example of these powerful tools. This was not covered
in the course as these tools are quite complex and certainly not
beginner-level tools.

## Packages
Be sure to install the required Python packages
following command. `pip install -r requirements.txt`

Ensure that you have `gcc` installed along with the proper Python
development packages needed to compile code. If you have the `Python.h`
file for your specific Python version, there is a good chance that the
install will succeed.

```
$ python --version
Python 3.7.3

$ sudo find / -name "Python.h"
/usr/local/include/python3.7m/Python.h
```

After installation, verify that pyATS and genie are correctly installed.

```
$ which genie
/home/ec2-user/environments/gman37/bin/genie

$ which pyats
/home/ec2-user/environments/gman37/bin/pyats

$ pyats version
You are currently running pyATS version: 19.8
```

## Sample runs
In the `data_ref/` directory, there are two files.
  * `passing_run.txt`: This shows an example where all tests pass. This
    implies all OSPF neighbors are up
  * `failing_run.txt`: This shows an example where some tests fail. I
    broke one of the OSPF neighbors on purpose to simulate this failure.

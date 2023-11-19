# Configuring NetFlow with RESTCONF
Reference the YANG trees displayed in module 2. The `data_ref/` directory
contains an example NetFlow capture using Python's `netflow` package.

Process to collect and view netflow data:
```
python -m netflow.collector -p 2055 -D
(ctrl+c to stop)
gunzip filename.gz
cat filename
```

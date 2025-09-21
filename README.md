# Volatility Helper Scripts
Helper scripts for Volatility 3

(tested with Volatility 3 Framework 2.26.0 only)


## dump_process_memory.py
Uses subprocess moddule. Runs windows.pslist, then enumerates over all the process IDs extracting the process memory of each using windows.memmap. Output is renamed to include both process ID and process name. This makes it easier to load all process memory into tools such as Autopsy (for keywrod searching for example). Text files are also exported fo the plist and memmmap processes. 

```usage: dump_process_memory.py [-h] -f MEMORY_FILE [-o OUTPUT]```


<img width="1078" height="295" alt="image" src="https://github.com/user-attachments/assets/3b35e3d7-3db4-4db7-8920-1ea00213cd58" />



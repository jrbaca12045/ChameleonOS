check_disk_space.py
===================

Purpose
-------
Report disk usage for a drive or path. Prints the percentage used and
the free space in gigabytes. Warns when usage exceeds 80 percent.

Why this exists
---------------
Small, dependency-free utility for checking whether a machine is running
out of room. Useful before large installs, before recording sessions, or
for a daily automated health check.

Requirements
------------
Python 3.6 or later. Uses only the standard library (shutil, sys, io,
argparse). No pip install needed. Cross-platform: works on Windows,
macOS, and Linux.

Usage
-----
    python check_disk_space.py [path]

    path   Optional. Drive or path to check. Default: C:/

Examples
--------
    python check_disk_space.py
        Checks C:/ (the default on Windows).

    python check_disk_space.py D:/
        Checks the D: drive.

    python check_disk_space.py /home
        Checks a specific path on Linux or macOS.

    python check_disk_space.py "C:/Users/you/Documents"
        Checks free space available to a specific folder.

Output
------
    ----------
    [OK] C:/ Usage: 63.4%
         Free: 182.3 GB of 498.1 GB
    [OK] C:/ is operating within normal parameters.
    ----------

When usage exceeds 80 percent, the middle line becomes:
    [WARN] Alert: C:/ exceeds 80% capacity!

Exit codes
----------
    0   Success. Drive/path was read and reported.
    1   Failure. Path could not be read (bad drive letter, missing
        path, permission denied). Error message printed to stdout.

Exit code 1 means you can chain this in scripts:
    python check_disk_space.py C:/ || echo Disk check failed

Limitations
-----------
- Reports the whole volume, not folder-level usage. To see which
  folder is eating space, use a separate tool.
- Uses the platform's native path syntax. On Windows, drive letters
  like C:/ and D:/ work; UNC paths like //server/share may work
  but are untested.
- Free space numbers come from shutil.disk_usage and reflect what
  the operating system reports, which may differ slightly from what
  Explorer shows.

See also
--------
- setup.txt  quick start for a first-time user

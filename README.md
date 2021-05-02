# Creatures Add-on Installer
Automatically(ish) install add-ons to Creatures 3 and/or Docking Station. All original Creatures files are backed up in the event that something goes wrong.

## Usage
There are two folders in the directory:

|Folder|Game|
|---|---|
|C3|Creatures 3|
|DS|Docking Station|

Simply unzip your add-ons into the appropriate folder for the appropriate game. One caveat: If your add-on unzips as a single file, you'll need to create a new folder to move it into.

Once your add-ons are unzipped, simply run Creatures Add-on Installer.

## Command-line Options
```
usage: addoninstall.py [-h] [-i PATH] [-b PATH] [-c PATH] [-s] [-u]

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input_dir PATH
                        The path to the input directory containing the add-ons
                        to install.
  -b PATH, --backup_dir PATH
                        The path to the directory where backups of the
                        original game files are stored.
  -c PATH, --creatures_dir PATH
                        The path to your Creatures Exodus installation.
  -s, --skip_backup     Don't create any backups, just install patches and
                        add-ons.
  -u, --uninstall       Uninstall add-ons and restore any original files from
                        backups (if available).
```

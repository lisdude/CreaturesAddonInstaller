from argparse import ArgumentParser
from pathlib import Path
from shutil import copy
from filecmp import cmp

# Globals
version = "0.3"

# Cos is 0 here because its location is game-dependant, but it still needs to be present
# because this dictionary is used as the basis of the file search.
filetypes = {
    "cos": 0,
    "c16": "Images",
    "s16": "Images",
    "agents": "My Agents",
    "catalogue": "Catalogue",
    "wav": "Sounds",
    "mng": "Sounds"
}

file_exceptions = {
    "!DS splash map.cos": "Bootstrap/000 Switcher",
    "DS Music.cos": "Bootstrap/000 Switcher"
}

full_name = {"C3": "Creatures 3", "DS": "Docking Station"}
##

# Command-line Arguments
parser = ArgumentParser()

parser.add_argument("-i", "--input_dir",
type = Path,
metavar = "PATH",
default = Path().absolute(),
help = "The path to the input directory containing the add-ons to install.")

parser.add_argument("-b", "--backup_dir",
type = Path, 
metavar = "PATH",
default = Path().home() / "Documents" / "Creatures Patch Backups",
help = "The path to the directory where backups of the original game files are stored.")

parser.add_argument("-c", "--creatures_dir",
type = Path, 
metavar = "PATH",
default = Path().home() / "Documents" / "Creatures",
help = "The path to your Creatures Exodus installation.")

parser.add_argument("-s", "--skip_backup",
action = "store_true",
help = "Don't create any backups, just install patches and add-ons.")

parser.add_argument("-u", "--uninstall",
action = "store_true",
help = "Uninstall add-ons and restore any original files from backups (if available).")

parser.add_argument("--version", action = "store_true", help = "Display the version number.")

args = parser.parse_args()
##

# Return the target directory for the given file extension.
def filetype_dir(game, file):
    name = file.name
    extension = file.suffix.replace(".", "")
    # Cos is a special case because its destination depends on the game.
    if extension == "cos":
        # Some fixes have special exceptions. If there are enough add-ons like this,
        # we may have to come up with a more clever solution.
        exceptioned = file_exceptions.get(file.name, 0)
        if exceptioned != 0:
            return exceptioned
        else:
            return "Bootstrap/" + ("001 World" if game == "C3" else "010 Docking Station")
    else:
        return filetypes.get(extension, 0)

# Copy original game files into a backup directory.
def backup(game):
    file_list = args.input_dir / game
    for extension in filetypes:
        for file in file_list.glob("**/*." + extension):
            # Directory Creatures stores this filetype in (e.g. Images):
            filetype_directory = filetype_dir(game, file)
            # Path to the appropriate directory for the current Creatures install (e.g. /Creatures 3/Images):
            source = args.creatures_dir / full_name[game] / filetype_directory
            # Path to our backup location (e.g. Backups/Creatures 3/My Cool Patch/Images):
            backup = args.backup_dir / full_name[game] / file.parent.name / filetype_directory
            # Full path to the actual file in the current Creatures install (e.g. /Creatures 3/Images/worm.c16):
            current_file = source / file.name
            if not current_file.exists():
                print("SKIPPED: '" + file.name + "' from '" + file.parent.name + "' doesn't exist in current install. Nothing to backup.")
            elif cmp(current_file, file):
                print("SKIPPED: Currently installed '" + file.name + " is already from '" + file.parent.name + "'.")
            else:
                print("Backing up '" + file.name + "' from '" + file.parent.name + "'...")
                backup.mkdir(parents=True, exist_ok=True)
                copy(current_file, backup)

# Copy add-on files into the original game directories based on filetype.
def install(game):
    file_list = args.input_dir / game
    for extension in filetypes:
        for file in file_list.glob("**/*." + extension):
            # Directory Creatures stores this filetype in (e.g. Images):
            filetype_directory = filetype_dir(game, file)
            # Path to the appropriate directory for the current Creatures install (e.g. /Creatures 3/Images):
            dest = args.creatures_dir / full_name[game] / filetype_directory
            print("Copying '" + file.name + "' from '" + file.parent.name + "'...")
            copy(file, dest)

# Delete add-on files from the original game directories. If present, copy the matching
# backup file from the backup directory back to the original game directory.
def uninstall(game):
    file_list = args.input_dir / game
    for extension in filetypes:
        for file in file_list.glob("**/*." + extension):
            # Directory Creatures stores this filetype in (e.g. Images):
            filetype_directory = filetype_dir(game, file)
            # Path to the appropriate directory for the current Creatures install (e.g. /Creatures 3/Images):
            dest = args.creatures_dir / full_name[game] / filetype_directory
            # Path to our backup location (e.g. Backups/Creatures 3/My Cool Patch/Images):
            backup = args.backup_dir / full_name[game] / file.parent.name / filetype_directory
            # Full path to the actual file in the current Creatures install (e.g. /Creatures 3/Images/worm.c16):
            current_file = dest / file.name
            print("Deleting '" + file.name + "' from '" + file.parent.name + "'...")
            current_file.unlink()
            current_file = backup / file.name
            if current_file.exists():
                print("Restoring '" + file.name + " (" + file.parent.name + ") from backup...")
                copy(current_file, dest)


def main():
    print("Creatures Exodus Add-on Installer v" + version)
    if not args.version:
        print("\nSource directory: " + str(args.input_dir))
        print("Backup directory: " + str(args.backup_dir))
        print("Creatures directory: " + str(args.creatures_dir) + "\n")
        if args.uninstall:
            print("Uninstalling...")
            uninstall("C3")
            uninstall("DS")
        else:
            if args.skip_backup:
                print("Skipping backups...")
            else:
                print("Creating backups...")
                backup("C3")
                backup("DS")
            print("Installing add-ons...")
            install("C3")
            install("DS")
        print("\nDone!")

if __name__ == "__main__":
    main()

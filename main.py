import os
import sys
import datetime
import shutil

"""

    THIS SCRIPT IS DESIGNED TO MAKE SORTING FILES EASIER BY
    ITERATING OVER EVERY FILE/DIRECTORY (NON-RECURSIVE) IN
    A GIVEN DIRECTORY, IDENTIFYING THE TYPE OF EACH FILE
    BY COMPARING ITS EXTENSION, RENAMING THAT FILE IF NEEDED,
    BEFORE FINALLY MOVING IT INTO ITS RESPECTIVE DIRECTORY
    BASED ON THAT FILETYPE.

"""

# Directory to be sorted
DEFAULT_PATH = "C://Users//Matt//Downloads"

# Destination Paths based on file type
PROGRAM = "A://Programs"
DIRECTORY = "A://Programs"
DOCUMENT = "A://Documents"
VIDEO = "A://Videos"
IMAGE = "A://Images"
MUSIC = "A://Music"
OTHER = "A://Other"

# Log all movements in a text file
PATH_TO_LOG_FILE = "A://Logs.txt"

# All file extensions included in the sort function
FILETYPES = {
    "IMAGE": (".JPG", ".PNG", ".AI", ".PSD", ".SVG", ".GIF",
              ".BMP", ".ICO", "JPEG", ".TIF", "TIFF", ".RAW"),
    "VIDEO": (".MOV", ".MP4", ".AVI", "MKV", ".WMV", ".MPEG-4"),
    "DOCUMENT": (".DOC", ".CSV", ".PPTX", ".TXT", ".XLSX", ".PDF", ".DOCX"),
    "PROGRAM": (".EXE", ".WASM", ".PY"),
    "MUSIC": (".MP3", ".WAV", ".MPEG")
}

# Compare file extension against common extensions to identify filetype


def get_filetype(filename):
    for filetype in FILETYPES:
        for extension in FILETYPES[filetype]:
            if filename.endswith(extension):
                return filetype
    return "OTHER"

# Search directory subfiles for video files, if found send directory to
# the Video directory instead


def check_subfiles(dir_path):
    for file in os.listdir(dir_path):
        file_upper = file.upper()
        for extension in (FILETYPES["VIDEO"]):
            if file_upper.endswith(extension):
                return VIDEO
    return DIRECTORY

# Rename the image file to a unique integer in ascending order


def rename_image(file_path, extension, scan_path):
    filename = 0
    # Search Image directory for file with largest integer value. The image
    # file wil be renamed to that value + 1
    for file in os.listdir(IMAGE):
        # Non integer files in target directory are ignored
        if os.path.splitext(file)[1]:
            stripped_file = 0
            try:
                stripped_file = int(os.path.splitext(file)[0])
            except:
                print(f"Unable to cast {file} to integer")
            if filename <= stripped_file:
                filename = stripped_file
    # Rename the image file
    new_filename = str(filename + 1) + extension
    new_file_path = os.path.join(scan_path, new_filename)
    os.rename(file_path, new_file_path)
    return new_filename, new_file_path

# Append an integer to the end of the filename


def rename_file(file_path, filename, file_destination, scan_path):
    counter = 1
    file = os.path.splitext(filename)[0]
    extension = os.path.splitext(filename)[1]
    # Increment the integer until the filename is unique
    while filename in os.listdir(file_destination):
        filename = file + "(" + str(counter) + ")" + extension
        counter += 1
    # Change the filename
    new_file_path = os.path.join(scan_path, filename)
    os.rename(file_path, new_file_path)
    return filename, new_file_path

# Send information to a .txt file for each file migration


def logger(file_destination, old_filename, new_filename):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
    event_log = open(PATH_TO_LOG_FILE, "a")
    event_log.write(
        f"{timestamp}    {file_destination :<20}{old_filename :<29}>>{new_filename :>29}  \n")
    event_log.close()
    print(f"successfully moved {old_filename} to {file_destination}!")
    return


def main():
    scan_path = sys.argv[1] if len(sys.argv) == 2 else DEFAULT_PATH
    print(f"Organising files at: {scan_path}")

    # Iterate over every file in directory
    for filename in os.listdir(scan_path):
        extension = os.path.splitext(filename)[1]
        filename_upper = filename.upper()
        file_path = os.path.join(scan_path, filename)
        # If the file is a directory, check its contents for video files
        if not extension:
            file_destination = check_subfiles(file_path)
        # If the file is not a directory, compare extensions to determine filetype
        else:
            file_destination = globals()[get_filetype(filename_upper)]

        # If the file is an image, it is renamed as a unique
        # integer in target directory
        if file_destination == IMAGE:
            new_filename, new_file_path = rename_image(file_path, extension, scan_path)
        # If the filename already exists in target location, the file is renamed
        elif filename in os.listdir(file_destination):
            new_filename, new_file_path = rename_file(
                file_path, filename, file_destination, scan_path)
        else:
            new_file_path = file_path
            new_filename = filename
        # Attempt to move the file into the target directory and log
        # the migration if successful
        try:
            shutil.move(new_file_path, file_destination)
            logger(file_destination, filename, new_filename)
        except:
            print(f"Unable to transfer {filename}")
    print(f"Task finished successfully!")
    return 0


if __name__ == "__main__":
    main()

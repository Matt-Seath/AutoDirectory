import os
import datetime
import shutil


# Directory to be sorted
PATH = "C://Users//Matt//Downloads"

# Destination Paths based on file type
EXECUTABLE = "F://Executables"
DIRECTORY = "F://Directories"
DOCUMENT = "F://Documents"
VIDEO = "F://Videos"
IMAGE = "F://Images"
OTHER = "F://Other"

# Log all movements in a text file
PATH_TO_LOG_FILE = "F://Logs.txt"

# All file extensions included in the sort function
FILETYPES = {
    "IMAGE": (".JPG", ".PNG", ".AI", ".PSD", ".SVG", ".GIF",
              ".BMP", ".ICO", "JPEG", ".TIF", "TIFF", ".RAW"),
    "VIDEO": (".MOV", ".MP4", ".AVI", "MKV", ".WMV", ".MPEG-4"),
    "DOCUMENT": (".DOC", ".CSV", ".PPTX", ".TXT", ".XLSX", ".PDF"),
    "EXECUTABLE": (".EXE", ".WASM", ".PY")
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


def rename_image(file_path, extension):
    filename = 0
    # Search Image directory for file with largest integer value. The image
    # file wil be renamed +1 greater
    for file in os.listdir(IMAGE):
        try:
            stripped_file = int(os.path.splitext(file)[0])
        except:
            print(f"Unable to cast {file} to integer")
        if filename <= stripped_file:
            filename = stripped_file
    new_filename = str(filename + 1) + extension
    new_file_path = os.path.join(PATH, new_filename)
    os.rename(file_path, new_file_path)
    return new_filename, new_file_path

# TODO


def rename_file(file_path, filename, file_destination):
    counter = 1
    while filename in os.listdir(file_destination):
        filename = filename + "(" + str(counter) + ")"
        counter += 1
    new_file_path = os.path.join(PATH, filename)
    os.rename(file_path, new_file_path)
    return filename, new_file_path

# Send information to a .txt file for each file migration


def logger(file_destination, old_filename, new_filename):
    now = datetime.datetime.now()
    timestamp = now.strftime("%d/%m/%Y, %H:%M:%S")
    event_log = open(PATH_TO_LOG_FILE, "a")
    event_log.write(
        f"{timestamp}    {file_destination :<20}{old_filename :<20}>>{new_filename :>20}  \n")
    event_log.close()
    print(f"successfully moved {old_filename} to {file_destination}!")


def main():
    for filename in os.listdir(PATH):
        extension = os.path.splitext(filename)[1]
        filename_upper = filename.upper()
        file_path = os.path.join(PATH, filename)
        if not extension:
            file_destination = check_subfiles(file_path)
        else:
            file_destination = globals()[get_filetype(filename_upper)]

        if file_destination == IMAGE:
            new_filename, new_file_path = rename_image(file_path, extension)
        elif filename in os.listdir(file_destination):
            new_filename, new_file_path = rename_file(
                file_path, filename, file_destination)
        else:
            new_file_path = file_path
            new_filename = filename
        try:
            shutil.move(new_file_path, file_destination)
            logger(file_destination, filename, new_filename)
        except:
            print(f"Unable to transfer {filename}")


if __name__ == "__main__":
    main()

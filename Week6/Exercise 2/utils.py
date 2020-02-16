import os
import platform
import argparse
import sys


def lookup_and_save_filenames(folder_path, save_file_path):
    entries = os.listdir(folder_path)
    # Doesn't seem to be necessary, but I don't know why
    # if platform.system() == 'Windows':
    #     newline=''
    # else:
    #     newline=None
    #with open(save_file_path, 'w', newline=newline) as save_file:
    with open(save_file_path, 'w') as save_file:
        for entry in entries:
            if os.path.isfile(folder_path + "/" + entry):
                save_file.write(entry + "\n")
            else:
                save_file.write(entry + " (subfolder)" + "\n")
    print("List of files saved in: " + save_file_path)

def lookup_and_save_all_filenames_recursive(folder_path, save_file_path, FILE):
    entries = os.listdir(folder_path)
    if not FILE:    
        with open(save_file_path, 'w') as save_file:
            for entry in entries:
                if(os.path.isfile(folder_path + "/" + entry)):
                    save_file.write(entry + "\n")
                else:
                    lookup_and_save_all_filenames_recursive(folder_path + "/" + entry, None, save_file)
                    #save_file.write(entry + " (subfolder)" + "\n")
                    print("List of files saved in: " + save_file_path)
    else:
        for entry in entries:
            if os.path.isfile(folder_path + "/" + entry):
                FILE.write(entry + "\n")
            else:
                lookup_and_save_all_filenames_recursive(folder_path + "/" + entry, None, FILE)
    
def print_first_lines(files):
    for file in files:
        if not os.path.isfile(file):
            print('File ' + file + ' does not exist.')
            continue
        with open(file) as file_object:
            print(str.strip(file_object.readline()))

def print_lines_with_email(files):
    for file in files:
        if not os.path.isfile(file):
            print('File ' + file + ' does not exist.')
            continue
        with open(file) as file_object:
            for line in file_object:
                if '@' in line:
                    print(str.strip(line))

def save_headlines(save_file_path, files):
    with open(save_file_path, 'w') as save_file:
        for file in files:
            if not os.path.isfile(file):
                print('File ' + file + ' does not exist.')
                continue
            with open(file) as file_object:
                for line in file_object:
                    if line[0] == '#' and not line[1] == '#':
                        save_file.write(str.strip(line) + "\n")
    print("Headlines saved in file with path: " + save_file_path)
                    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that looks through files and either prints content from these files or saves the content in a new file.')
    parser.add_argument('-sfn', '--save_file_names', help='Provide a save file name (.txt). Use this option to store all file names from the given folder path in a new text file.')
    parser.add_argument('-safn', '--save_all_file_names', help='Provide a save file name (.txt). Use this option to store all file names from the given folder path (including all files in all sub folders) in a new text file.')
    parser.add_argument('-p', '--print_first_lines', default='UNSPECIFIED', nargs='?', help='Use this option to print the first line of all the files provided.')
    parser.add_argument('-e', '--print_emails', default='UNSPECIFIED', nargs='?', help='Use this option to print all lines that contain an email from all the files provided.')
    parser.add_argument('-sh', '--save_headlines', help='Provide a save file name (.txt). Use this option to look through .md files and save all headlines in a new text file.')
    parser.add_argument('filepaths', metavar='Paths', nargs='+',
                    help='One or more paths to files or folders. Either the first or all of these path arguments may be used depending on which other arguments you provide.')
    args = parser.parse_args()
    if args.save_file_names:
        lookup_and_save_filenames(args.filepaths[0], args.save_file_names)
    elif args.save_all_file_names:
        lookup_and_save_all_filenames_recursive(args.filepaths[0], args.save_all_file_names, None)
    elif '-p' in sys.argv:
        print_first_lines(args.filepaths)
    elif '-e' in sys.argv:
        print_lines_with_email(args.filepaths)
    elif args.save_headlines:
        save_headlines(args.save_headlines, args.filepaths)
    else:
        print("You need to add another argument. Use -h to get help")


    # first function takes a path to a folder and writes all filenames in the folder to a specified output file
    # second takes a path to a folder and write all filenames recursively (files of all sub folders too)
    # third takes a list of filenames and print the first line of each
    # fourth takes a list of filenames and print each line that contains an email (just look for @)
    # fifth takes a list of md files and writes all headlines (lines starting with #) to a file. 
    # Make sure your module can be called both from cli and imported to another module.
    # Create a new module that imports utils.py and test each function.

    
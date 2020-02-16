import csv
import argparse
import sys

def print_file_content(filepath):
    with open(filepath) as file:
        reader = csv.reader(file)
        for row in reader:
            print(str(row))

def write_list_to_file(output_file, lst):
    with open("./download_dumps/" + output_file, 'w') as file:
        for element in lst:
            file.write(str(element) + "\n")

def read_csv(input_file):
    with open(input_file) as file:
        reader = csv.reader(file)
        res = []
        for row in reader:
            res += [row]
        return res

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='A program that reads a csv file and prints the content')
    parser.add_argument('-f', '--file', help='A file name with extension (.txt). Use this option to store output in a file instead of printing content')
    parser.add_argument("filename", help="File path to the csv file you want to read")
    args = parser.parse_args()
    if (args.file):
        data = read_csv(args.filename)
        write_list_to_file(args.file, data)
        print("File saved to: ./download_dumps/" + args.file)
    else:
        print_file_content(args.filename)


#!/usr/bin/env python

import os
import shutil
import argparse
import sys

BACKUP_LOCATION = "change to the directory where you want your files to be saved in"

#Create a file contain the directory where you will restore you files in 
def creat_dir(directory, filename, text):
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Combine directory path and filename
    file_path = os.path.join(directory, filename)

    # Write text to the file
    with open(file_path, 'w') as file:
        file.write(text)

#read the directory for the backuped file 
def read_dir(directory, filename):
    # Combine directory path and filename
    file_path = os.path.join(directory, filename)

    # Read text from the file
    with open(file_path, 'r') as file:
        text = file.read()
    
    return text

def has_sudo():
    return os.geteuid() == 0

def backup(source_dir, dest_dir):
    base_name = os.path.basename(os.path.normpath(source_dir))
    filename = base_name+".txt"
    creat_dir(BACKUP_LOCATION,filename,source_dir)
    shutil.make_archive(os.path.join(dest_dir, base_name), 'zip', source_dir)

def restore(filename):

    backup_file = os.path.join(BACKUP_LOCATION, filename + ".zip")
    dest_dir = read_dir(BACKUP_LOCATION,filename+".txt")
    shutil.unpack_archive(backup_file, dest_dir)

def list_backups():
    backup_files = [f for f in os.listdir(BACKUP_LOCATION) if f.endswith('.zip')]
    if backup_files:
        print("Backup files:")
        for file in backup_files:
            print(file)
    else:
        print("No backup files found.")

def delete_backup(filename):
    if not has_sudo():
        print("This operation requires sudo permission. Please run with sudo.")
        return
    backup_file_path = os.path.join(BACKUP_LOCATION, filename + ".zip")
    if os.path.exists(backup_file_path):
        os.remove(backup_file_path)
    backup_dir_path = os.path.join(BACKUP_LOCATION, filename + ".txt")
    if os.path.exists(backup_dir_path):
        os.remove(backup_dir_path)
        print(f"{filename}.zip deleted successfully.")
    else:
        print(f"{filename}.zip not found.")

def main():
    parser = argparse.ArgumentParser(description="Backup and Restore Tool")
    parser.add_argument("-b", "--backup", help="Backup a file or directory")
    parser.add_argument("-r", "--restore", help="Restore a backed-up file or directory")
    parser.add_argument("-l", "--list", action="store_true", help="List all backup files")
    parser.add_argument("-d", "--delete", help="Delete a specific backup file")
    args = parser.parse_args()

    if not has_sudo():
        print("This tool requires sudo permission to deal with system files.")
        print("Please enter your sudo password to continue.")
        os.system("sudo ls > /dev/null")

    if args.backup:
        backup(args.backup, BACKUP_LOCATION)
        print("Backup successful.")
    elif args.restore:
        restore(args.restore)
        print("Restore successful.")
    elif args.list:
        list_backups()
    elif args.delete:
        delete_backup(args.delete)
    else:
        parser.print_help()

if name == "main":
    main()

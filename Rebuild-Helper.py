#!/usr/bin/env python3
import sys
import os
import subprocess


START_DIR = os.getcwd()
HOME = os.getenv("HOME")


def rebuild_helper(package_name):
    print(package_name)
    try:
        os.mkdir(package_name)
    except FileExistsError:
        print('Directory exists! Quit?')
        answer = input()
        if answer == 'y' or answer == 'yes':
            return
    os.chdir(os.getcwd() + '/' + package_name + '/')
    #  print(os.getcwd())
    subprocess.call(['apt-get', 'source', package_name])
    subprocess.call(['sudo', 'apt-get', 'build-dep', package_name])


def main():
    arg_number = 0
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            print('Type the name of the package you want to',
                  'rebuild with -n or --name')
            return
        if arg == '-n' or arg == '--name':
            rebuild_helper(sys.argv[arg_number + 1])

        arg_number += 1


if __name__ == '__main__':
    print("changing to work directory...")
    os.chdir(HOME + '/src/src_Work/')
    main()

#!/usr/bin/env python3
# coding=utf-8
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
    subprocess.call(['apt-get', '-t', 'unstable', 'source', package_name])
    subprocess.call(['sudo', 'apt-get', 'build-dep', package_name])
    print("would you like to compile the program and",
          "copy foo to foo.orig ?")
    answer = input()
    if answer == 'y' or answer == 'yes':
        directories = [name for name in os.listdir(".") if os.path.isdir(name)]
        os.chdir(directories[0])
        #  print(os.getcwd())
        subprocess.call(['dpkg-buildpackage', '-uc', '-us', '-nc', '-b'])
        subprocess.call(['cp', '-r', '../../' + package_name, '../../' + package_name + '.orig'])


def diff_creator(package_name):
    print("MAKE ME!: diff_creator")


def main():
    arg_number = 0
    for arg in sys.argv:
        if arg == '-h' or arg == '--help':
            print('Type the name of the package you want to',
                  'rebuild with -n or --name or diff with -d or --diff')
            return
        if arg == '-n' or arg == '--name':
            rebuild_helper(sys.argv[arg_number + 1])

        if arg == '-d' or arg == '--debug':
            diff_creator(sys.argv[arg_number + 1])

        arg_number += 1


if __name__ == '__main__':
    os.chdir(HOME + '/src/src_Work/')
    main()

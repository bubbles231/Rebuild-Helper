#!/usr/bin/env python3
# coding=utf-8
import sys
import os
import subprocess
import configparser


HOME = os.getenv("HOME")


def rebuild_helper(package_name):
    """

    :param package_name: Debian package name
    :return: Nothing
    """
    print("Building " + package_name + " with Clang")

    try:
        os.mkdir(package_name)
    except FileExistsError:
        print('WARNING: Directory exists! Quit? [y/N]')
        answer = input()
        if answer == 'y' or answer == 'yes':
            return

    os.chdir(os.getcwd() + '/' + package_name + '/')
    subprocess.call(['apt-get', '-t', 'unstable', 'source', package_name])
    subprocess.call(['sudo', 'apt-get', 'build-dep', package_name])

    print("PROMPT: would you like to compile the program and",
          "copy foo to foo.orig? [Y/n]")
    answer = input()
    if answer == 'y' or answer == 'yes' or answer == "":
        directories = [name for name in os.listdir(".") if os.path.isdir(name)]
        os.chdir(directories[0])
        subprocess.call(['dpkg-buildpackage', '-uc', '-us', '-nc', '-b'])
        subprocess.call(['cp', '-r', '../../' + package_name, '../../' + package_name + '.orig'])
    else:
        print("Aborting compilation...")
        sys.exit(0)


def configure_work_dir(wd_default):
    """
    This function will configure the working directory to rebuild packages in.
    :param wd_default: Default working directory
    :return: working_dir (path)
    """
    prompting = True
    configuring = True
    is_correct = False
    working_dir = wd_default

    while configuring:
        print("PROMPT: What is your package rebuilding directory path?\n" +
              "INFO: (Program will append your home directory to the path entered)")
        print("INFO: (Default = " + HOME + working_dir)
        working_dir = input()

        if working_dir == "":
            working_dir = wd_default

        while prompting:
            print("INFO: You choose: " + HOME + working_dir + " Is this correct? [Y/n]")
            answer = input()
            if answer == 'y' or answer == "":
                is_correct = True
                prompting = False
            elif answer == 'n':
                is_correct = False
                break
            else:
                print("WARNING: You entered an invalid option")
                prompting = True

        if is_correct:
            configuring = False

    return working_dir


def create_directory(working_dir):
    """
    Create a directory that the user wanted if it doesn't exist.
    :param working_dir: Path
    """
    print("WARNING: No such file or directory for " + HOME + working_dir)
    prompting = True

    while prompting:
        print("PROMPT: Create directory? [Y/n]")
        answer = input()
        if answer == 'y' or answer == "":
            print("INFO: Creating " + HOME + working_dir)
            os.makedirs(HOME + working_dir)
            prompting = False
        elif answer == 'n':
            print("INFO: Not creating directory, exiting program...")
            sys.exit(0)
        else:
            print(answer, "is not a valid option. Try again...")
            prompting = True


def main():
    """
    Function that makes the program take arguments and runs the main method to rebuild packages.
    :return: Nothing
    """
    config = configparser.ConfigParser()

    # Test if there is a config file
    if os.path.isfile(HOME + '/.Rebuild-Helper.ini'):
        # Read existing configuration
        config.read(HOME + '/.Rebuild-Helper.ini')
        work_dir = config['Work Directory']['WorkDir']
    else:
        # Make default configuration
        config['Work Directory'] = {'WorkDir': '/src/src_Work/'}
        with open(HOME + '/.Rebuild-Helper.ini', 'w') as configfile:
            config.write(configfile)
        config.read(HOME + '/.Rebuild-Helper.ini')
        work_dir = config['Work Directory']['WorkDir']

    try:
        os.chdir(HOME + work_dir)
    except FileNotFoundError:
        pass

    if ('-c' in sys.argv) or ('--config-directory' in sys.argv):
        work_dir = configure_work_dir(work_dir)
        config['Work Directory']['WorkDir'] = work_dir
        with open(HOME + '/.Rebuild-Helper.ini', 'w') as configfile:
            config.write(configfile)
        try:
            os.chdir(HOME + work_dir)
        except FileNotFoundError:
            create_directory(work_dir)
            os.chdir(HOME + work_dir)

    arg_number = 0
    for arg in sys.argv:

        if arg == '-h' or arg == '--help':
            print('\n   -n, --name              Type the name of the package you want to rebuild\n\n',
                  '  -c, --config-directory  Configure which directory to recompile packages in\n',
                  '                            [Saves your choice in a configuration file]\n\n',
                  '  -d, --debug             This flag does nothing at the moment :P\n\n',
                  '  -h, --help              Print this help message\n')
            sys.exit(0)

        if arg == '-n' or arg == '--name':
            try:
                os.chdir(HOME + work_dir)
            except FileNotFoundError:
                create_directory(work_dir)
                os.chdir(HOME + work_dir)
            try:
                rebuild_helper(sys.argv[arg_number + 1])
            except IndexError:
                print("Must specify a package name")
                break

        if arg == '-d' or arg == '--debug':
            print("No debugging info to show for now")
        arg_number += 1


if __name__ == '__main__':
    main()

#!/usr/bin/env python

import getopt, os, shutil, subprocess, sys, urllib, zipfile

class Installer:
    def __init__(self, src, dst):
        self.name = 'munch'
        self.src = src
        self.dst = dst
        self.errors = []
        self.make_dir()
        self.setup_munch()

    def make_dir(self):
        if not os.path.exists(self.dst):
            os.makedirs(self.dst)

    def setup_munch(self):
        """Install Munch to /usr/local/bin/"""
        print "Installing Munch..."
        try:
            subprocess.call(['chmod', '+x', self.src])
            shutil.copy2(self.src, self.dst + '/' + self.name)
            print 'Munch installed successfully.'
            return True
        except:
            self.errors.append('There was a problem installing Munch.')
            return False


class Munch:
    def __init__(self, branch, name):
        self.branch = branch
        self.url = 'https://github.com/bigspring/lunchbox/archive/{}.zip'.format(branch)
        self.lunchbox_zip = 'lunchbox.zip'
        self.composer_filename = 'composer.json'
        self.composer_data = False
        self.project_name = name
        self.files_to_delete = ['composer.lock', self.lunchbox_zip, self.composer_filename]
        self.dirs_to_delete = ['vendor']
        self.missing_dependencies = []
        self.idiot_check()
        self.execute()


    def idiot_check(self):
        """Check for dependencies. Why don't you already have these dependencies? WHYYYY"""
        dependencies = [['composer', '-q']]
        for dependency in dependencies:
            try:
                subprocess.call(dependency) # attempt to run
            except:
                self.missing_dependencies.append(dependency)
        if (len(self.missing_dependencies) == 0):
            return True

        print 'Could not find the following dependencies: {}'.format(','.join(str(md) for md in self.missing_dependencies))
        print 'Exiting...'
        sys.exit(2)

    def execute(self):
        """Run the Lunchbox setup"""
        print "Fetching Lunchbox..."
        self.fetch(self.lunchbox_zip)
        print "Lunchbox retrieved."
        print "Opening Lunchbox..."
        self.open_lunchbox()
        print "Lunchbox open."
        print "Munching lunch..."
        print "-------------------------------------"
        self.munch_lunch()
        print "-------------------------------------"
        print "Lunch eaten."
        print "Cleaning up mess..."
        cleanup(self.files_to_delete, self.dirs_to_delete)
        print "Mess cleaned up."

    def fetch(self, file):
        """Download the Lunchbox repo as a zip file"""
        try:
            urllib.urlretrieve(self.url, file)
        except:
            print "There was a problem getting the repo."
            print "Please ensure that the URI '{}' exists and that the".format(self.url)
            print "monolith branch specified in composer.json also exists."

    def open_lunchbox(self):
        """Prepare Lunchbox files"""
        zf = zipfile.ZipFile(self.lunchbox_zip, 'r')
        self.composer_data = zf.read('lunchbox-{}/'.format(self.branch) + self.composer_filename)
        name_prompt = 'Enter the project name: '
        if not self.project_name:
            self.project_name = raw_input(name_prompt).replace(' ', '-')
            while os.path.isdir('{}/{}'.format(os.getcwd(), self.project_name)):
                print "A directory with that name already exists."
                self.project_name = raw_input(name_prompt)

        print "Project name is " + self.project_name
        self.composer_data = self.composer_data.replace('LUNCHBOX_DIR', self.project_name)
        file = open(self.composer_filename, 'w')
        file.write(self.composer_data)
        file.close()

    def munch_lunch(self):
        """Run composer install"""
        try:
            subprocess.call(['composer', 'install'])
        except:
            print "There was a problem. Please ensure that composer is installed and functioning."
            print "Exiting..."
            sys.exit(2)


def correct_usage():
    """Print usage information"""
    print "usage: munch [-h], [-n projectname] [-b]"
    print "\t-h --help\tPrint correct usage and options"
    print "\t-u --update\tUpdate Munch"
    print "\t-n --name\tDefine the project name"
    print "\t-b --branch\tBranch from which to pull lunchbox"

def install(src, dst):
    """Run installer"""
    install = Installer(src, dst)
    if len(install.errors) > 0:
        for error in install.errors:
            print error
        sys.exit(2)

def update(dst):
    """Update Munch"""
    branch = 'master'
    url = 'https://github.com/bigspring/munch/archive/{}.zip'.format(branch)
    munch_zip = 'munch.zip'
    munch_py = 'munch.py'
    urllib.urlretrieve(url, munch_zip)
    zf = zipfile.ZipFile(munch_zip, 'r')
    munch_file = zf.read('munch-{}/'.format(branch) + munch_py)
    file = open(munch_py, 'w')
    file.write(munch_file)
    file.close()
    dst = '/usr/local/bin' # bin directory
    install('munch.py', dst)
    files_to_delete = [munch_zip, munch_file, munch_py]
    cleanup(files_to_delete, [])
    sys.exit(2)

def cleanup(files_to_delete, dirs_to_delete):
    """Cleanup unrequired files/directories"""
    for file in files_to_delete:
        if os.path.exists(os.getcwd() + '/' + file):
            os.remove(os.getcwd() + '/' + file)
    for directory in dirs_to_delete:
        if os.path.exists(directory):
            shutil.rmtree(directory)

if __name__ == '__main__':

    # define defaults
    bin_path = '/usr/local/bin/munch'
    src = os.path.realpath(__file__) # current filepath
    dst = '/usr/local/bin' # bin directory
    branch = 'master'
    project_name = False
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hun:b:', ['help', 'update', 'name=', 'branch='])
    except getopt.GetoptError:
        correct_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            correct_usage()
        elif opt in ('-n', '--name'):
            project_name = arg
        elif opt in ('-b', '--branch'):
            branch = arg
        elif opt in ('-u', '--update'):
            update(dst)

    # install Munch if not found or installing from repo; otherwise run
    if not os.path.isfile(bin_path) or __file__ == './munch.py':
        install(src, dst)
    else:
        munch = Munch(branch, project_name)

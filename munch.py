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
            shutil.copy2(self.src, self.dst + self.name)
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
        self.execute()

    def execute(self):
        """Run the Lunchbox setup"""
        print "Fetching Lunchbox..."
        self.fetch_lunchbox()
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
        self.cleanup()
        print "Mess cleaned up."

    def fetch_lunchbox(self):
        """Download the Lunchbox repo as a zip file"""
        try:
            urllib.urlretrieve(self.url, self.lunchbox_zip)
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
            self.project_name = raw_input(name_prompt)
            while os.path.isdir(os.getcwd() + '/' + self.project_name):
                print "A directory with that name already exists."
                self.project_name = raw_input(name_prompt)
        else:
            self.project_name = os.path.dirname(os.getcwd())
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

    def cleanup(self):
        """Cleanup unrequired files/directories"""
        for file in self.files_to_delete:
            if os.path.exists(os.getcwd() + '/' + file):
                os.remove(os.getcwd() + '/' + file)
        for dir in self.dirs_to_delete:
            if os.path.exists(dir):
                shutil.rmtree(dir)

def correct_usage():
    """Print usage information"""
    print "usage: munch [-h], [-n projectname] [-b]"
    print "\t-h --help\tPrint correct usage and options"
    print "\t-n --name\tProvide project name"
    print "\t-b --branch\tBranch from which to pull lunchbox"

def install(src, dst):
    """Run installer"""
    install = Installer(src, dst)
    if len(install.errors) > 0:
        for error in install.errors:
            print error
        sys.exit(2)

if __name__ == '__main__':

    sys.exit(2)

    # define defaults
    bin_path = '/usr/local/bin/munch'
    src = os.path.realpath(__file__) # current filepath
    dst = '/usr/local/bin/' # bin directory
    branch = 'master'
    project_name = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hn:b:u:', ['help', 'name=', 'branch='])
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

    # install Munch if not found or installing from repo; otherwise run
    if not os.path.isfile(bin_path) or __file__ == './munch.py':
        install(src, dst)
    else:
        munch = Munch(branch, project_name)

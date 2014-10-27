#!/usr/bin/env python

import getopt, os, shutil, subprocess, sys, urllib, zipfile

class Installer:
    def __init__(self, src, dst):
        self.name = 'munch'
        self.src = src
        self.dst = dst
        self.errors = []
        self.make_dir()
        #self.setup_terminal_notifier()
        self.setup_munch()

    def make_dir(self):
        if not os.path.exists(self.dst):
            os.makedirs(self.dst)

    def setup_terminal_notifier(self):
        """Install Terminal Notifier with Homebrew"""
        print "Installing Terminal Notifier..."
        print "-------------------------------------"
        try:
            subprocess.call(['brew', 'install', 'terminal-notifier'])
            print "-------------------------------------"
            return True
        except:
            print "-------------------------------------"
            print "There was a problem installing Terminal Notifier. Please try again or install manually."
            self.problem.append('Problem installing Terminal Notifier.')
            return False

    def setup_munch(self):
        """Install Munch to ~/.bin/"""
        print "Installing Munch..."
        try:
            subprocess.call(['chmod', '+x', self.src])
            shutil.copy2(self.src, self.dst + self.name)
            #os.renames(self.src, self.dst + self.name)
            print 'Munch installed successfully.'
            return True
        except:
            self.problem.append('Problem installing Munch.')
            return False


class Munch:
    def __init__(self, branch = 'master', name = False):
        self.branch = branch
        self.url = 'https://github.com/bigspring/lunchbox/archive/{0}.zip'.format(branch)
        self.lunchbox_zip = 'lunchbox.zip'
        self.composer_filename = 'composer.json'
        self.composer_data = False
        self.project_name = name
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
        self.cleanup()

    def fetch_lunchbox(self):
        """Download the Lunchbox repo as a zip file"""
        urllib.urlretrieve(self.url, self.lunchbox_zip)

    def open_lunchbox(self):
        """Prepare Lunchbox files"""
        zf = zipfile.ZipFile(self.lunchbox_zip, 'r')
        self.composer_data = zf.read('lunchbox-{0}/'.format(self.branch) + self.composer_filename)
        if self.project_name == False:
            self.project_name = raw_input('Enter the project name: ')
            while os.path.isdir(os.getcwd() + '/' + self.project_name):
                print "A directory with that name already exists."
                project_name = raw_input('Enter the project name: ')
        self.composer_data = self.composer_data.replace('LUNCHBOX_DIR', self.project_name)
        file = open(self.composer_filename, 'w')
        file.write(self.composer_data)
        file.close()

    def munch_lunch(self):
        """Run composer install"""
        subprocess.call(['composer', 'install'])

    def cleanup(self):
        """Cleanup unrequired files"""
        for file in [self.composer_filename, 'composer.lock', self.lunchbox_zip]:
            os.remove(os.getcwd() + '/' + file)
        shutil.rmtree('vendor')

def correct_usage():
    """Print usage information"""
    print "usage: munch [-h], [-n projectname] [-b]"
    print "\t-h --help\tPrint correct usage and options"
    print "\t-n --name\tProvide project name"
    print "\t-b --branch\tBranch to pull from"

def install(src, dst):
    """Run installer"""
    install = Installer(src, dst)
    if len(install.errors) > 0:
        for error in install.errors:
            print error
        sys.exit(2)

if __name__ == '__main__':

    print __file__
    sys.exit(2)
    bin_path = os.getenv('HOME') + '/.bin/munch'
    src = os.path.realpath(__file__) # current filepath
    dst = os.getenv('HOME') + '/.bin/' # bin directory
    branch = 'master'
    project_name = False
    installed = False

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hn:b:', ['help', 'name=', 'branch='])
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

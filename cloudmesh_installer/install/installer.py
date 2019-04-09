"""Usage:
  cloudmesh-installer git [clone|pull|status] [BUNDLE]
  cloudmesh-installer install [BUNDLE] [-e]
  cloudmesh-installer local purge [DIR] [-f]
  cloudmesh-installer list
  cloudmesh-installer info


A convenient program called `cloudmesh-installer` to ownload and install cloudmesh
from sources published in github.

Arguments:
  BUNDLE      the bundle [default: cms]
  REPOS       list of git repos

Options:
  -h --help
  -f       executes the purge

Description:


    cloudmesh-installer list

        Bundles

        Cloudmesh has a number of bundels. Bundels are simple a number of git
        repositories. You can list the bundels with the list command. and see
        their names in the top level.

    cloudmesh-installer git [clone|pull|status] [BUNDLE]

        This command executes the given git command on the bundle

    cloudmesh-installer install [BUNDLE]

        This command executes an install on the given bundle

    cloudmesh-installer info

        This command is very useful to list the version of the installed
        package, the version n git, and the version on pypi

    cloudmesh-installer local purge [DIR] [-f]

        This command should not be used in general. It is for the most
        experienced user and allows to identify eggs in your directory
        recursively. The -f option allows to delete the egg, but it may be a
        better strategy to just list the egs without th -f and than delete the
        files you do not want.

    Example:

        let us assume you like to work on storage, than you need to do the following

            cloudmesh-install git clone storage
            cloudmesh-installer install storage -e
            cloudmesh-installer info

"""
from docopt import docopt
import subprocess
import sys
from pprint import pprint
import oyaml as yaml
import requests
import re
import os
from pathlib import Path
import shutil

repos = dict({

    'cms': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
    ],

    'cloud': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
        'cloudmesh-cloud'
    ],

    'storage': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
        'cloudmesh-cloud',
        'cloudmesh-storage'
    ],

    'source': [
        'cloudmesh-common',
        'cloudmesh-cmd5',
        'cloudmesh-sys',
        'cloudmesh-inventory',
        'cloudmesh-cloud',
        'cloudmesh-storage',
        'cloudmesh-emr',
        'cloudmesh-comet',
        'cloudmesh-openapi',
        'cloudmesh-nn',
        'cloudmesh-nist',
        'cloudmesh-conda',
    ],

    'web': [
        'about',
        'get',
        'cloudmesh-github.io',
    ],

    'community': [
        'cloudmesh-community.github.io'
    ],

    'spring19': [
         'fa18-516-22',
         'fa18-516-26',
         'fa18-516-29',
         'hid-sample',
         'hid-sp18-407',
         'hid-sp18-512',
         'hid-sp18-519',
         'hid-sp18-520',
         'hid-sp18-522',
         'hid-sp18-523',
         'hid-sp18-602',
         'hid-sp18-701',
         'hid-sp18-704',
         'hid-sp18-709',
         'hid-sp18-710',
         'sp19-222-100',
         'sp19-222-101',
         'sp19-222-102',
         'sp19-222-89',
         'sp19-222-90',
         'sp19-222-91',
         'sp19-222-92',
         'sp19-222-93',
         'sp19-222-94',
         'sp19-222-96',
         'sp19-222-97',
         'sp19-222-98',
         'sp19-222-99',
         'sp19-516-121',
         'sp19-516-122',
         'sp19-516-123',
         'sp19-516-124',
         'sp19-516-125',
         'sp19-516-126',
         'sp19-516-127',
         'sp19-516-128',
         'sp19-516-129',
         'sp19-516-130',
         'sp19-516-131',
         'sp19-516-132',
         'sp19-516-133',
         'sp19-516-134',
         'sp19-516-135',
         'sp19-516-136',
         'sp19-516-137',
         'sp19-516-138',
         'sp19-516-139',
         'sp19-616-111',
         'sp19-616-112'
    ]
})


# git clone git@github.com:cloudmesh-community/$f.git


#git clone https://github.com/cloudmesh/get.git

def run(command):
    try:
        output = subprocess.check_output(command,
            shell=True,
            stderr=subprocess.STDOUT,
        )
    except subprocess.CalledProcessError as err:
        print('ERROR:', err)
        sys.exit(1)

    return output.decode('utf-8')


class Git(object):

    @staticmethod
    def url(repo):
        if repo in repos['community']:
            return f"https://github.com/cloudmesh-community/{repo}"
        else:
            return f"https://github.com/cloudmesh/{repo}"

    @staticmethod
    def clone(repos):
        for repo in repos:
            print(f"clone -> {repo}")
            if not os.path.isdir(repo):
                try:
                    location = Git.url(repo)
                    r = run(f"git clone {location}.git")
                    print (f"         {r}")
                except Exception as e:
                    print (e)
            else:
                print ("         ERROR: not downlaoded as repo already exists.")

    @staticmethod
    def status(repos):
        for repo in repos:
            print ("status ->", repo)
            os.chdir(repo)
            print (run("git status"))
            os.chdir("../")

    # git clone https://github.com/cloudmesh/get.git

    @staticmethod
    def pull(repos):
        for repo in repos:
            print ("pull ->", repo)
            os.chdir(repo)
            print (run("git pull"))
            os.chdir("../")

    @staticmethod
    def install(repos, dev=False):
        for repo in repos:
            print ("install ->", repo)
            if dev:
                os.chdir(repo)
                print (run("pip install -e ."))
                os.chdir("../")
            else:
                print (run("pip install {repo}".format(repo=repo)))


#git clone https://github.com/cloudmesh/get.git

def yn_question(msg):
    while True:
        query = input(msg)
        answer = query.lower().strip()
        if query == '' or not answer in ['yes', 'n']:
            print('Please answer with yes/n!')
        else:
            break
    return answer == 'yes'


def banner(txt):
    """prints a banner of the form with a frame of # around the txt::

      ############################
      # txt
      ############################

    :param txt: a text message to be printed
    :type txt: string
    """
    print("#" * 70)
    print("#", txt)
    print("#" * 70)

def remove(location):
    print ("delete", location)
    try:
        shutil.rmtree(location)
    except Exception as e:
        print(e)


def main():
    arguments = docopt(__doc__)
    bundle = arguments["BUNDLE"] = arguments.get("BUNDLE") or 'cms'
    arguments["DIR"] = \
        os.path.expandvars(os.path.expanduser(arguments.get("DIR") or '.'))

    if arguments["purge"] and arguments["local"]:
        dryrun = not arguments['-f']

        eggs = list(Path(arguments["DIR"]).glob("**/cloudmesh*egg*"))

        if dryrun:
            banner("Dryrun purge")
            for egg in eggs:
                print(f" found -> {egg}")
        else:
            banner("WARNING dryrun: once you say yess a delete can not be undone")

            if not yn_question(f"WARNING: Do you realy want to continue. This is DANGEROUS (yes/n)? "):
                sys.exit(1)

            for egg in eggs:
                print ()
                if yn_question(f"WARNING: Do you want to delete the egg '{egg}' (yes/n)? "):
                    remove(egg)

    elif arguments["list"]:
        print("list")
        lines = yaml.dump(repos, default_flow_style=False).split("\n")
        for line in lines:
            if ":" in line:
                print()
            print(line)

    elif arguments["info"]:
        #print("info")
        #packages = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]
        packages = repos[bundle]
        for package in packages:
            print ("\nVersion -> {package}".format(
                package=package))
            try:
                installed = run("pip freeze | grep {package}".format(
                package=package)).strip()
            except:
                installed = "!CANNOT FIND INSTALLED VERSION"
            print("...Installed Version ->", installed)
            try:
                v = requests.get("https://raw.githubusercontent.com/cloudmesh"
                             "/{package}/master/VERSION".format(
                                package=package)).text
            except:
                v = "!CANNOT FIND GIT VERSION INFO"
            finally:
                if '404' in v:
                    v = "!CANNOT FIND GIT VERSION INFO"
            print("...Github Version ->", v)
            try:
                v = requests.get("https://pypi.org/project/{package}/".format(
                package=package)).text
                pat_str = '(.*)<h1 class="package-header__name">(.+?)</h1>(.*)'
                pattern = re.compile(pat_str, re.M | re.I | re.S)
                groups = re.match(pattern, v)
            #print (groups)
                v = (groups.group(2)).strip().split(package)[1].strip()
            except:
                v = "!CANNOT FIND PYPI VERSION INFO"
            print("...Pypi Version ->", v)

    elif arguments["git"]:

        if arguments["status"]:
            #repos = ["cloudmesh-common", "cloudmesh-cmd5", "cloudmesh-cloud"]
            Git.status(repos[bundle])

        elif arguments["clone"]:
            result = Git.clone(repos[bundle])

        elif arguments["pull"]:
            Git.pull(repos[bundle])

    elif arguments["install"]:
        if arguments["-e"]:
            result = Git.install(repos[bundle], dev=True)
        else:
            result = Git.install(repos[bundle])

if __name__ == '__main__':
    main()
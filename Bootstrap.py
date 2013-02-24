#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright 2012 Maximilian Fellner
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Downloads and extracts the Twitter bootstrap library into a new
directory on the filesystem and creates a basic HTML file."""

import os, sys, shutil, urllib2, zipfile, argparse

BOOTSTRAP_URL='http://twitter.github.com/bootstrap/assets/bootstrap.zip'
TEMPLATE_SRC='<!doctype html>\n\
<html lang="en">\n\
<head>\n\
  <meta charset="utf-8">\n\
  <title>My Bootstrap Project</title>\n\
  <meta name="viewport" content="width=device-width, initial-scale=1.0">\n\
  <meta name="description" content="">\n\
  <meta name="author" content="">\n\
  <link href="bootstrap/css/bootstrap.min.css" rel="stylesheet">\n\
  <!--[if lt IE 9]>\n\
  <script src="http://html5shiv.googlecode.com/svn/trunk/html5.js"></script>\n\
  <![endif]-->\n\
</head>\n\
  <body>\n\
    <h1>Hello, world!</h1>\n\
    <script src="bootstrap/js/bootstrap.min.js"></script>\
  </body>\n\
</html>'

def is_internet_connected():
    try:
        response = urllib2.urlopen('http://74.125.232.200', timeout=1)
        return True
    except urllib2.URLError as err: pass
    return False

def create_template_files(targetDir):
    if not targetDir.endswith(os.sep):
      targetDir += os.sep
    with open(targetDir + 'index.html', 'w') as indexFile:
        indexFile.write(TEMPLATE_SRC)

def download_bootstrap(targetDir):
    print('> Downloading bootstrap.zip…')
    targetFile = targetDir + 'bootstrap.zip';
    response = urllib2.urlopen(BOOTSTRAP_URL)
    with open(targetFile, 'w') as zipFile:
        zipFile.write(response.read())
    with zipfile.ZipFile(targetFile, "r") as zipFile:
        zipFile.extractall(targetDir)
    os.remove(targetFile)

def create_project_dir(dirname):
    if os.path.exists(dirname):
        overwrite = ''
        while overwrite != 'y' and overwrite != 'n':
            overwrite = raw_input("> Overwrite existing directory? [y/n] ").lower()
        if overwrite == 'y':
            if os.path.realpath(dirname).startswith(os.path.expanduser('~')):
                shutil.rmtree(dirname)
                print('> Deleted existing directory "%s"' % dirname)
            else:
                print('> Can only delete user-directories. Bootstrap aborted.')
                sys.exit(0)
        else:
            print('> Bootstrap aborted.')
            sys.exit(0)
    os.mkdir(dirname)
    print('> Created new directory "%s"' % dirname)

def init_new_project(dirname):
    create_project_dir(dirname)
    download_bootstrap(dirname)
    create_template_files(dirname)
    print('> Bootstrap complete!')

def main():
    if not is_internet_connected():
        print('> No internet connection. Bootstrap aborted.')
        sys.exit(0)

    arg_parser = argparse.ArgumentParser(description='Bootstrap: a setup script for Twitter bootstrap.')

    arg_parser.add_argument('-d', '--directory', action='store', type=str, dest='dirname',
    help='Directory to initialize new project in.', required=True)

    args = arg_parser.parse_args()
    init_new_project(args.dirname)

if __name__=='__main__':
    try:
        main ()
    except KeyboardInterrupt:
        pass

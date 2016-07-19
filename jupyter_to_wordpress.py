import sys
import os
from os import path as op
import shutil as sh
from glob import glob
import time

file_path = sys.argv[1]

root = op.dirname(file_path)
if root == '':
    root = '.'
title = op.basename(file_path).split('.ipynb')[0]
# Check to see if the html folder exists
if not op.exists('{}/html/'.format(root)):
    os.mkdir('{}/html/'.format(root))

# Remove pre-existing versions of this post if it's there
existing = glob('{}/html/*{}*.html'.format(root, title))
if len(existing) > 1:
    raise ValueError('There should be at most 1 file with this title')
elif len(existing) == 1:
    # Keep the date info for the post
    existing = existing[0]
    print('Updating old file:\n{}'.format(existing))
    date_info = op.basename(existing).split('-')[:3]
    year, mo, day = [int(ii) for ii in date_info]
    os.remove(existing)
else:
    print('Creating new file...')
    # Create new date info for the post
    now = time.localtime()
    mo = now.tm_mon
    day = now.tm_mday
    year = now.tm_year

# Now convert to html and move to the `html` folder
cmd_convert = 'jupyter nbconvert --to html --template basic {}'.format(file_path)
print("Running command:\n{}".format(cmd_convert))
os.system(cmd_convert)
new_folder = '{}/html/'.format(root)
new_file = '{}.html'.format(title)
html_file = '{}-{}-{}-{}.html'.format(year, mo, day, title)
sh.move('{}/{}'.format(root, new_file), '{}{}'.format(new_folder, html_file))
print('New file is at:\n{}'.format(op.abspath(new_folder + html_file)))

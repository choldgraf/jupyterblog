import sys
import os
from os import path as op
import shutil as sh
from glob import glob
import time
import nbformat as nb
import argparse
from glob import glob
from tqdm import tqdm

parser = argparse.ArgumentParser(
    description='Process a jupyter notebook for blogs.')
parser.add_argument('file_path', metavar='F', type=str, nargs='+',
                    help='The path to the notebook file to be converted')
parser.add_argument('--inplace', dest='inplace', action='store_const',
                    const=True, default=False,
                    help='Whether to simply modify the notebook in place')

args = parser.parse_args()
inplace = args.inplace

files = args.file_path
print('Found {} files'.format(len(files)))

if inplace is True:
    print('Overwriting notebook file')
else:
    print('Creating new HTML')


for file_path in tqdm(files):
    file_path = op.abspath(file_path).replace(' ', '\ ')

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
        date_info = op.basename(existing).split('-')[:3]
        year, mo, day = [int(ii) for ii in date_info]
        os.remove(existing)
    else:
        # Create new date info for the post
        now = time.localtime()
        mo = now.tm_mon
        day = now.tm_mday
        year = now.tm_year

    # Clean up the notebook
    file_path_tmp = file_path + '_TMP'
    ntbk = nb.read(file_path, nb.NO_CONVERT)
    new_cells = []
    for ii, cell in enumerate(ntbk.cells):
        # Don't modify non-code cells and just add
        if cell['cell_type'] != 'code':
            new_cells.append(cell)
            continue

        # Skip the cell if it's empty
        if len(cell['source']) == 0:
            continue

        # Clean outputs otherwise
        outputs = []
        for output in cell['outputs']:
            # Remove stderrors in the outputs
            if 'name' in list(output.keys()):
                if output['name'] != 'sterr':
                    continue
            # Check if we have any object outputs (e.g. a function returned)
            if 'data' in list(output.keys()):
                if 'text/plain' in output['data'].keys():
                    if output['data']['text/plain'].startswith('<'):
                        _ = output['data'].pop('text/plain')
            outputs.append(output)
        cell['outputs'] = outputs
        cell['execution_count'] = None
        new_cells.append(cell)

    # Update the notebook w/ new cells and write it
    ntbk['cells'] = new_cells

    # Continue with the conversion or just overwrite in place
    if inplace is True:
        nb.write(ntbk, file_path, nb.NO_CONVERT)
        continue
    nb.write(ntbk, file_path_tmp, nb.NO_CONVERT)

    # Now convert to html and move to the `html` folder
    curdir = os.path.abspath(os.curdir)
    newdir = os.path.dirname(__file__)
    cmd_convert = 'jupyter nbconvert --to html --template basic {}'.format(file_path_tmp)
    print("Running command:\n{}".format(cmd_convert))
    os.chdir(newdir)
    os.system(cmd_convert)
    os.chdir(curdir)

    # Now move the HTML to a new folder and delete the temp file
    new_folder = '{}/html/'.format(root)
    new_file = '{}.html'.format(title)
    html_file = '{}-{}-{}-{}.html'.format(year, mo, day, title)
    sh.move('{}/{}'.format(root, new_file), '{}{}'.format(new_folder, html_file))
    os.remove(file_path_tmp)
    print('New file is at:\n{}'.format(op.abspath(new_folder + html_file)))
print('Finished!')

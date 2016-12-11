from glob import glob
import os
import os.path as op
import shutil as sh
import argparse
import nbformat as nb

parser = argparse.ArgumentParser(
    description=('Check whether jupyter notebooks have an Interactive property'
                 ' and copy them to an interactive output folder if so.'))
parser.add_argument('file_path', metavar='F', type=str, nargs='+',
                    help='The path to the notebook files to be checked')
parser.add_argument('output_path', metavar='F', type=str, nargs='+',
                    help='The path to the notebook files to be checked')
parser.add_argument('old_rel_path', metavar='F', type=str, nargs='+',
                    help='The relative path to replace')
parser.add_argument('new_rel_path', metavar='F', type=str, nargs='+',
                    help='Replace all instances of the old path with this one')


args = parser.parse_args()

files_input = args.file_path
path_output = args.output_path[0]
old_rel_path = args.old_rel_path[0]
new_rel_path = args.new_rel_path[0]

print('Replacing {} with {}'.format(old_rel_path, new_rel_path))


n_copied = 0
for file in files_input:
    if not op.exists(file + '-meta'):
        continue
    with open(file + '-meta', 'r') as ff:
        interactive = False
        for ln in ff.readlines():
            if ln.startswith('Interactive'):
                interactive = ln.split(': ')[-1]
    if interactive == 'True':
        file_name = op.basename(file)
        ntbk = nb.read(file, nb.NO_CONVERT)
        for cell in ntbk['cells']:
            cell['source'] = cell['source'].replace(old_rel_path, new_rel_path)
        nb.write(ntbk, os.sep.join([path_output, file_name]))
        n_copied += 1


print('Finished. Copied {} notebooks to {}'.format(n_copied, path_output))

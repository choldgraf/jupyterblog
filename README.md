# jupyterblog
A helper repository for converting Jupyter notebooks into a blog-friendly format. It consists of a few scripts that can be called from the shell.

# Scripts
**`jupyter_to_blog.py`**
Takes as input a path to a jupyter notebook. It will then strip the notebook of cell count numbers, warnings, and some other outputs that look ugly in a blog. Finally, it either converts the notebook to html format (if no `--inplace` flag is given) or modifies the notebook in place (if `--inplace` is given, in which case the notebook will simply be cleaned up).

**`create_interactive_notebooks.py`**
This is for moving a notebook to a new folder that's meant for "interactive" notebooks hosted with mybinder. It take a path to a jupyter notebook and a path to an output "interactive" folder, as well as paths for changing any relative links that are in the notebook (e.g. to images). It will copy the notebook and replace relative links.

# How to use it
* Copy/paste the code in `notebooks.css` into your website's CSS code.
* Run `jupyter_to_blog.py /path/to/notebook.ipynb`.
* Go into the created `html` folder and find the post that was created.
* Copy/paste this html into wordpress' html editor
* Preview the post. The formatting should be taken care of by the CSS you pasted.
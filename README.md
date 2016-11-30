# jupyter_to_wordpress
A helper repository for converting Jupyter notebooks into a wordpress-friendly format.

This currently consists of a single file, `jupyter_to_wordpress.py` that can be called from the shell. It takes as input a path to a jupyter notebook. It will then strip the notebook of cell count numbers, warnings, and some other outputs that look ugly in a blog. Finally, it converts the notebook to html format.

# How to use it
* Copy/paste the code in `notebooks.css` into your website's CSS code.
* Run `jupyter_to_wordpress.py /path/to/notebook.ipynb`.
* Go into the created `html` folder and find the post that was created.
* Copy/paste this html into wordpress' html editor
* Preview the post. The formatting should be taken care of by the CSS you pasted.
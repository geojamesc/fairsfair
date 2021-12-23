g# fairsfair

Python notebooks created by DCC to show a PID graph connecting Data Management Plans to the outputs coming out of research projects.

The 2 source notebooks we are taking as starting points are available from here:

https://github.com/datacite/pidgraph-notebooks-python


specifically (which we have cloned into this repo under):

notebooks/original/pidgraph-notebooks-python/user-story-10-grant-outputs/py-grant-outputs.ipynb
notebooks/original/pidgraph-notebooks-python/dmp/user-story-single-dmp-connections.ipynb

and then taken copies of these as:

/home/james/PycharmProjects/fairsfair/notebooks/py-grant-outputs.ipynb
/home/james/PycharmProjects/fairsfair/notebooks/user-story-single-dmp-connections.ipynb

created a new (3.6) pyenv (dcc36env)

pidgraph-notebooks have listed as a requirement chord==0.0.11

however this version of chord no longer seems to work and upgrading results in nags prompting one to use non-free version
so for now do not install the library by commenting out chord in the requirements.txt

notebooks/original/pidgraph-notebooks-python/requirements.txt

jupyter is not included in requirements.txt so need to pip install it as well
also install bokeh and holoviews as alternative to chord (so we can look at refactoring construction of chord diagram in py-grant-outputs.ipynb using bokeh/holoviews rather than chord)

https://holoviews.org/reference/elements/bokeh/Chord.html

# install new/missing libraries

* need jupyter

pip install jupyter

* /home/james/PycharmProjects/fairsfair/notebooks/user-story-single-dmp-connections.ipynb

needs the following additional libraries:

altair_saver 
altair_viewer
vega 

pip install altair_saver
pip install altair_viewer
pip install vega

* /home/james/PycharmProjects/fairsfair/notebooks/py-grant-outputs.ipynb

needs the following additional libraries:

chord==0.0.17

but chord is problematic so we will additonally use/install bokeh/holoviews as an alternative to chord

pip install bokeh
pip install holoviews


* recreate requirements.txt
pip freeze > requirements.txt

---



















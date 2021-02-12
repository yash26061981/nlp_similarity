from setuptools import setup, find_packages
import pathlib, os

root = pathlib.Path(__file__).parent
os.chdir(str(root))

name = 'nlpsim'
version = '1.0'

setup(name=name,
      version=version,
      description='NLP Based Similarity',
      long_description='',
      author='HiVOCO',
      author_email='n/a',
      url='',
      package_dir={'': 'nlpsim'},
      packages=find_packages(where='nlpsim'),
      python_requires='>=3.6, <4',
      install_requires=['nltk','flask','inflect','word2number','sklearn','pronouncing',
                        'Phyme','Spacy','pyinflect','python-Levenshtein','fuzzywuzzy'],
      )

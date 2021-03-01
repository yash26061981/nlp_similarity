from setuptools import setup, find_packages
import pathlib, os

root = pathlib.Path(__file__).parent
os.chdir(str(root))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

name = 'nlpsim'
version = '2.0'

setup(name=name,
      version=version,
      description='NLP Based Similarity',
      long_description=long_description,
      long_description_content_type="text/markdown",
      author='HiVOCO',
      author_email='n/a',
      url="https://github.com/yash26061981/nlp_similarity",
      project_urls={
            "Bug Tracker": "https://github.com/yash26061981/nlp_similarity/issues",
      },
      package_dir={'': 'nlpsim'},
      classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: MIT License",
              "Operating System :: OS Independent",
          ],
      packages=find_packages(where='nlpsim'),
      python_requires='>=3.6, <4',
      install_requires=['nltk','flask','inflect','word2number','sklearn','pronouncing',
                        'Phyme','Spacy','pyinflect','python-Levenshtein','fuzzywuzzy'],
      )

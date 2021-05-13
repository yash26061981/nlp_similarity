from setuptools import setup, find_packages
import pathlib, os
from nlpsim._version import __version__
print(__version__)
#import subprocess
#subprocess.call(['sh', './test.sh', ])

root = pathlib.Path(__file__).parent
os.chdir(str(root))

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

version = __version__

setup(
    name='nlpsim',
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
    zip_safe=True,
    packages=find_packages(where='nlpsim'),
    include_package_data=True,
    python_requires='>=3.6, <4',
    install_requires=['incremental', 'nltk','flask','inflect','word2number','sklearn','pronouncing',
                      'Phyme','Spacy','pyinflect','python-Levenshtein','fuzzywuzzy'],
)

# CS 5293 Text Analytics Project 1


## Usage

pipenv run python project1/main.py --input [GOLB or FILES] [REDACTION_FLAGS] --output dir [--stats]``

Current output of pipenv run python project1/main.py -h:


usage: main.py [-h] [--input INPUT [INPUT ...]] [--names] [--genders]
               [--dates] [--addresses] [--phones] [--concept CONCEPT]
               [--output OUTPUT] [--stats STATS]

optional arguments:
  -h, --help            show this help message and exit
  --input INPUT [INPUT ...]
                        Any number of input files. Supports GLOB formatting.
  --names               Use to redact names.
  --genders             Use to redact gendered words.
  --dates               Use to redact dates.
  --addresses           Use to redact addresse.
  --phones              Use to redact phones.
  --concept CONCEPT     Redacts sentences containing words related to the
                        given string.
  --output OUTPUT       The ouput directory for the .redacted files.
  --stats STATS         The output file for the stat information. If not
                        provided it will print to stdout.**


#tests

Tests can be run with ``pipenv run python -m pytest``.

Currently there are fives tests the run tests on each different redaction flag.

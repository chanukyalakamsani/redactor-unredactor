import argparse
import os
import sys

import pytest

import project1
from project1 import main
import nltk
from nltk.tokenize import WordPunctTokenizer


def test_concept():
    filename = "concept.txt"
    concept_file = 'tests/test_files/' + filename
    output_dir = 'tests/test_files/redacted/'

    main.init_stats(concept_file, 0, None)

    # Get test file
    content = main.get_file_contents(concept_file)

    # Used to split the file for POS analysis
    word_punct_tokenizer = WordPunctTokenizer()
    tagged_content = nltk.pos_tag(word_punct_tokenizer.tokenize(content))

    # Make required dot structure. 
    # See https://stackoverflow.com/questions/2352181/how-to-use-a-dot-to-access-members-of-dictionary
    arg = {"concept":["child"]}
    args = temp(arg)

    # Redacte
    content = main.redact_concept(content, concept_file, args)

    # X concept words in file
    assert(main.num_concept[concept_file] == 12)

    # Create path
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)

    # Write out the redacted test file for reference
    main.write_redacted(content, concept_file, output_dir)


class temp(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

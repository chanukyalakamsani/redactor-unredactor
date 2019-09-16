import argparse
import os
import sys

import pytest

import project1
from project1 import main
import nltk
from nltk.tokenize import WordPunctTokenizer


def test_name():
    filename = "name.txt"
    name_file = 'tests/test_files/' + filename
    output_dir = 'tests/test_files/redacted/'

    main.init_stats(name_file, 0, None)

    # Get test file
    content = main.get_file_contents(name_file)

    # Used to split the file for POS analysis
    word_punct_tokenizer = WordPunctTokenizer()
    tagged_content = nltk.pos_tag(word_punct_tokenizer.tokenize(content))

    # Redacte
    content = main.redact_names(content, tagged_content, name_file)

    # X nameed words in file
    assert(main.num_names[name_file] == 22)

    # Create path
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)

    # Write out the redacted test file for reference
    main.write_redacted(content, name_file, output_dir)

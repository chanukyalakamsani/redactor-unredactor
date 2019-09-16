import argparse
import os
import sys

import pytest

import project1
from project1 import main
import nltk
from nltk.tokenize import WordPunctTokenizer


def test_gender():
    filename = "gender.txt"
    gender_file = 'tests/test_files/' + filename
    output_dir = 'tests/test_files/redacted/'

    main.init_stats(gender_file, 0, None)

    # Get test file
    content = main.get_file_contents(gender_file)

    # Used to split the file for POS analysis
    word_punct_tokenizer = WordPunctTokenizer()
    tagged_content = nltk.pos_tag(word_punct_tokenizer.tokenize(content))

    # Redacte
    content = main.redact_gendered_words(content, tagged_content, gender_file)

    # X gendered words in file
    assert(main.num_gendered_words[gender_file] == 13)

    # Create path
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)

    # Write out the redacted test file for reference
    main.write_redacted(content, gender_file, output_dir)

import argparse
import os
import sys

import pytest

import project1
from project1 import main


def test_phone():
    filename = "phones.txt"
    phone_file = 'tests/test_files/' + filename
    output_dir = 'tests/test_files/redacted/'

    main.init_stats(phone_file, 0, None)

    # Get test file
    content = main.get_file_contents(phone_file)

    # Redacte
    content = main.redact_phones(content, phone_file)

    # Three phones numbers in file
    assert(main.num_phones[phone_file] == 4)

    # Create path
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)

    # Write out the redacted test file for reference
    main.write_redacted(content, phone_file, output_dir)

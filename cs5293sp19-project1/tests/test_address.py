import argparse
import os
import sys

import pytest

import project1
from project1 import main


def test_address():
    filename = "addresses.txt"
    address_file = 'tests/test_files/' + filename
    output_dir = 'tests/test_files/redacted/'

    main.init_stats(address_file, 0, None)

    # Get test file
    content = main.get_file_contents(address_file)

    # Redacte
    content = main.redact_addresses(content, address_file)

    # Three addressses in file
    assert(main.num_addresses[address_file] == 3)

    # Create path
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)

    # Write out the redacted test file for reference
    main.write_redacted(content, address_file, output_dir)

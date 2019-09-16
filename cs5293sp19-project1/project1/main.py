"""
Example call: pipenv run python project1/main.py --input docs/input.txt docs/input2.txt --names --addresses --phones --dates --concept pig --output redacted
"""

import argparse
import datetime
import glob
import os
import re
import sys
from pprint import pprint

import nltk
from nltk.corpus import wordnet as wn
from nltk.tokenize import WordPunctTokenizer

num_names = dict()
num_phones = dict()
num_dates = dict()
num_gendered_words = dict()
num_addresses = dict()
num_concept = dict()


def main(args):
    # Get the list of files exanded by glob. Removed files that still contain a * expansion.
    input_files = list(file_path for value in args.input for pattern in value for file_path in glob.glob(
        pattern, recursive=True))

    # Pull out output dir for a better name
    output_dir = args.output

    # Verbose printing
    pprint("Input files: " + str(input_files))
    pprint("Output directory: " + args.output)
    pprint("Stats file: " + str(args.stats if args.stats else "sys.stdout"))

    # Check if the input / output files exist
    check_file_paths(input_files, output_dir)
    file_number = 0

    # Redact and store all input files
    for filename in input_files:
        # Initialize trackers for stats
        init_stats(filename, file_number, args)

        # Pull out content of the file
        content = get_file_contents(filename)

        # Used to split the file for POS analysis
        word_punct_tokenizer = WordPunctTokenizer()
        tagged_content = nltk.pos_tag(word_punct_tokenizer.tokenize(content))

        # Redact the file
        content = redact_content(content, tagged_content, filename, args)

        # Store the results out to the redacted file.
        write_redacted(content, filename, output_dir)

        # Track with file we are on
        file_number = file_number + 1


def check_file_paths(input_files, output_dir):

    # Check if files do not exist
    for name in input_files:
        if not os.path.isfile(name):
            sys.stderr.write("Error: File not found: " + name + "\n")

    # Create output dir if it does exist
    if(not os.path.isdir(output_dir)):
        sys.stderr.write(
            "Output directory did not exist...creating " + output_dir + "/\n")
        os.makedirs(output_dir)


def init_stats(filename, file_number, args):

    # Initialize dicts for this file
    num_names[filename] = 0
    num_phones[filename] = 0
    num_dates[filename] = 0
    num_gendered_words[filename] = 0
    num_addresses[filename] = 0
    num_concept[filename] = 0

    # Override current file and print header
    if(file_number == 0):
        if(args and args.stats):
            with open(args.stats, "w") as stats_file:
                stats_file.write(
                    "+---------------------------------------------+\n")
                stats_file.write("| Redaction ran at " +
                                 str(datetime.datetime.today()) + " |\n")
                stats_file.write(
                    "+---------------------------------------------+\n\n")
        else:
            sys.stdout.write(
                "+---------------------------------------------+\n")
            sys.stdout.write("| Redaction ran at " +
                             str(datetime.datetime.today()) + " |\n")
            sys.stdout.write(
                "+---------------------------------------------+\n\n")


def get_file_contents(filename):
    content = ""
    # Does file exist?
    if(os.path.isfile(filename)):
        # Open and read file
        with open(filename, "r", encoding="utf8") as input_file:
            content = input_file.read()
    return content


def redact_content(content, tagged_content, filename, args):

    # Redacte phone numbers (if specified)
    if(args and args.phones):
        content = redact_phones(content, filename)
    # Redacte dates (if specified)
    if(args and args.dates):
        content = redact_dates(content, filename)
    # Redacte addresses (if specified)
    if(args and args.addresses):
        content = redact_addresses(content, filename)
    # Redacte names (if specified)
    if(args and args.names):
        content = redact_names(content, tagged_content, filename)
    # Redacte gendered words (if specified)
    if(args and args.genders):
        content = redact_gendered_words(content, tagged_content, filename)
    # Redacte provided concept (if specified)
    if(args and args.concept):
        content = redact_concept(content, filename, args)

    # Write stats out
    output_stats(filename, args)

    # Return the redacted string
    return content


def redact_phones(content, filename):
    # Regex for finding the strings to replace
    phone_regex = r"(\(?\d{3}\)??.?\d{3}.?\d{4})"
    matches = re.findall(phone_regex, content)

    # Replace the matches with the unicode block
    for match in matches:
        repl = re.sub(r"[^()-/.,]", u"\u2588", match, 0)
        content = content.replace(match, repl, 1)
        num_phones[filename] = num_phones[filename] + 1

    return content


def redact_dates(content, filename):

    # Common date string regex
    date_regex = r"(\d{1,2}[-/.]\d{1,2}[-/.]\d{1,}|\d{1,}[-/.]\d{1,2}[-/.]\d{1,2})"
    matches = re.findall(date_regex, content)

    # Find and redact matched dates
    for match in matches:
        repl = re.sub(r"[^-/.]", u"\u2588", match, 0)
        content = content.replace(match, repl, 1)
        num_dates[filename] = num_dates[filename] + 1

    return content


def redact_addresses(content, filename):

    # Handmade regex for addresses, this can be improved through alternate third party methods.
    address_regex = r"(\d+(\s[A-Z][A-z]*){2,6})((,(\s?[A-Z][A-z]+)+)(,\s?([A-z]{2}|\w+)\b)(,?\s?\d+(\-\d+)?)?)?"
    matches = re.findall(address_regex, content)

    # Find and redact the matchs
    for match in matches:
        address = match[0]+match[2]
        repl = re.sub(r"[^\s,.\":\-=_+!?]", u"\u2588", address, 0)
        content = content.replace(address, repl, 1)
        num_addresses[filename] = num_addresses[filename] + 1

    return content


def redact_names(content, tagged_content, filename):

    # Create grammer for proper nouns
    grammar = r"NAME: {(<NNP>|<NNP\$>)}"

    # Use NLTK to find and tag these POS
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged_content)

    # Creates a list of the matched words
    words = list()
    for subtree in tree.subtrees():
        if subtree.label() == 'NAME':
            for leaf in subtree.leaves():
                words.append(leaf[0])

    # Redactes the words from the content string
    for word in words:
        regex_str = r'\b(' + re.escape(word) + r')\b'
        content = re.sub(regex_str, u"\u2588" * len(word), content, count=1)
        num_names[filename] = num_names[filename] + 1
    return content


def redact_gendered_words(content, tagged_content, filename):

    # Create grammer for personal nouns
    grammar = r"GENDERED: {(<PRP>|<PRP\$>)}"

    # Use NLTK to find and tag these POS
    cp = nltk.RegexpParser(grammar)
    tree = cp.parse(tagged_content)
    words = list()

    # Creates a list of the matched words
    for subtree in tree.subtrees():
        if subtree.label() == 'GENDERED':
            for leaf in subtree.leaves():
                words.append(leaf[0])

    # Redactes the words from the content string
    for word in words:
        regex_str = r'\b(' + re.escape(word) + r')\b'
        content = re.sub(regex_str, u"\u2588" * len(word), content, count=1)
        num_gendered_words[filename] = num_gendered_words[filename] + 1

    return content


def redact_concept(content, filename, args):

    # For each concept word
    for concept in args.concept:
        # Stores the synonyms
        syn_words = set()

        # Get syns from NLTK
        for synset in wn.synsets(concept):
            for lemma in synset.lemmas():
                syn_words.add(lemma.name())
        # Find and redact sentences containing the matched words
        for syn_word in syn_words:
            # Matches full sentences with the given word
            sent_regex = r"([\s,\"-_+=()]*?\.|^)([\w\s\u2588,\"--_+=()]*?[\s,\"\-_+=()]?" + \
                syn_word+r"[\s,\"\-_+=()]?[\w\s\u2588,\"\-+=()]*?)\."
            res = re.findall(sent_regex, content, flags=re.UNICODE)

            # Replaces the matches
            for match in res:
                sent = match[1]
                if(sent in content):
                    repl = re.sub(r"[^\s,.\":\-=_+!?]", u"\u2588", sent, 0)
                    content = content.replace(sent, repl)
                    num_concept[filename] = num_concept[filename] + 1

    return content


def output_stats(filename, args):


    # Output to file if it exists
    if(args and args.stats):
        with open(args.stats, "a") as stats_file:
            stats_file.write("Redaction information for: " + filename + "\n")
            stats_file.write("\tNumber of names redacted: " +
                             str(num_names[filename]) + "\n")
            stats_file.write("\tNumber of phone numbers redacted: " +
                             str(num_phones[filename]) + "\n")
            stats_file.write("\tNumber of addresses redacted: " +
                             str(num_addresses[filename]) + "\n")
            stats_file.write("\tNumber of dates redacted: " +
                             str(num_dates[filename]) + "\n")
            stats_file.write("\tNumber of gendered words redacted: " +
                             str(num_gendered_words[filename]) + "\n")
            stats_file.write("\tNumber of concept sentences redacted: " +
                             str(num_concept[filename]) + "\n")
            stats_file.write("\n")
    # Output to stdout
    else:
        sys.stdout.write("Redaction information for: " + filename + "\n")
        sys.stdout.write("\tNumber of names redacted: " +
                         str(num_names[filename]) + "\n")
        sys.stdout.write("\tNumber of phone numbers redacted: " +
                         str(num_phones[filename]) + "\n")
        sys.stdout.write("\tNumber of addresses redacted: " +
                         str(num_addresses[filename]) + "\n")
        sys.stdout.write("\tNumber of dates redacted: " +
                         str(num_dates[filename]) + "\n")
        sys.stdout.write("\tNumber of gendered words redacted: " +
                         str(num_gendered_words[filename]) + "\n")
        sys.stdout.write("\tNumber of concept sentences redacted: " +
                         str(num_concept[filename]) + "\n")
        sys.stdout.write("\n")


def write_redacted(content, filename, output_dir):
    # Open and write to the file
    output_path = get_output_file_path(filename, output_dir)
    with open(output_path, 'w', encoding="utf8") as output_file:
        output_file.write(str(content))


def get_output_file_path(input_file, output_dir):
    
    filename = os.path.basename(input_file) + ".redacted"
    output_path = os.path.join(output_dir, filename)
    return output_path


if __name__ == "__main__":
    """
    Used for argparse, forwards to main().
    """
    # Setup arguments for the program
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", nargs='+', type=str, action="append",
                        help="Any number of input files. Supports GLOB formatting.")
    parser.add_argument("--names", action="store_true",
                        help="Use to redact names.")
    parser.add_argument("--genders", action="store_true",
                        help="Use to redact gendered words.")
    parser.add_argument("--dates", action="store_true",
                        help="Use to redact dates.")
    parser.add_argument("--addresses", action="store_true",
                        help="Use to redact addresse.")
    parser.add_argument("--phones", action="store_true",
                        help="Use to redact phones.")
    parser.add_argument("--concept", nargs='+', type=str, action="append",
                        help="Redacts sentences containing words related to the given strings.")
    parser.add_argument("--output", type=str,
                        help="The ouput directory for the .redacted files.")
    parser.add_argument("--stats", type=str,
                        help="The output file for the stat information. If not provided it will print to stdout.")

    # Parse args
    args = parser.parse_args()

    # Redact the files
    main(args)

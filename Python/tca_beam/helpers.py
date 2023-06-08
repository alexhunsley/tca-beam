import os
import re


def dbg(string):
    pass
    # print(string)


def p(string=""):
    print(string)


def error(string):
    print(f"\n ERROR: {string}")


def make_abs_path(rel_path):
    script_dir = os.path.dirname(__file__)
    return os.path.normpath(os.path.join(script_dir, rel_path))


def sanitize_filename(filename):
    return re.sub(r'(?u)[^-\w.{}]', '', filename.strip())

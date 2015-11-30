#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function, absolute_import
import argparse
import logging
from bs4 import BeautifulSoup
import os
import sqlite3

logging.basicConfig(
    level='INFO', format='[%(asctime)s] %(levelname)8s %(message)s')
logger = logging.getLogger(__name__)


def chunks(it, n):
    for i in range(0, len(it), n):
        yield it[i:i+n]


def main(args):
    if args.verbose:
        logger.setLevel('DEBUG')
    logger.debug(args)

    root_path = 'cfitsio.docset/Contents/Resources/Documents'
    index_page = os.path.join(root_path, 'node122.html')
    with open(index_page) as infile:
        contents = infile.read()

    soup = BeautifulSoup(contents, 'html.parser')
    elements = soup.find_all('td')

    db_name = 'cfitsio.docset/Contents/Resources/docSet.dsidx'
    with sqlite3.connect(db_name) as connection:
        cursor = connection.cursor()
        cursor.execute('delete from searchIndex')
        query = 'INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?, ?, ?)'

        for left, right in chunks(elements, 2):
            item_name = left.text
            link = next(right.children)
            url = link.attrs['href']
            params = (item_name, 'Function', url)
            cursor.execute(query, params)





if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true')
    main(parser.parse_args())

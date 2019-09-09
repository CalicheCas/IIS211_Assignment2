#!/usr/bin/env python3

import urllib.request
import tempfile
import csv
import shutil
from datetime import datetime
import logging
from pprint import pprint
import argparse

parser = argparse.ArgumentParser("DataProcessor")
parser.add_argument(
    "url",
    help="processes csv file data. Expects a url as args",
    type=str
)

argss = parser.parse_args()

log_filename = 'errors.log'
err_logger = logging.getLogger('‘assignment2’')
err_logger.setLevel(logging.ERROR)

logging.basicConfig(
    filename=log_filename,
    level=logging.ERROR
)


def downloadData(url):
    """
    Function downloads csv content from a given
    url and returns a reader object with comma delimiter.

    :param str url:
    :return: csv file
    """
    with urllib.request.urlopen(url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            shutil.copyfileobj(response, tmp_file)

            return tmp_file.name


def date_sanitizer(date):

    return datetime.strptime(date, '%m/%d/%Y')


def processData(csv_file):
    """
    Function takes in a csv file,
    iterates over every line and stores the data
    in a dictionary.

    :param csv_file:
        data to process
    :return: dict
        Dictionary mapping person's ID to a tuple (name, birthday)
   """
    data_dict = {}
    reader = csv.reader(open(csv_file), delimiter=',')

    for row_num, row in enumerate(reader, 1):

        try:

            data_dict[int(row[0])] = (row[1], date_sanitizer(row[2]))

        except ValueError:
            err_logger.error('Error processing line # {} for ID # {}', str(row_num), row[0])

    return data_dict


def displayPerson(person_id, data):
    """
    prints on the screen person data when found or no uer found when non-existent.
    :param int person_id:
        ID look up
    :param data:
        Dictionary with person data.
    :return:
        prints message on screen
    """
    try:

        person = data.get(person_id)

        pprint("Person # {} is {} with a birthday of {}"
               .format(str(person_id), person[0], person[1].strftime("%Y-%m-%d")))

    except Exception:

        pprint("No person found with that ID.")


def interface(data):
    while True:

        key = int(input('Insert an ID to lookup: '))

        if key <= 0:
            break
        else:
            displayPerson(key, data)


def main(args):

    csv_data = None
    print(args)

    try:
        csv_data = downloadData(args)

    except urllib.request.HTTPError:
        err_logger.error('Error fetching the contents of the url')

    new_data = processData(csv_data)

    interface(new_data)

    exit()


if __name__ == "__main__":
    main(argss.url)

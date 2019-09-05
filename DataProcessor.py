import urllib.request
import tempfile
import csv
import shutil
from datetime import datetime

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
    for row in reader:
        # Sanitize Date
        try:
            id = row[0]
            name = row[1]
            bday = datesanitizer(row[2])
            data_dict[id] = (name, bday)
        except ValueError:
            print("log error")


def datesanitizer(date):

    return datetime.strptime(date, '%m/%d/%Y')





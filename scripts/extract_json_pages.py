#!/usr/bin/env python3


"""
Extracts the source files for crow and test source files for the svelte app from the
compressed csv file containing all the inspection data.

Usage:

./extract_json_pages /path/to/src/file.csv.gz /path/to/crow/source/directory /path/to/svelte/app/test/data/source/directory

Typically this translates to

./extract_json_pages data/latest_file.csv.gz crow-app/data svelte-app/src


The script will create the following files

svelte-app/src/test_violation_pages.json containing paginated test data (latest inspections)
svelte-app/src/test_violation_history.json containing the full histories of the inspections in the test data.
svelte-app/src/descriptions.json maps a short key to the full descriptions the full data. The key is is "VIOLATION CODE" + an increasing number from 0 to 1


crow-app/data/latest_violations.csv containing paginated test data (latest inspections)
crow-app/data/violation_histories.json containing the full histories of the inspections per location.

We want to save all descriptions (instead of using a 1:1 relationship to VIOLATION CODE) to be as close to the original data as possible.

"""

import gzip
import json
import csv
import bisect
import sys
from datetime import datetime
import os
import itertools

_FIELDS = ["INSPECTION DATE", "DBA", "GRADE", "Latitude", "Longitude", "VIOLATION CODE", "SCORE"]
_INSPECTION_DATE_INDEX = _FIELDS.index("INSPECTION DATE")
_GRADE_INDEX = _FIELDS.index("GRADE")


_DATE_FORMAT = "%m/%d/%Y"
_COMPLETE_FIELDS = _FIELDS + ["VIOLATION DESCRIPTION KEY"]

def parse_date(date_str: str):
    """Parses a Month/Day/Year date string into a timestamp"""
    
    parsed_date = datetime.strptime(date_str, _DATE_FORMAT)
    return int(parsed_date.timestamp())

# In case python 3.12 is not available, we reimplement batched here.
def batched(iterable, n, *, strict=False):
    if n < 1:
        raise ValueError('n must be at least one')
    iterator = iter(iterable)
    while batch := tuple(itertools.islice(iterator, n)):
        if strict and len(batch) != n:
            raise ValueError('batched(): incomplete batch')
        yield batch


def json_pages(source_file: str,  crow_data_dir: str, svelte_data_dir: str, page_size: int, number_of_pages: int):
    histories = {}
    descriptions_to_keys = {}
    keys_to_descriptions = {}
    for row in csv.DictReader(gzip.open(source_file, 'rt')):
        if row["INSPECTION DATE"] == "01/01/1900":
            continue
        # turn date to timestamp seconds
        row["INSPECTION DATE"] = parse_date(row["INSPECTION DATE"])

        try:
            row["Latitude"] = float(row["Latitude"])
            row["Longitude"] = float(row["Longitude"])
        except ValueError:
            continue
        
        violation_description = row["VIOLATION DESCRIPTION"]
        if violation_description in descriptions_to_keys:
             violation_description_key = descriptions_to_keys[violation_description]
        else:
            # Insert a new description
            for description_index_per_code in range(10):
                violation_description_key = f"{row['VIOLATION CODE']}{description_index_per_code}"
                if violation_description_key not in keys_to_descriptions:
                    break
            else:
                raise ValueError(f"Found more than 10 descriptions for a single violation code in row {row} {[keys_to_descriptions[row['VIOLATION CODE'] + str(i)] for i in range(10)]}",)
        row["VIOLATION DESCRIPTION KEY"] = violation_description_key
        keys_to_descriptions[violation_description_key] = violation_description
        descriptions_to_keys[violation_description] = violation_description_key
        inspections_history = histories.setdefault(row["CAMIS"], [])
        inspection = [row[field] for field in _COMPLETE_FIELDS]
        # to revert the list we use -timestamp as key.
        bisect.insort_left(inspections_history, inspection, key=lambda insp: -insp[_INSPECTION_DATE_INDEX])
    
    # list of all latest violations
    violations = []
    for camis, history in histories.items():
        # Grade can be missing, fill with previous data or set N if no such data exists.
        last_grade = 'N'
        for inspection in reversed(history):
            if inspection[_GRADE_INDEX]:
                last_grade = inspection[_GRADE_INDEX]
            else:
                inspection[_GRADE_INDEX] = last_grade
        violations.append([camis] + history[0])

    # Crow data files
    with open(os.path.join(crow_data_dir, 'violation_histories.json'), 'w') as crow_data_violation_histories_file:
        json.dump(histories, crow_data_violation_histories_file)
    with open(os.path.join(crow_data_dir, 'latest_violations.csv '), 'w') as crow_data_violations_file:
        writer = csv.writer(crow_data_violations_file)
        for violation in violations:
            writer.writerow(violation)
    
    # Svelte app data files

    with open(os.path.join(svelte_data_dir, 'descriptions.json'), 'w') as descriptions_file:
        json.dump(keys_to_descriptions, descriptions_file)

    with open(os.path.join(svelte_data_dir, 'test_violation_histories.json'), 'w') as violation_histories_file:
        total_histories = number_of_pages * page_size
        print(f"storing {total_histories} test histories out of {len(histories)}.")
        histories_in_pages = {}
        for i, (camis, history) in enumerate(histories.items()):
            if i == total_histories:
                break
            histories_in_pages[camis] = history
        json.dump(histories_in_pages, violation_histories_file, indent=3)
    
    with open(os.path.join(svelte_data_dir, 'test_violation_pages.json'), 'w') as violation_pages_file:
        pages = {}
        for i, last_inspection_batch in enumerate(batched(violations, n=page_size)):
            if i == number_of_pages:
                break
            pages[f"page{i}"] = last_inspection_batch
        json.dump(pages, violation_pages_file, indent=3)
    
    


        



if __name__ == "__main__":
    _, source_file, crow_data_dir, svelte_data_dir = sys.argv
    
    #counter = Counter(row["CAMIS"] for row in csv.DictReader(gzip.open("data/DOHMH_New_York_City_Restaurant_Inspection_Results_20240918.csv.gz", 'rt')))
    #import pprint
    #pprint.pprint(counter)
    json_pages(source_file, crow_data_dir, svelte_data_dir,
               1000, 2)
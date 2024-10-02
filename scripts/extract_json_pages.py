import gzip
import json
import csv


def json_pages(path: str, page_size: int, number_of_pages: int):
    done_pages = 1
    result = {}
    page=[]
    for row in csv.DictReader(gzip.open(path, 'rt')):
        if row["INSPECTION DATE"] == "01/01/1900":
            continue
        page.append(row)
        if len(page) == page_size:
            result[f"page{done_pages}"] = page
            done_pages += 1
            page=[]
        if done_pages > number_of_pages:
            print(json.dumps(result, indent=3))
            break


if __name__ == "__main__":
    json_pages("data/DOHMH_New_York_City_Restaurant_Inspection_Results_20240918.csv.gz",
               10, 2)
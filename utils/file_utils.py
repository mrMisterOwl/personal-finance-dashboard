import os
import pandas as pd
import numpy as np
from datetime import datetime

download_dir = os.path.join("downloads")
output_dir = os.path.join("output")

def find_csv_files():
    print("reading csv files")
    files_to_ingest = []
    files = os.listdir(download_dir)
    for file in files:
        if file.endswith(".csv"):
            files_to_ingest.append(file)
    print("found %s files to ingest" % len(files_to_ingest))
    return files_to_ingest

def build_xlsx_file(file):
    print("ingesting file: %s" % file)
    file_path = os.path.join(download_dir, file)
    new_file = os.path.join(output_dir, file.replace(".csv", ".xlsx"))
    data = pd.read_csv(file_path)
    expenses = []
    if file.startswith("cap1"):
        print("Creating Capitol One file %s:" % new_file)
        for idx, row in data.iterrows():
            date = row['Posted Date']
            if np.isnan(float(row['Debit'])):
                amount = float(row['Credit']) * -1
            else:
                amount = float(row['Debit'])
            source = "CREDIT CARD"
            description = str(row['Description']).upper()
            new_exp = {"DATE": date, "AMOUNT": amount, "SOURCE": source, "DESCRIPTION": description}
            expenses.append(new_exp)

    elif file.startswith("bellco"):
        print("Creating Bellco file %s:" % new_file)
        for idx, row in data.iterrows():
            date = convert_date_format(row['Posting Date'])
            amount = float(row['Amount']) * -1
            source = "CHECKING"
            description = str(row['Description']).upper()
            new_exp = {"DATE": date, "AMOUNT": amount, "SOURCE": source, "DESCRIPTION": description}
            expenses.append(new_exp)
    else:
        print("Unknown ingest file: %s. File name must start with 'cap1' or 'bellco'" % file)
    df = pd.DataFrame(expenses, columns=['DATE', 'AMOUNT', 'SOURCE', 'DESCRIPTION'])
    df.to_excel(new_file, index=False)

def convert_date_format(date):
    datetime_object = datetime.strptime(date, '%m/%d/%Y')
    formatted_date = datetime_object.strftime('%Y-%m-%d')
    return formatted_date


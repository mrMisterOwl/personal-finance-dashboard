import utils.file_utils as file_utils



if __name__ == '__main__':

    files = file_utils.find_csv_files()
    for file in files:
        file_utils.build_xlsx_file(file)
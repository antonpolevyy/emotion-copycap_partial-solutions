import os
import csv
import numpy as np
import cv2

# dataset_folder = 'dataset'
csv_file_name = 'duplicates.csv'
# delete files that listed in this column of csv_file_name
column_to_delete = 'image-2'

# img_list = [directory + i for i in os.listdir(directory)]
files_to_delete = []

with open(csv_file_name, 'r') as csvFile:
    print('.csv file opened')
    csvReader = csv.DictReader(csvFile)
    for row in csvReader:
        # print(row)

        if row[column_to_delete] not in files_to_delete:
            files_to_delete.append(row[column_to_delete])

for file in files_to_delete:
    try:
        os.remove(file)
    except OSError:
        print('---[ERROR]--- Failed to delete ', file)
        pass

print('all done')
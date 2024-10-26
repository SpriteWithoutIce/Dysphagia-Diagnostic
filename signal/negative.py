import csv

with open('干咽.csv', 'r', newline='') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

    for i, row in enumerate(rows):
        first_column = row[0].split(',')
        modified_column = []

        for num in first_column:
            modified_num = float(num) * -1
            modified_column.append(str(modified_num))
        rows[i][0] = ','.join(modified_column)

with open('modified_file.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)

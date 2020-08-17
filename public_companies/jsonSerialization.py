import json

# json.dumps() method can convert a Python object into a JSON string.
# json.dump() method can be used for writing to JSON file.


def get_json_data(filename):
    try:
        with open(filename) as json_file:
            json_data = json.load(json_file)
        return json_data
    except FileNotFoundError:
        return None


def store_json_data(filename, dict_data):
    """writes data to JSON file"""
    with open(filename, 'w') as json_file:
        json.dump(dict_data, json_file)


def update_json(add_this):
    """# Updating a JSON file"""

    with open('state.json') as json_file:
        data = json.load(json_file)

        temp = data['companies']

        # appending data to emp_details
        temp.append(add_this)

    store_json_data(data)


def json_to_csv():
    """Convert JSON to CSV in Python"""
    import csv

    # Opening JSON file and loading the data
    # into the variable data
    with open('data.json') as json_file:
        data = json.load(json_file)

    employee_data = data['employee_details']

    # now we will open a file for writing
    data_file = open('data_file.csv', 'w')

    # create the csv writer object
    csv_writer = csv.writer(data_file)

    # Counter variable used for writing
    # headers to the CSV file
    count = 0

    for emp in employee_data:
        if count == 0:
            # Writing headers of CSV file
            header = emp.keys()
            csv_writer.writerow(header)
            count += 1

        # Writing data of CSV file
        csv_writer.writerow(emp.values())

    data_file.close()

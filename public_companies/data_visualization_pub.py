
import csv
from .jsonSerialization import store_json_data, get_json_data
import statistics
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

JSON_FILE = 'datadict.json'
DATA_TYPE = int
DATA_RANGE = [1, 10]


def data_inspection(tase_data_dict):
    """Detect unexpected, incorrect, and inconsistent data."""
    counter = 0
    inspect = []

    for company in tase_data_dict["companies"]:
        if company["found"]:
            counter += 1
            # missing values
            try:
                # data type
                if type(company["women"]) is not int or type(company["men"]) is not int:
                    inspect.append(company)

                # range
                elif not DATA_RANGE[0] <= company["women"] < DATA_RANGE[1] \
                        or not DATA_RANGE[0] < company["men"] < DATA_RANGE[1]:
                    inspect.append(company)

                elif company["women"] >= company["men"]:
                    inspect.append(company)

            except KeyError:
                inspect.append(company)
    print(f"{counter} unexpected entries found")
    return inspect


class Visualisation(object):

    def histogram(data_dict):

        women_l, men_l = get_numerical_list(data_dict)
        print("women:", sum(women_l))
        print("men:", sum(men_l))
        mu_women, mu_men = statistics.mean(women_l), statistics.mean(men_l)  # mean of distribution

        # Histogram
        # n - The values of the histogram bins
        # bins - The edges of the bins
        # patches - Silent list of individual patches
        plt.hist(x=men_l, alpha=0.5, color="orangered", label="Men")
        n, bins, patches = plt.hist(x=women_l, color='lightseagreen',   histtype='stepfilled',
                                    # histtype : {'bar', 'barstacked', 'step', 'stepfilled'}, optional
                                    alpha=0.5, rwidth=0.85, label="Women")

        plt.grid(axis='y', alpha=0.75)
        plt.xlabel('# of Women/Men Directors')
        plt.ylabel('Frequency')
        plt.title(' םינוירוטקרידב םירבגו םישנ תוגיצנ')
        plt.legend()
        plt.text(60, .25, r'$\mu=15, b=3$')  # Add text to the axes.
        # Set a clean upper y-axis limit.
        plt.xlim(0, max(men_l) + 1)
        plt.ylim(0, n.max() + 2)
        plt.show()

    def time_series(self):
        pass

    def bar_plot(found_dict):

        women_l, men_l, companies_name = get_numerical_list(found_dict,True)

        # set width of bar
        barWidth = 0.25
        # Set position of bar on X axis
        r1 = np.arange(len(women_l))
        r2 = [x + barWidth for x in r1]
        # Make the plot
        plt.bar(r1, women_l, color='#7f6d5f', width=barWidth, edgecolor='white', label='women')
        plt.bar(r2, men_l, color='#557f2d', width=barWidth, edgecolor='white', label='men')

        # Add xticks on the middle of the group bars
        plt.xlabel('company', fontweight='bold')
        plt.xticks([r + barWidth for r in range(len(women_l))], companies_name)
        # Create legend & Show graphic
        plt.legend()
        plt.show()


def get_numerical_list(data_dict, name=False):
    women_list = []
    men_list = []
    company_name = []
    for company in data_dict['companies']:
        women_list.append(company["women"])
        men_list.append(company["men"])
        company_name.append(company['companyName'])
    if name:
        return women_list, men_list, company_name
    return women_list, men_list


def bar_plot_(data):
    sectors = {}
    sec_list = []
    freq_list = []
    for company in data['companies']:
        sectors[company['sector']] = sectors.get((company['sector']), 0) + 1
    for sector in sectors:
        sec_list.append(sector)
        freq_list.append(sectors[sector])

    print(sectors)
    plt.bar(sec_list, freq_list)
    plt.show()


def json_store_not_empty(data_dict):
    not_empty_dict = {'companies': []}
    for company in data_dict['companies']:
        if company['found']:
            not_empty_dict['companies'].append(company)

    store_json_data('not_empty_companies_data.json', not_empty_dict)


def copy_to_csv(data_dict):
   # -- copy to csv --:

    csv_file = open('gov_direct_check.csv', 'w')
    # create the csv writer object
    csv_writer = csv.writer(csv_file)

    # Counter variable for writing headers to the CSV file
    count = 0
    for comp in data_dict:
        if count == 0:
            # Writing headers of CSV file
            header = comp.keys()
            csv_writer.writerow(header)
            count += 1
        # Writing data of CSV file
        csv_writer.writerow(comp.values())

    csv_file.close()


def securities_sectors():
    sec_dict = get_json_data('securities.json')
    for sec in sec_dict['securities']:
        # count = 0
        # num = len(sec)
        for comp in sec.values():
            count = 0
            num = len(comp)
            for i in comp:
                for j in data_dict["companies"]:
                    if i == j['companyName']:
                        count += 1
        if num == 0:
            continue
        else:
            print(sec.keys(),str(round((count/num)*100, 1))+'%')


if __name__ == '__main__':
    # inspect raw data
    data_dict = get_json_data('state.json')
    copy_to_csv(data_inspection(data_dict))

    data_dict = get_json_data('not_empty_companies_data.json')
    v = Visualisation
    v.histogram(data_dict)

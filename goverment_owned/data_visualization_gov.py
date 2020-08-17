import csv
import public_companies.jsonSerialization as Serialize
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import json

JSON_FILE = 'datadict.json'
DATA_TYPE = int
DATA_RANGE = [0, 10]


def data_inspection(gov_data_dict):
    """Detect unexpected, incorrect, and inconsistent data."""
    counter = 0
    count_total = 0
    inspect = []

    for dict in gov_data_dict["companies"]:
        for year in dict:
            for company in dict[year]:
                count_total += 1
                if company["found"]:
                    counter += 1
                    # missing values
                    try:
                        # data type
                        if type(company["women"]) is not int or type(company["men"]) is not int:
                            inspect.append(company)

                        # range
                        elif not DATA_RANGE[0] <= company["women"] < DATA_RANGE[1] or not \
                                DATA_RANGE[0] < company["men"] < DATA_RANGE[1] or not \
                                0 <= company["womenCEO"] <= 1 or not 0 <= company['menCEO'] <= 1 \
                                or not 0 <= company["womenChair"] <= 1 or not 0 <= company['menChair'] <= 1:
                            inspect.append(company)

                        elif company["women"] >= company["men"]:
                            inspect.append(company)

                    except KeyError:
                        inspect.append(company)
    print(f"{counter} were found")
    # print("total:", count_total)
    return inspect


def time_series(dict_of_lists):

    df = pd.DataFrame(data=dict_of_lists)

    # gca stands for 'get current axis'
    ax = plt.gca()

    df.plot(kind='line', x='הנש', y='םישנ זוחא', color='lightseagreen', ax=ax)
    df.plot(kind='line', x='הנש', y='םירבג זוחא', color='orangered', ax=ax)
    plt.ylim(0, df['םירבג זוחא'].max() + 10)
    #plt.xlim(2015, 2020)
    plt.title(' םינוירוטקרידב םירבגו םישנ תוגיצנ')

    plt.show()
    # Instead of calling plt.show(), you can call plt.savefig('outputfile.png')


def get_sums(data_dict):
    data_lists = {}
    women_sum_list = []
    men_sum_list = []
    women_ceo_list = []
    men_ceo_list = []
    women_chair_list = []
    men_chair_list = []
    women_outside_list = []
    men_outside_list = []

    for dict in data_dict["companies"]:
        for year in dict:
            women_sum = 0
            men_sum = 0
            women_ceo_sum = 0
            men_ceo_sum = 0
            women_chair_sum = 0
            men_chair_sum = 0
            women_outside_sum = 0
            men_outside_sum = 0

            for company in dict[year]:
                women_sum += company['women']
                men_sum += company['men']
                women_ceo_sum += company['womenCEO']
                men_ceo_sum += company['menCEO']
                women_chair_sum += company['womenChair']
                men_chair_sum += company['menChair']
                women_outside_sum += company['womenOutside']
                men_outside_sum += company['menOutside']
            women_sum_list.append(women_sum)
            men_sum_list.append(men_sum)
            if women_ceo_sum == 0:
                women_ceo_list.append(None)
            else: women_ceo_list.append(women_ceo_sum)
            if men_ceo_sum == 0:
                men_ceo_list.append(None)
            else: men_ceo_list.append(men_ceo_sum)
            women_chair_list.append(women_chair_sum)
            men_chair_list.append(men_chair_sum)
            women_outside_list.append(women_outside_sum)
            men_outside_list.append(men_outside_sum)
    women_percentage = []
    men_percentage = []
    for i in range(len(women_sum_list)):
        women_percentage.append(round(women_sum_list[i]/(women_sum_list[i]+men_sum_list[i]), 2)*100)
        men_percentage.append(round(men_sum_list[i]/(women_sum_list[i]+men_sum_list[i]), 2)*100)

    data_lists = {
        'םישנ': women_sum_list,
        'םירבג': men_sum_list,
        'תויל"כנמ': women_ceo_list,
        'םיל"כנמ': men_ceo_list,
        'שאר תובשוי': women_chair_list,
        'שאר יבשוי': men_chair_list,
        'תויצ"חד': women_outside_list,
        'םיצ"חד': men_outside_list,
        'םישנ זוחא': women_percentage,
        'םירבג זוחא': men_percentage,
        'הנש': list(range(2015, 2021))
    }
    return data_lists


def companies_wo_women(data_dict):
    """Companies without women in BOD"""
    no_women_list = []
    no_women_year = []
    no_women_comp_name = []
    no_women_men = []
    total_list = []
    for dict in data_dict["companies"]:
        for year in dict:
            no_women_sum = 0
            total_sum = 0
            for company in dict[year]:
                if not company['found']:
                    pass
                elif sum([company['women'], company['womenCEO'], company['womenChair'], company['womenOutside']]) == 0:
                    no_women_year.append(year)
                    no_women_comp_name.append(company['companyName'])
                    no_women_men.append(sum([company['men'], company['menCEO'], company['menChair'],
                                             company['menOutside']]))
                    total_sum += 1
                    no_women_sum += 1
                else:
                    total_sum += 1
            total_list.append(total_sum)
            no_women_list.append(no_women_sum)

    final_lists = {
        'companies w/o women': no_women_list,
        'number of companies': total_list,
        'הנש': list(range(2015, 2021))
    }

    no_women_arrays = {
        'שנה': no_women_year,
        'שם חברה': no_women_comp_name,
        'מספר גברים': no_women_men
    }

    return no_women_arrays


def json_found(data_dict):
    found_dict = {'companies': []}
    for company in data_dict['companies']:
        if company['found']:
            found_dict['companies'].append(company)

    Serialize.store_json_data('found_data.json', found_dict)


def write_to_excel(dict_of_lists):

    df = pd.DataFrame(data=dict_of_lists)

    #df = pd.DataFrame(data_dict, columns=columns)
    df.to_excel('gov_excel_file_df.xlsx')



def copy_to_csv(data_dict):
   # -- copy to csv --:

    csv_file = open('gov_time_dataframe.csv', 'w')
    # create the csv writer object
    csv_writer = csv.writer(csv_file)

    # Counter variable for writing headers to the CSV file
    #count = 0
#for i in secdict['securities']: print(i.keys())
    header = data_dict.keys()
    csv_writer.writerow(header)
    for comp in data_dict:
       # if count == 0:
            # Writing headers of CSV file
            # header = comp.keys()
            # csv_writer.writerow(header)
            #count += 1
        # Writing data of CSV file
        for value in data_dict.values():
            csv_writer.writerow(value)

    csv_file.close()


def chairmen_check(data_dict):
    for dict in data_dict["companies"]:
        for year in dict:
            sum = 0
            for company in dict[year]:
                sum += company['menChair']

if __name__ == '__main__':
    data_dict = Serialize.get_json_data('gov_time_series.json')
    #copy_to_csv(data_inspection(data_dict))
    #chairmen_check(data_dict)

    write_to_excel(companies_wo_women(data_dict))
    #time_series(companies_wo_women(data_dict))

    # for dict in data_dict["companies"]:
    #     for year in dict:
    #         for company in dict[year]:
    #            print(year,":", company)


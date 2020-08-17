__author__ = 'Hagar Zemach'

from .tase_API import TASE
from .scraper import SeleniumManager
from .pdf_parser import extract_text, pars_text, get_women_and_men_num
from .pdf_handler import get_report
from .jsonSerialization import get_json_data, store_json_data
import json

import time
import os

FROM_YEAR = 2019
TO_YEAR = 2019
PDF_FILE = 'company_report.pdf'
JSON_FILE = 'state.json'


def run(tase_api, selenium):

    tase_companies_dict = tase_api.companies_list()

    skip = False
    final_data_dict = get_json_data(JSON_FILE)
    if not final_data_dict:
        final_data_dict = {'companies': []}
        skip = True

    if os.path.exists(PDF_FILE):
        os.remove(PDF_FILE)

    # selenium = SeleniumManager()

    for company in tase_companies_dict["taseCompanies"]:
        company_name, company_id, sector = company['companyName'], company["companyID"], \
                                           company["taseSector"]
        company_dict = {'companyID': company_id, 'companyName': company_name, 'sector': sector}

        try:
            if not skip:
                for comp in final_data_dict['companies']:
                    if company_id == comp['companyID']:
                        raise Continue
        except Continue:
            continue

        link = selenium.get_company_reports(company_id, FROM_YEAR, TO_YEAR)
        if link is None:
            print("Report not found for", company)
            continue
        get_report(link)

        text = extract_text('company_report.pdf')

        if text[0] is not None:
            company_dict["found"] = True
            parsed_text = pars_text(text)
            result = get_women_and_men_num(parsed_text)

            try: company_dict["women"] = result[0]["women"]
            except (KeyError, IndexError): company_dict["women"] = -1
            try: company_dict["men"] = result[1]["men"]
            except (KeyError, IndexError): company_dict["men"] = -1
            final_data_dict['companies'].append(company_dict)
            skip = False
        else:
            if text[1]: company_dict["found"] = True
            else: company_dict["found"] = False
            final_data_dict['companies'].append(company_dict)
            skip = False

        store_json_data(JSON_FILE, final_data_dict)
        if os.path.exists(PDF_FILE):
            os.remove(PDF_FILE)


class Continue(Exception):
    pass


if __name__ == '__main__':
    tase_api = TASE()
    selenium = SeleniumManager()

    run(tase_api, selenium)

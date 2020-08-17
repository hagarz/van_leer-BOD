#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'Hagar Zemach'

import requests
import json


class TASE(object):
    """Tel-Aviv Stock Exchange API requests"""

    base_url = 'https://openapigw.tase.co.il'

    def __init__(self):
        self.token = get_token()

    def priority_disclosures(self):
        url = self.base_url + '/tase/prod/api/v1/maya-reports-online/priority-disclosures'
        headers = {
            'authorization': "Bearer "+str(self.token),
            'accept-language': "he-IL",
            'accept': "application/json"
        }
        response = requests.get(url, headers=headers)
        output = response.json()

    def securities(self, indexid, year, month, day):
        """Basic details of securities comprising TASE indices"""
        url = self.base_url + f"/tase/prod/api/v1/basic-indices/index-components-basic/{indexid}/{year}/{month}/{day}"
        headers = {
            'authorization': "Bearer " + str(self.token),
            'accept-language': "he-IL",
            'accept': "application/json"
        }
        response = requests.get(url, headers=headers)
        output = response.json()
        companies_name_list = []
        securities_details = output['indexComponents']['result']
        print(output)

        for i in securities_details:
            companies_name_list.append(i['securityName'])
            # companies_id_dict[i['securityName']] = [i['securityID']]
        print(companies_name_list)
        return companies_name_list

    def indices_codes(self):
        """List of TASE indices and their codes"""
        url = self.base_url + "/tase/prod/api/v1/basic-indices/indices-list"
        headers = {
            'authorization': "Bearer " + str(self.token),
            'accept-language': "he-IL",
            'accept': "application/json"
        }
        response = requests.get(url, headers=headers)
        output = response.json()
        codes_output = output['indicesList']['result']
        codes_dict = {}
        for i in codes_output:
            codes_dict[i['indexName']] = i['indexCode']
        print(codes_dict)
        return codes_dict

    def companies_list(self):
        """
        List of TASE companies.
        API returns: company Name, Sector, issuerID, corporateID
        method returns a dictionary {[companyName]:[ID]}
        """
        url = self.base_url + "/tase/prod/api/v1/basic-securities/companies-list"
        headers = {
            'authorization': "Bearer " + str(self.token),
            'accept-language': "he-IL",
            'accept': "application/json"
        }
        response = requests.get(url, headers=headers)
        output = response.json()
        tase_companies_dict = {"taseCompanies": []}
        for i in output['companiesList']['result']:
            tase_companies_dict["taseCompanies"].append(
               {'companyName': i['companyName'], 'companyID': i['issuerID'], "taseSector": i['taseSector']})
            # tase_companies_dict['companyName'] = i['companyName']
            # tase_companies_dict['companyID'] = i['issuerID']
            # tase_companies_dict["taseSector"] = i['taseSector']
        return tase_companies_dict


def get_token():
    """generate an OAuth2 token """
    body_params = {'grant_type': 'client_credentials', "scope": "tase"}
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    user = get_key()
    password = get_secret()
    token_url = "https://openapigw.tase.co.il/tase/prod/oauth/oauth2/token"

    response = requests.post(token_url, auth=(user, password), data=body_params, headers=headers)
    reply = response.json()
    return reply['access_token']


def get_key():
    """gets api key from file"""
    with open("API_Key.txt", 'r') as file:
        key = file.read()
    file.close()
    return key


def get_secret():
    """gets api secret from file"""
    with open("API_Secret.txt", 'r') as file:
        key = file.read()
    file.close()
    return key

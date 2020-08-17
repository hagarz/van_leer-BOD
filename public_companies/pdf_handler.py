
import requests


def get_report(url):
    # Download report
    response = requests.get(url)
    with open("company_report.pdf", 'wb') as file:
        file.write(response.content)

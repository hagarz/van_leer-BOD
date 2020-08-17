
import pdfplumber
import public_companies.jsonSerialization as Serialize
# -== Time series ==-

FILE_NAME_JSON = 'gov_time_series.json'


def extract_text(file, year):
    year = year
    pdf_file = file
    pdf = pdfplumber.open(pdf_file)
    pages = pdf.pages
    str1 =     "03.03.2020 ךיראתל ןוכנ תורבחב םינהכמ םירוטקריד תמישר"
    str2 =     'החפשמ םש יטרפ םש דיקפת ךיראת '
    str3 =    ' םויס ךיראת'
    str4 = 'החפשמ םש םש דיקפת'
    str5 = '* הנוהכה'
    str6 = '1.1.2015 םויל ןוכנ תויתלשממ תורבחב םינהכמ םירוטקריד'
    str7 = 'םויס'
    str8 = 'תונב תורבחו תויתלשממ תורבח'

    company_dict = {year: []}
    w_count, m_count = 0, 0
    w_ceo, m_ceo = 0, 0
    w_chair, m_chair = 0, 0
    w_outside, m_outside = 0, 0
    count = 0
    for i, pg in enumerate(pages):
        text = pages[i].extract_text(1, 0)
        text_list = text.splitlines()

        for line in text_list:
            if line in {str1, str2, str3, str4, str5, str6, str7, str8} or '12 ךותמ' in line:
                pass

            elif "רוטקריד" in line:
                if "תירוטקריד" in line:
                    w_count += 1
                else:
                    m_count += 1
            elif 'צ"חד' in line:
                if 'תיצ"חד' in line:
                    w_outside += 1
                else:
                    m_outside += 1
            elif 'ל"כנמ' in line:
                if 'תיל"כנמ' in line:
                    w_ceo += 1
                else:
                    m_ceo += 1
            elif 'ר"וי' in line:
                if 'תיר"וי' in line:
                    w_chair += 1
                else:
                    m_chair += 1
            else:
                if count > 0:
                    if sum([w_count, w_chair, w_ceo, m_count, m_chair, m_ceo]) == 0:
                        found = False
                    company_dict[year].append(
                        {"companyName": companyName, "women": w_count, "men": m_count, 'womenCEO': w_ceo,
                         'menCEO': m_ceo, 'womenOutside': w_outside, "menOutside": m_outside, 'womenChair': w_chair,
                         'menChair': m_chair, 'found': found})
                companyName = line
                w_count, m_count, w_ceo, m_ceo, w_chair, m_chair, w_outside, m_outside = 0, 0, 0, 0, 0, 0, 0, 0
                found = True
                count += 1
    if sum([w_count, w_chair, w_ceo, m_count, m_chair, m_ceo]) == 0:
        found = False
    company_dict[year].append(
        {"companyName": companyName, "women": w_count, "men":m_count, 'womenCEO': w_ceo, 'menCEO': m_ceo,
         'womenOutside': w_outside, "menOutside": m_outside, 'womenChair': w_chair, 'menChair': m_chair,
         'found': found})
    # jsonSerialization.store_json_data(FILE_NAME_JSON, company_dict)
    return company_dict


def initialize_json_file():
    init = {'companies': []}
    Serialize.store_json_data(FILE_NAME_JSON, init)


if __name__ == '__main__':
    # initialize_json_file()

    FILE_NAME_PDF = [('directorsmanningreport_01012015-file1.pdf', 2015),
                     ('directorsmanningreport_01082016-file1.pdf', 2016),
                     ('directormanningreport_01062017-file1.pdf', 2017),
                     ('directormanningreport_05072018-file1.pdf', 2018),
                     ('directormanningreport_02012019-file1.pdf', 2019),
                     ('directormanningreport_03032020-file1.pdf', 2020)]

    for y in FILE_NAME_PDF:
        file, year = y

        data_dict = Serialize.get_json_data(FILE_NAME_JSON)

        ts_dict = extract_text(file, year)

        data_dict['companies'].append(ts_dict)
        Serialize.store_json_data(FILE_NAME_JSON, data_dict)

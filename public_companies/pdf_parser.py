
import pdfplumber


def extract_text(file_path):
    print("Extracting text...")
    pdf = pdfplumber.open(file_path)
    pages = pdf.pages
    corporate_governance_questionnaire = False
    for i, pg in enumerate(pages):
        text = pages[i].extract_text(1, 0)
        if text is None:
            continue
        if "ןימ לכמ םירוטקרידה רפסמ" in text:
            pdf.close()
            return text
        else:
            if not corporate_governance_questionnaire:
                if "ידיגאת לשממ ןולאש" in text:
                    corporate_governance_questionnaire = True

    pdf.close()
    return None, corporate_governance_questionnaire


def pars_text(text):
    if "םירבג" in text.partition("ןימ לכמ םירוטקרידה רפסמ")[0]:
        parsed_text = text.partition("ןימ לכמ םירוטקרידה רפסמ")[0]
    else:
        parsed_text = text.partition("ןימ לכמ םירוטקרידה רפסמ")[2]

    return parsed_text


def get_women_and_men_num(parsed_str):
    if parsed_str is None:
        return
    if "cid" in parsed_str:
        parsed_str = parsed_str.replace("cid:170","")
    women_men_list = []
    for j in parsed_str:
        if j.isdigit():
            if not women_men_list:
                women_men_list.append({'women': int(j)})
            else:
                women_men_list.append({"men": int(j)})
                break
    return women_men_list

import pprint
import pandas as pd
import sqlalchemy as db
import requests



def CompaniesList():

    companies = ['Amazon', 'NVIDIA', 'Intel', 'Apple', 'Microsoft', 'HBO Max', 'Netflix', 'Nintendo', 'Sony', 'Google', 'Dell', 'Facebook', 'HP']

    return companies


        

def clearbitInformation(domain_input):
    CLEARBIT_TOKEN = 'sk_b5291d8bbeddea820b1603e2cd7b309e'

    clearbit_info = {
        "industry": "", 
        "description": "", 
        "domain": "", 
        "legalName": "",
        "linkedin": "", 
        "location": "", 
        "logo": "", 
        "employees": "", 
        "employeesRange": "", 
        "name": "", 
        "tags": ""
    }
    
    headers = {'Authorization': 'Bearer {token}'.format(token=CLEARBIT_TOKEN)}

    clearbit_NameToDomainURL = f"https://company.clearbit.com/v1/domains/find?name=:{domain_input}"

    domain_output = requests.get(clearbit_NameToDomainURL, headers=headers).json()
    domain = domain_output['domain']

    company_url = "https://company.clearbit.com/v2/companies/find?domain=" + domain
    company = requests.get(company_url, headers=headers).json()

    clearbit_duplicates = []
    clearbit_list = ["tags", "linkedin"]
    #print("--------------------------------------------------------------")


    for company_tag in company:
        if company_tag in clearbit_list:
            if company_tag == "linkedin":
                linkedin_extracted = company[company_tag] ["handle"]
                if isinstance(company[company_tag], str):
                    company_linkedin = "https://www.linkedin.com/" + linkedin_extracted
                    clearbit_info[company_tag] = company_linkedin
                else:
                    clearbit_info[company_tag] = "None provided"
            else:
                clearbit_info[company_tag] = company[company_tag]
        elif isinstance(company[company_tag], dict) and company[company_tag] not in clearbit_duplicates:
            inner_dict = company[company_tag]
            for inner_tag in inner_dict:
                if inner_tag in clearbit_info:
                    if inner_tag == 'domain':
                        continue
                    else:
                        clearbit_info[inner_tag] = inner_dict[inner_tag]
                        clearbit_duplicates.append(inner_tag)
        elif company_tag in clearbit_info:
            clearbit_info[company_tag] = company[company_tag]

        if company_tag in clearbit_info and clearbit_info[company_tag] != "":
            clearbit_duplicates.append(company_tag)
    
    categories = ["industry", "description", "domain", "legalName", "linkedin", "location", "logo", "employees", "employeesRange", "name", "tags"]


    clearbit_Dataframe = pd.DataFrame.from_records(clearbit_info, columns = categories)
    engine = db.create_engine('sqlite:///clearbitAPITable.db')
    clearbit_Dataframe.to_sql('clearbit_results',con = engine,if_exists = 'replace',index = False)

    query = engine.execute('SELECT * FROM clearbit_results;').fetchall()
    print(pd.DataFrame(query)) 

    
    return clearbit_info


domain = input("Enter Company name: ")
domainInfomration = clearbitInformation(domain)
pprint.pprint(domainInfomration)



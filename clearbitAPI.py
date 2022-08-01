import clearbit
import pprint

clearbit.key = 'sk_111170e184f1f4a664b677009250e622'

def clearbitCompaniesList():
    companies = clearbit.Discovery.search(query={'tech':'marketo'}, sort='score')

    pprint.pprint(companies)

def clearbitInformation(domain_input):
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

    domain_output = clearbit.NameToDomain.find(name=domain_input)
    domain = domain_output['domain']

    company = clearbit.Company.find(domain=domain,stream=True)
    #pprint.pprint(company)

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

    return clearbit_info

'''
domain = input("Enter Company name: ")
domainInfomration = clearbitInformation(domain)
pprint.pprint(domainInfomration)
'''

clearbitCompaniesList()
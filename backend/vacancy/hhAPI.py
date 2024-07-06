import requests

host = "https://api.hh.ru"
headers = requests.utils.default_headers()
headers.update({"User-Agent": 'api-test-agent'})


def get_vacancies(**kwargs):
    print(kwargs)
    query_params = "&".join(["&".join([f"{key}={value}" for value in kwargs[key][0].split(',')]) for key in kwargs])
    response = requests.get(host + f'/vacancies?{query_params}', headers=headers).json()
    print(host + f'/vacancies?{query_params}')
    vacancies = []
    for item in response['items']:
        url = item['url']
        vacancy = requests.get(url, headers=headers).json()
        name = vacancy['name']

        salary = vacancy.get('salary', None)
        if salary is not None:
            salary_min = salary.get('from', None)
            salary_max = salary.get('to', None)
            salary_currency = salary['currency']
            salary = {
                "minimal": salary_min,
                "maximum": salary_max,
                "currency": salary_currency
            }

        experience = vacancy['experience']
        experience_min = None
        experience_max = None
        match experience['id']:
            case "noExperience":
                experience = None
            case "between1And3":
                experience_min = 1
                experience_max = 3
            case "between3And6":
                experience_min = 3
                experience_max = 6
            case "moreThan6":
                experience_min = 6
        if experience is not None:
            experience = {
                "minimal": experience_min,
                "maximum": experience_max
            }

        employment = vacancy['employment']['name']

        schedule = vacancy['schedule']['name']

        company_name = vacancy['employer']['name']
        address = vacancy.get('address', None)
        company_city = None
        company_address = None
        if address is not None:
            company_city = vacancy['address']['city']
            company_address = vacancy['address']['street']
        if company_city is None:
            company_city = vacancy['area']['name']
        company = {
            "name": company_name,
            "city": company_city,
            "address": company_address
        }

        description = vacancy['description']

        href = vacancy['alternate_url']

        vacancies.append({
            "name": name,
            "salary": salary,
            "experience": experience,
            "employment": employment,
            "schedule": schedule,
            "company": company,
            "description": description,
            "href": href
        })
    return vacancies, response['pages']

def load_currency():
    response = requests.get(host + "/dictionaries/", headers=headers).json()
    currencies = response['currency']
    return currencies
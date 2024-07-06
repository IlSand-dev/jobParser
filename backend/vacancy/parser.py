import re
import time

from undetected_chromedriver import ChromeOptions
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.common import NoSuchElementException


class HHParser:
    def __init__(self):
        chrome_options = ChromeOptions()
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        user_agent = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 "
            "Safari/537.36")
        chrome_options.add_argument(f"user-agent={user_agent}")

        self.driver = uc.Chrome(options=chrome_options)

        self.driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})
        self.driver.execute_cdp_cmd('Network.enable', {})
        self.driver.execute_cdp_cmd('Network.setExtraHTTPHeaders',
                                    {"headers": {"Referer": "https://www.google.com",
                                                 "Accept-Language": "en-US,en;q=0.9"}})
        self.url = 'https://hh.ru/vacancy/'

    def parser_start(self, page=None, **kwargs):
        self.driver.get(self.url)
        self.driver.implicitly_wait(2)
        pages = self.driver.find_element(By.CLASS_NAME, 'pager')
        pages_amount = int(pages.find_elements(By.CSS_SELECTOR, 'a[data-qa="pager-page"]')[-1].text)
        hrefs = []
        if page is None:
            for page in range(pages_amount):
                self.driver.get(
                    f"{self.url}?{('&'.join([f'{key}={kwargs[key]}' for key in kwargs]) + '&') if kwargs else ''}page={page}")
                hrefs += self.get_hrefs()
        else:
            self.driver.get(
                f"{self.url}?{('&'.join([f'{key}={kwargs[key]}' for key in kwargs]) + '&') if kwargs else ''}page={page}")
            hrefs = self.get_hrefs()
        vacancies = []
        for href in hrefs:
            print(href)
            self.driver.get(href)
            vacancy = self.scrape()
            vacancies.append(vacancy)
        return vacancies

    def get_hrefs(self):
        hrefs = []
        vacancy_cards = self.driver.find_elements(By.CLASS_NAME, 'vacancy-card--z_UXteNo7bRGzxWVcL7y.font-inter')
        for vacancy_card in vacancy_cards:
            name = vacancy_card.find_element(By.CLASS_NAME,
                                             'vacancy-name--c1Lay3KouCl7XasYakLk.serp-item__title-link')
            hrefs.append(name.find_element(By.XPATH, '..').get_attribute("href"))
        return hrefs

    def scrape(self):
        for i in range(10):
            try:
                name = self.driver.find_element(By.CSS_SELECTOR, "h1[data-qa='vacancy-title']").text
                break
            except NoSuchElementException:
                self.driver.implicitly_wait(2)
                print(self.driver.page_source)
        try:
            salary = self.driver.find_element(By.CSS_SELECTOR, "div[data-qa='vacancy-salary']")
            compensation_type = salary.find_element(By.CLASS_NAME, "vacancy-salary-compensation-type").text
            salary = salary.text.replace(compensation_type, "")
            salaries = re.findall(r"\d[\d+ ]+\d", salary)
            minimal = None
            maximum = None
            if len(salaries) == 2:
                minimal = int(salaries[0].replace(" ", ""))
                maximum = int(salaries[1].replace(" ", ""))
                currency = salary.split()[-1]
            else:
                preposition, currency = map(lambda x: x.strip(), salary.split(salaries[0]))
                if preposition == "от":
                    minimal = int(salaries[0].replace(" ", ""))
                else:
                    maximum = int(salaries[0].replace(" ", ""))
            salary = {
                "minimal": minimal,
                "maximum": maximum,
                "currency": currency,
                "type": compensation_type
            }
        except NoSuchElementException:
            salary = None

        experience = self.driver.find_element(By.CSS_SELECTOR, "span[data-qa='vacancy-experience'").text
        if experience == "не требуется":
            experience = None
        else:
            years = list(map(int, experience.split()[-2].split("–")))
            minimal = None
            maximum = None
            if len(years) == 2:
                minimal = years[0]
                maximum = years[1]
            else:
                minimal = years[0]
            experience = {
                "minimal": minimal,
                "maximum": maximum
            }
        employment, schedule = map(lambda string: string.strip().capitalize(),
                                   self.driver.find_element(By.CSS_SELECTOR,
                                                            "p[data-qa='vacancy-view-employment-mode']").text.split(
                                       ','))
        company = self.driver.find_element(By.CSS_SELECTOR, "div[data-qa='vacancy-company'")
        company_name = company.find_element(By.CLASS_NAME, "vacancy-company-name").text
        city = None
        address = None
        try:
            raw_address = (company.find_element(By.CSS_SELECTOR, "span[data-qa='vacancy-view-raw-address']")
                           .text.split(',', 1))
            if len(raw_address) == 2:
                city, address = map(lambda string: string.strip(), raw_address)
            else:
                city = raw_address[0].strip()
        except NoSuchElementException:
            city = company.find_element(By.CSS_SELECTOR, "p[data-qa='vacancy-view-location']").text
        company = {
            "name": company_name,
            "city": city,
            "address": address
        }

        description = self.driver.find_element(By.CLASS_NAME, "vacancy-section").text

        href = self.driver.current_url.split("?")[0]

        return {
            "name": name,
            "salary": salary,
            "experience": experience,
            "employment": employment,
            "schedule": schedule,
            "company": company,
            "description": description,
            "href": href
        }

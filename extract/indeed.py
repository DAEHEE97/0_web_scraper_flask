from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def get_page_count(keyword):
    
    options = Options()
    browser = webdriver.Chrome(options=options)

    base_url = "https://kr.indeed.com/jobs"
    browser.get(f"{base_url}?q={keyword}")
    
    soup = BeautifulSoup(browser.page_source, "html.parser")
    
    pagination = soup.find('nav', class_='css-jbuxu0 ecydgvn0')    
    
    pages = pagination.find_all('div', recursive=False)
    
    length = len(pages)
    
    # 5를 초과하는 6 이상 부터는 처리 하지 않을 예정
    if length == 0:
        return 1
    elif length > 5:
        return 5
    else: 
        return length



def extract_indeed_jobs(keyword):
    
    pages = get_page_count(keyword)
    
    results = []
  
    for page in range(pages):
        
        options = Options()

        browser = webdriver.Chrome(options=options)
        
        base_url = "https://kr.indeed.com/jobs"
        search_term = f'{keyword}'
        final_url = f"{base_url}?q={search_term}&start={page*10}"
        
        print(f'Request url : {final_url}')
        browser.get(final_url)

        # --- bs4 처리 

        soup = BeautifulSoup(browser.page_source, "html.parser")

        job_list = soup.find("ul", class_="jobsearch-ResultsList")

        jobs = job_list.find_all('li', recursive=False)


        # li 태그 중 class 네임에 따라 출력,
        # find, none 논리로 출력 


        for job in jobs:

            zone = job.find("div", class_="mosaic-zone")

            if zone == None:

                # anchor = job.find_all('a') # list

                anchor = job.select_one('h2 a') # dict

                title = anchor['aria-label']
                link = anchor['href']

                company = job.find('span', class_='companyName')
                location = job.find('div', class_='companyLocation')

                # dict 데이터 형
                job_data = {
                    'position': title.replace(",", " "),
                    'company': company.string.replace(",", " "),
                    'location': location.string.replace(",", " "),
                    'link': f"https://kr.indeed.com{link}"

                }

                # 결과 리스트 append
                results.append(job_data)

    
    return results


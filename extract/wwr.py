from requests import get 
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def extract_jobs(keyword):

    base_url = "https://weworkremotely.com/remote-jobs/search?utf8=✓&term="

    response = get(f"{base_url}{keyword}")

        
    if response.status_code != 200:
        print("Can't request website")
    else:

        print(f'Request url : {base_url}{keyword}')

        soup = BeautifulSoup(response.text,"html.parser")
        
        # print(soup.find_all('title'))

        jobs = soup.find_all('section', class_="jobs")
        # print(soup.find_all('section', class_="jobs"))    
        # print(len(jobs))
        
        results = []
        
        for job_section in jobs:
        
            # print(job_section.find_all('li')) 
            job_posts = job_section.find_all('li')
            
            # 리스트 컴프리헨션으로 view-all 클래스 제외 (버튼)
            job_posts = [post for post in job_section.find_all('li') if 'view-all' not in post['class']]

            for post in job_posts:
                
                
                anchors = post.find_all('a') # list
                
                anchor = anchors[1] # dictionary in list
                
                link = anchor['href'] # value in dictionary
                
                # anchor('a') 내 span tag (class = company)추출, list
                company, position, region = anchor.find_all('span',class_='company')
                
                title = anchor.find('span', class_='title')
                
                # html tag 제외 후, dictionary 데이터 생성 후, list append
                data_result = {
                    #'title': title.string,
                    'position' : position.string.replace(',', ' '),
                    'company' : company.string.replace(',', ' '),
                    'location' : region.string.replace(',', ' '),
                    'link' : f'https://weworkremotely.com{link}'
                    }
                
                results.append(data_result)
            

        return results
    
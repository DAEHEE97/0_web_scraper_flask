def save_to_file(keyword,jobs):

    file = open(f"{keyword}.csv", "w",encoding="utf-8-sig")
    # 파일에 헤더 입력 , \n
    file.write("Position,Company,Location,URL\n")

    # jobs 리스트, job dict
    for job in jobs:
        file.write(f"{job['position']},{job['company']},{job['location']},{job['link']}\n")

    file.close()


        

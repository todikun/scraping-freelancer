import os
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup


def get_data(pages):
    url = 'https://www.freelancer.com/jobs/{}'.format(pages)
    site = 'https://www.freelancer.com'

    # scraping process
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    contents = soup.find_all('div', 'JobSearchCard-item')

    job_list = []

    for content in contents:
        titles = content.find('a', 'JobSearchCard-primary-heading-link').text.strip()
        try:
            salary = content.find('div', 'JobSearchCard-primary-price').text.strip().split(' ')
            value_salary = salary[0].strip()
        except:
            value_salary = 'none'

        link = site + content.find('a')['href']

        # sorting_data
        data_dict = {
            'titles': titles,
            'salary': value_salary,
            'link': link
        }

        # append
        job_list.append(data_dict)

    return job_list


def generate_file(data, pages):
    # generate csv & excel
    df = pd.DataFrame(data)
    df.to_csv(f'result/freelancer.com page_{pages}.csv', index=False)
    df.to_excel(f'result/freelancer.com page_{pages}.xlsx', index=False)
    print(f'File csv & xlsx successfully created')


def run(total_page):
    try:
        os.mkdir('result')
    except FileExistsError:
        pass

    final_result = []
    for counter in range(total_page):
        counter += 1
        final_result += get_data(counter)
        print('scraping page : ', counter)

    # writing json
    with open(f'result/freelancer.com page_{total_page}.json', 'w+') as json_data:
        json.dump(final_result, json_data)
    print('JSON successfully created')

    # generate file csv & excel
    generate_file(final_result, total_page)


if __name__ == '__main__':
    page = int(input('Input total page : '))
    run(page)

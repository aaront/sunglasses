__title__ = 'sunglasses'
__version__ = '0.0.1'
__author__ = 'Aaron Toth'

import aiohttp
import asyncio
import lxml.html
import csv
import os
import string
import tqdm

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
page_data = []


def get_output_file(category):
    return os.path.join(data_dir, category + ".csv")


def save_page_data(category, rows):
    with open(get_output_file(category), 'a', newline='', encoding='utf-8') as output:
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        writer.writerows(rows)


@asyncio.coroutine
def fetch_page_data(sem, category, url):
    with (yield from sem):
        response = yield from aiohttp.request('GET', url=url)
        page = (yield from response.read_and_close(decode=True))
        save_page_data(category, parse_page(page))


@asyncio.coroutine
def wait_progress(c):
    for f in tqdm.tqdm(asyncio.as_completed(c), total=len(c)):
        yield from f


def parse_page(page):
    html = lxml.html.fromstring(page.decode('utf-8'))
    rows = html.xpath('//table[@summary="Salary Disclosure"]//tbody/tr')
    all_cells = []
    for row in rows:
        formatted = [string.capwords(cell.text_content().strip()) for cell in row.xpath('td')]
        if '\r\n\t' in formatted[0]:
            formatted[0] = formatted[0].split('\r\n\t')[0].strip()
        if '\xa0/\xa0' in formatted[3]:
            formatted[3] = formatted[3].split('\xa0/\xa0')[0].strip()
        all_cells.append(formatted)
    return all_cells


def run(organizations, year,
        base_url='http://www.fin.gov.on.ca/en/publications/salarydisclosure/pssd/orgs.php?organization={}&year={}'
                 '&pageNum_pssd={}',
        concurrent_requests=10):
    urls = []
    for org in organizations:
        category = org[0]
        max_page = org[1]
        if max_page == 0:
            urls.append([category, base_url.format(category, year, max_page)])
        else:
            for pg in range(max_page):
                urls.append([category, base_url.format(category, year, pg)])
    sem = asyncio.Semaphore(concurrent_requests)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(wait_progress([fetch_page_data(sem, u[0], u[1]) for u in urls]))


def main():
    organizations = [
        ['ministries', 5],
        ['legislative', 0],
        ['judiciary', 0],
        ['crown', 1],
        ['electricity', 5],
        ['municipalities', 12],
        ['schoolboards', 6],
        ['universities', 7],
        ['colleges', 2],
        ['hospitals', 4],
        ['other', 2]
    ]
    run(organizations, 2013)


if __name__ == '__main__':
    main()
import asyncio
import threading
import aiohttp
import time
from bs4 import BeautifulSoup

# @asyncio.coroutine  # 修饰符，等同于 asyncio.coroutine(hello())
# def hello():
#     print('Hello world! (%s)' % threading.currentThread())
#     yield from asyncio.sleep(1)  # 执行到这一步以后，直接切换到下一个任务，等到一秒后再切回来
#     print('Hello again! (%s)' % threading.currentThread())


async def hello():
    print("begin")
    r = await asyncio.sleep(5)
    print("end")


async def pa(url, res_list):
    print('>>>', url)
    sem = asyncio.Semaphore(5)
    header = {"User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36'}
    with (await sem):
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=header) as resp:
                print(url, resp.status, resp.content)
                assert resp.status == 200
                res_list.append(await resp.text())
                session.close()


def parse_html(html):
    # print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    divs = soup.find_all('div', attrs={'class': 'ContentItem-main'})
    for div in divs:
        aa = div.find('a', attrs={'class': 'UserLink-link'})
        img = aa.find('img')['srcset'].split(' ')[0]
        rich = div.find('div', attrs={'class': 'RichText'})
        aa = aa.find_next('a', attrs={'class': 'UserLink-link'})
        name = aa.get_text()
        uid = aa['href'].split('/')[-1]
        print(name, uid)


page_url_base = 'https://www.zhihu.com/people/excited-vczh/following?page='

loop = asyncio.get_event_loop()
ret_list = []
totle = 200
begin = 0
for a in range(int(totle /5)):
    end = begin + 5
    urls = [page_url_base + str(i + 1) for i in range(begin, end)]
    begin = end

    tasks = [pa(host, ret_list) for host in urls]
    loop.run_until_complete(asyncio.wait(tasks))

    for ret in ret_list:
        parse_html(ret)
    ret_list.clear()


loop.close()





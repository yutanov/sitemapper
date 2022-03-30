#! /usr/bin/env python3

from sitemapper.crawler import Crawler
import asyncio
import signal
from datetime import datetime
import prompt


def crawler(root_url, out_file, out_format='txt', maxtasks=100, exclude_urls=None):
    """
    run crowler
    :param root_url: Site root url
    :param out_file: path to the out file
    :param out_format: format of out file [xml, txt]
    :param maxtasks: max count of tasks
    :return:
    """
    loop = asyncio.get_event_loop()
    c = Crawler(root_url, out_file=out_file, out_format=out_format, maxtasks=maxtasks)
    if exclude_urls:
        c.set_exclude_url(urls_list=exclude_urls)
    loop.run_until_complete(c.run())

    try:
        loop.add_signal_handler(signal.SIGINT, loop.stop)
    except RuntimeError:
        pass


def main():
    root_url = prompt.string("Enter url starts with 'http://' or 'https://' : ")
    url = root_url.split('/')[2]
    file_name = '{}_sitemap.txt'.format(url)

    time_start = datetime.now()
    crawler(root_url, out_file=file_name)
    time_finish = datetime.now()
    time = time_finish - time_start

    print('Finished in {}'.format(time))

    links = sum(1 for line in open(file_name, 'r'))
    print('Total links: ', links)


if __name__ == "__main__":
    main()

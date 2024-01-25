###
# File: /pyzotero_test/main.py
# Created Date: Thursday, January 25th 2024
# Author: Zihan
# -----
# Last Modified: Thursday, 25th January 2024 12:23:16 pm
# Modified By: the developer formerly known as Zihan at <wzh4464@gmail.com>
# -----
# HISTORY:
# Date      		By   	Comments
# ----------		------	---------------------------------------------------------
###

from pyzotero import zotero
import re  # regular expression
import yaml

# read from file
with open("api_key.txt", "r") as f:
    api_key = f.readline().strip()
    library_id = f.readline().strip()
    library_type = f.readline().strip()


def select_all_book_sections_and_change_to_conference_paper():
    zot = zotero.Zotero(library_id, library_type, api_key)
    items = zot.everything(zot.top())

    for item in items:
        # if doi in extra field
        if item["data"]["itemType"] == "bookSection" and "DOI" in item["data"]['extra']:
            # show all attributes and sub-attributes of item
            # print(item["data"]['extra'])
            # example of extra field:
            # DOI: 10.1017/CBO9781139042918.017
            # Citation Key: xiang2011DistributedTransferLearning

            doi = re.findall(r"DOI: (.*)", item["data"]['extra'])[0]
            bookTitle = item["data"]["bookTitle"]
            item["data"]["bookTitle"] = ""
            item["data"]["conferenceName"] = bookTitle

            # try:
            item["data"]["itemType"] = "conferencePaper"
            # except Exception as e:

            item["data"]["DOI"] = doi
            try:
                zot.update_item(item)
            except Exception as e:
                print(e)
                print(item["data"]["title"])
                continue
            print(f"updated {item['data']['title']}")


def get_conference_name_from_dblp(item):
    # https://dblp.org/search?q={z:title}&h=1000&f=0"
    title = item["data"]["title"]
    title = title.replace(" ", "+")
    url = f"https://dblp.org/search?q={title}&h=1000&f=0"

    import requests
    from bs4 import BeautifulSoup

    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    # print(soup.prettify())

    # find this:
    #  <span class="title" itemprop="name">
    #  When Machine Unlearning Jeopardizes Privacy.
    # </span>
    # <a href="https://dblp.org/db/conf/ccs/ccs2021.html#Chen000HZ21">
    #  <span itemprop="isPartOf" itemscope="" itemtype="http://schema.org/BookSeries">
    #   <span itemprop="name">
    #    CCS
    #   </span>
    #  </span>
    #  <span itemprop="datePublished">
    #   2021
    #  </span>

    item = soup.find("span", {"class": "title", "itemprop": "name"})

    if item is None:
        return None, None, None

    title = item.text
    conference = item.find_next("span", {"itemprop": "name"}).text
    year = item.find_next("span", {"itemprop": "datePublished"}).text

    # print(f"title: {title}, conference: {conference}, year: {year}")
    return title, conference, year


def get_conference_full_name(dblp_conf_result):
    # dblp_conf_result = "CCS"
    pass


def get_conference_rank(conference_code, file_path):
    # if no such file, return None



    with open(file_path, 'r') as file:
        conferences = yaml.load(file, Loader=yaml.FullLoader)

        conference = conferences[0]
        return conference['rank']
    


    return None


def get_conference_yaml_path(conference_code, repo_path, local=True):
    if not local:
        raise NotImplementedError
    # find /Volumes/Mac_Ext/codes/ccf-deadlines/conference/ -name "*.yml" | xargs grep -i "dblp: ccs"
    target_file_name = f"{conference_code}.yml"
    import os
    target_conference_path = f"{repo_path}/conference/"
    # /Volumes/Mac_Ext/codes/ccf-deadlines/conference   main                                                                      base  03:33:04 下午
    # ❯ tree
    # .
    # ├── AI
    # │   ├── aaai.yml
    # │   ├── aamas.yml
    # │   ├── acl.yml
    # ...

    sub_dirs = os.listdir(target_conference_path)
    for sub_dir in sub_dirs:
        sub_dir_path = os.path.join(target_conference_path, sub_dir)
        if os.path.isdir(sub_dir_path):
            for file_name in os.listdir(sub_dir_path):
                if file_name == target_file_name:
                    return os.path.join(sub_dir_path, file_name)
    return None


if __name__ == "__main__":
    zot = zotero.Zotero(library_id, library_type, api_key)
    items = zot.everything(zot.top())

    # choose conference paper
    for item in items:
        if item["data"]["itemType"] == "conferencePaper":
            title = item["data"]["title"]
            _, conference, year = get_conference_name_from_dblp(item)
            if conference is None:
                continue
            yaml_path = get_conference_yaml_path(
                conference.lower(), '/Volumes/Mac_Ext/codes/ccf-deadlines')
            if yaml_path is None:
                continue
            dblp_result = get_conference_rank(conference.lower(), yaml_path)
            # write to extra field "CCF: {dblp_result}"
            # if extra is null, just wirte; else, append a new line
            if "extra" not in item["data"]:
                item["data"]["extra"] = f"CCF: {dblp_result}"
            else:
                item["data"]["extra"] += f"\nCCF: {dblp_result}"
            zot.update_item(item)
            print(f"updated {title}")

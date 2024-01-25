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


if __name__ == "__main__":
    select_all_book_sections_and_change_to_conference_paper()

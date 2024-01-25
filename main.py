###
 # File: /pyzotero_test/main.py
 # Created Date: Thursday, January 25th 2024
 # Author: Zihan
 # -----
 # Last Modified: Thursday, 25th January 2024 12:21:21 pm
 # Modified By: the developer formerly known as Zihan at <wzh4464@gmail.com>
 # -----
 # HISTORY:
 # Date      		By   	Comments
 # ----------		------	---------------------------------------------------------
###

from pyzotero import zotero

# read from file
with open("api_key.txt", "r") as f:
    api_key = f.readline().strip()
    library_id = f.readline().strip()
    library_type = f.readline().strip()

if __name__ == "__main__":
    zot = zotero.Zotero(library_id, library_type, api_key)
    items = zot.top(limit=5)

    for item in items:
        print(item["data"]["title"])
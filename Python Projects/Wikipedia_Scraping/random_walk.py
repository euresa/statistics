# random_walk.py
# Author: Sam Eure
# Date: May 17, 2021
"""
I'm going to test out my Raspberry Pi's capabilities by running 
this script indefinitely on it.
"""

from random import shuffle

from wiki import WikiScraper, combine

N = 10
new_subject = WikiScraper(subject="World History")
old_links = combine(new_subject.hyperlinks)
file_path = "history.txt"
with open(file_path, "w") as open_file:
    for _ in range(N):
        sub = new_subject.subject
        print(sub, end='\n')
        open_file.write(sub)
        open_file.write(", ")
        open_file.write(str(len(old_links)))
        open_file.write("\n")
        shuffle(old_links)
        idx = 0
        try:
            new_subject = WikiScraper(link=old_links[idx])
            links = combine(new_subject.hyperlinks)
            while len(links) < 10:
                print(f"{new_subject.subject} was too short with {len(links)}")
                idx = idx + 1
                new_subject = WikiScraper(link=old_links[idx])
                links = combine(new_subject.hyperlinks)
            old_links = links.copy()
        except:
            print(f"Failed to scrape page:{old_links[idx]}")
            idx = idx + 1
exit()
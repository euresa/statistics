#random_walk.py
#Author: Sam Eure
#Date: May 17, 2021
'''
I'm going to test out my Raspberry Pi's capabilities by running 
this script indefinitely on it.
'''

from random import shuffle

import wiki
from wiki import WikiScraper


new_subject = WikiScraper(subject='World History')
old_links = combine(new_subject.hyperlinks)
f = open("history.txt", "w")
while True:
    sub = new_subject.subject
    print(sub)
    f.write(sub)
    f.write('\n')
    shuffle(old_links)
    idx = 0
    new_subject = WikiScraper(link=old_links[idx])
    links = combine(new_subject.hyperlinks)
    while len(links) < 3:
        print(f'{new_subject.subject} was too short with {len(links)}')
        idx = idx + 1
        new_subject = WikiScraper(link=old_links[idx])
        links = combine(new_subject.hyperlinks)
    old_links = links.copy()
    print(new_subject.subject)
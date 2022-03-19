

import urllib3
import json
from bs4 import BeautifulSoup


def get_words(url):
	words = []
	http = urllib3.PoolManager()
	r = http.request('GET', url)

	soup = BeautifulSoup(r.data.decode('utf-8'), "html.parser")

	for mot in soup.find_all("span", class_="mot"):
		for w in mot.text.split(" "):
			if len(w):
				words.append(w)
	return words


words = []

for i in range(1, 16):
	url = "https://www.bestwordlist.com/5letterwordspage{}.htm"
	if i == 1:
		url = "https://www.bestwordlist.com/5letterwords.htm"
	else:
		url = url.format(i)
	print(url)
	words += get_words(url)

print(len(words))

with open("all5", "w+") as f:
	for w in words:
		f.write(w+"\n")

#!/usr/bin/env python3

import re
import argparse
import requests
import yaml

wikiurl = "https://wikis.swarthmore.edu/ling073/"
apiurl = "api.php?action=query&prop=revisions&rvprop=content&format=json&titles={}"

#sectionMatch = re.compile("\=+([^\=]+?)\=+")
#tagReplace = re.compile("\{\{tag\|(.*?)\}\}")
testMatch = re.compile("\{\{[Tt]ransferTest\|(.*?)\|(.*?)\|(.*?)\|(.*?)\}\}")
fnTemplate = "{}.tests.txt"

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='scrape all {{transferTest}} templates on a page into a parallel corpus')
	parser.add_argument('pagename', type=str, #nargs=1,
		help='name of the page on the wiki')
	parser.add_argument('-p', '--pair', '--langPair', type=str,
		help='ISO codes of the two languages for the translation direction you want to scrape, e.g. abc-xyz')

	args = parser.parse_args()

	langCode = args.pair
	(lg1, lg2) = args.pair.split('-')
	(fn1, fn2) = (fnTemplate.format(lg1), fnTemplate.format(lg2))

	pageName = args.pagename
	fullUrlToGet = wikiurl+apiurl.format(pageName)
	#print(fullUrlToGet)

	r = requests.get(url=fullUrlToGet)
	rawjson = r.json()
	#print(rawjson)
	if len(rawjson['query']['pages']) != 1:
		print("Unexpected number of pages provided: {}".format(rawjson['query']['pages']))
	else:
		pageId = list(rawjson['query']['pages'])[0]
		#print(rawjson['query']['pages'][pageId])
		try:
			rawmarkup = rawjson['query']['pages'][pageId]['revisions'][0]['*']
		except:
			print("Page contents not as expected; page title probably not given correctly")

	lastSection = ""
	tests = {lg1: [], lg2: []}
	for line in rawmarkup.split('\n'):
		if testMatch.search(line):
			#print(line)
			(testLg1, testLg2, testText1, testText2) = testMatch.search(line).groups()
			if testLg1 == lg1 and testLg2 == lg2:
				tests[lg1].append(testText1)
				tests[lg2].append(testText2)

	for (lgName, outFileName) in zip((lg1, lg2), (fn1, fn2)):
		with open(outFileName, 'w') as outFile:
			outFile.write('\n'.join(tests[lgName]))

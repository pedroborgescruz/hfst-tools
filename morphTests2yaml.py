#!/usr/bin/env python3

#curl -s "https://wikis.swarthmore.edu/ling073/api.php?action=query&prop=revisions&rvprop=content&format=txt&titles=Grammar_documentation/Examples" | perl -pe 's/\{\{tag\|(.*?)\}\}/<\1>/g' | grep -Po 'Template:MorphTest.*?|\=.*=' | perl -pe 's/\{\{morphTest\|(.*?)\|(.*?)\}\}/    \1 : \2/g' | sed -r '^C\=+([^=]+)\=+/  "\1":/g'

import re
import argparse
import requests
import yaml

wikiurl = "https://wikis.swarthmore.edu/ling073/"
apiurl = "api.php?action=query&prop=revisions&rvprop=content&format=json&titles={}"

sectionMatch = re.compile("\=+([^\=]+?)\=+")
tagReplace = re.compile("\{\{tag\|(.*?)\}\}")
testMatch = re.compile("\{\{morphTest\|(.*?)\|(.*?)\}\}")

template = {'Config': {'hfst': {'App': 'hfst-lookup', 'Gen': '../{}.autogen.hfst', 'Morph': '../{}.automorf.hfst'}}, 'Tests': {}}

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='dump a yaml file from a wiki page containing {{morphTest}} templates')
	parser.add_argument('pagename', type=str, #nargs=1,
		help='name of the page on the wiki')
	parser.add_argument('-l', '--langCode', type=str,
		help='ISO code for the language of the data')

	args = parser.parse_args()

	langCode = args.langCode
	template['Config']['hfst']['Gen'] = template['Config']['hfst']['Gen'].format(langCode)
	template['Config']['hfst']['Morph'] = template['Config']['hfst']['Morph'].format(langCode)

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
		rawmarkup = rawjson['query']['pages'][pageId]['revisions'][0]['*']

	lastSection = ""
	for line in rawmarkup.split('\n'):
		if sectionMatch.match(line):
			lastSection = sectionMatch.match(line).groups()[0].strip()
			#print(lastSection)
			template['Tests'][lastSection] = {}
		elif tagReplace.search(line):
			tempLine = tagReplace.sub("<\g<1>>", line)
			#print(tempLine)
			if testMatch.search(tempLine):
				matchTests = testMatch.findall(tempLine)
				#print(matchTests)
				matchTestAnalyses = []
				for matchTest in matchTests:
					
					if matchTest[0] in matchTestAnalyses:
						template['Tests'][lastSection][matchTest[0]].append(matchTest[1])
					else:
						template['Tests'][lastSection][matchTest[0]] = [matchTest[1]]
					matchTestAnalyses.append(matchTest[0])

	outFileName = "{}.yaml".format(langCode)
	with open(outFileName, 'w') as outFile:
		yaml.dump(template, outFile, default_flow_style=False, allow_unicode=True)

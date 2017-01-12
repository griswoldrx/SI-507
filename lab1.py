import wikipedia
import re

search = input('Enter a search term:')
result = wikipedia.search(search)

for each in range(len(result)):
	content = wikipedia.WikipediaPage(result[each])
	## remove all special characters and numbers to count words only
	content = re.sub(r'[^a-zA-Z ]', '', content.content)
	words = content.split()
	length = len(words)
	print(str(each +1) + ':', result[each], length)
from nltk.corpus import stopwords

def get_stopwords():

	stop = set(stopwords.words('english'))
	stop = set([s.replace("'", "") for s in stop])

	# Add years to prevent spikes
	for year in range(1900, 2020):
		stop.add(str(year))

	# Add small numbers
	for num in range(0, 100):
		if len(str(num)) < 2:
			stop.add(str(num))
			num = '0' + str(num)
			
		stop.add(str(num))
		
	# Add these extra stopwords to the list
	extra = [
		'use', 'using', 'uses', 'used', 'based', 'including', 'include', 'approach',
		'wa', 'ha', 'doe'
			]
	for word in extra:
		stop.add(word)
		
	return(stop)
	

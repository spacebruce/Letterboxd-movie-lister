# Letterboxd movie lister

Returns a list of watched movies logged to the specified Letterboxd.com profile and regurgigates the list into a file. Does not rely on nor care about the diary system.

Usage:

	python letterboxd.py username outfile
	
	python letterboxd.py username outfile year

adding the argument "year" to the end of the call makes this retrieve the year a film was released. This mode is much slower as it scans every release year page on the users film list. This isn't the way I would have liked to add this feature, but alas, letterboxd doesn't supply a public API.
	
Output format sample:

	...
	Man of Steel
	Mandy ★★★★★
	Maniac Cop ★★
	Marooned ★½
	...
	
If an argument is missing, the script prompts for the information when needed

Works as of 14th of November 2018. If it's broken, feel free to raise an issue for a fix.

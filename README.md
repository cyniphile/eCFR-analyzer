# eCFR-analyzer

The goal of this project is to create a simple website to analyze Federal Regulations. 

The eCFR is available at https://www.ecfr.gov/.  There is a public api for it.
- https://www.ecfr.gov/developers/documentation/api/v1#/
    - In order to create the point-in-time features of the eCFR we process these XML files into smaller units that we then track over time. Our APIs provide access to these various transformations and generated metadata as well as historical search.

- Please write code to download the current eCFR
	- seems to be organized into 50 titles
	- title
    	- Chapter
    		- Subchapter
				- Part
					- subpart
						- Section
							- Subsection
- Analyze it for items such as
	- word count per agency
	- historical changes over time. 
	- Feel free to add your own custom metrics.

- There should be a front end visualization for the content where we can click around and ideally query items. 
- Additionally, there should be a public github project with the code.
- Feedback on the project
- Duration 
	- Start 8:30pm 4/14/2025
- Link to github repo
	- https://github.com/cyniphile/eCFR-analyzer
- Link to frontend 

We advise you to spend no more than 24 hours on this assignment.
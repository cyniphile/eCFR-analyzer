## Next steps
Read these
- https://www.ecfr.gov/reader-aids/using-ecfr/reading-ecfr-content
- https://www.ecfr.gov/reader-aids/using-ecfr/ecfr-changes-through-time
- how does title correlate to agency?
- still need to figure out changes api



## Day 2
- Goal is to finish word counting + figure out changes api. Stretch goal is to design/build local version of website, with plan for deployment.
- Want to finish this up by EOD Wednesday (day 3) (would focus more here but have a lot on my plate at work + another ongoing interview process)
- Big picture: thing about this project from a DOGE perspective. Want to increase govt efficiency so:
  - Departments with tons of words in the CFR are probably not doing a good job of communicating their rules and regulations. (But some departments are more complicated by nature...a good way to "normalize" raw word count??)
  - Departments with tons of changes might "problem children" for variety of reasons: political issues, congressional meddling (or incompetence in how the dept writes the cfr)
  - TODO: brainstorm more deeply how use this data for efficiency analysis

## Day 1
- As I was falling asleep thought of some things:
	- would be cool to vectorize at least one of the titles, and display an interactive UMAP of the sections and subsections, color coded by chapter
		- this would allow for a quick overview of the structure of the CFR; a more visual/intuitive way to explore the CFR
		- could also be used to find similar sections/subsections, but perhaps more interesting highlighting anomalies (paragraphs that seem to belong to another section, etc)  # type: ignore 
		- this is low priority: need to accomplish MVP first
		- TODO: brainstorm with claude a bit more on this
			- think about size of data
			- metadata tagging, etc
- Took ~1.5 hours to do basic project setup, familiarization with the CFR, the eCFR api, and download all the complete part files. Took ~30min to download the raw data (778M)
- Not doing too much verification of data yet, but so far they are big files with lots of lines that match up with what I've requested. Low pri TODO to verify more
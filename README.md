# caltech-crawl
To run the crawler: python crawler2.py 
(you may edit the max_pages parameter in crawl_caltech_concurrent, to desired number of crawled pages)
To perform the analysis: python graphs.py
Ensure crawled_data.json is in the same directory as graphs.py before running the analysis script.

Approach:
This crawler uses a concurrent fetching strategy with breadth-first search. It starts from a seed URL and fetches pages in parallel where possible, following links to discover new pages systematically. 



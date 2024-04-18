import fetcher3
from collections import deque, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse
import json

def is_caltech_domain(url):
    return urlparse(url).netloc.endswith('.caltech.edu')

def crawl_caltech_concurrent(start_url, max_pages=350, max_workers=10):
    visited = set()
    queue = deque([start_url])
    crawled_count = 0
    links_data = defaultdict(list)  # Store outgoing links for each visited page

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_url = {executor.submit(fetcher3.fetch_links, start_url): start_url}
        
        while future_to_url and crawled_count < max_pages:
            for future in as_completed(future_to_url):
                current_url = future_to_url[future]
                if current_url not in visited:
                    visited.add(current_url)
                    crawled_count += 1
                    print(f"Crawled {crawled_count}: {current_url}")
                    
                    links = future.result() or []
                    for link in links:
                        if is_caltech_domain(link):
                            links_data[current_url].append(link)
                            if link not in visited and link not in [future_to_url[f] for f in future_to_url]:
                                queue.append(link)
                                future_to_url[executor.submit(fetcher3.fetch_links, link)] = link
                
                del future_to_url[future]

                while queue and len(future_to_url) < max_workers:
                    next_url = queue.popleft()
                    if next_url not in visited and next_url not in [future_to_url[f] for f in future_to_url]:
                        future_to_url[executor.submit(fetcher3.fetch_links, next_url)] = next_url

                if crawled_count >= max_pages:
                    break

    with open('crawled_data.json', 'w') as file:
        json.dump(links_data, file)

    print(f"Data collected for {len(links_data)} pages and saved to crawled_data.json")

if __name__ == "__main__":
    start_url = "http://www.caltech.edu"
    crawl_caltech_concurrent(start_url)

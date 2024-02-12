import os
import os.path

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from collections import defaultdict
from whoosh.fields import Schema, TEXT, KEYWORD, ID, STORED
from whoosh.index import create_in, open_dir
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import LockError

def crawl_and_index(base_url, index_path):
    # Fetch the page containing the list of publications
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Initialize Whoosh index
    # schema = Schema(title=TEXT(stored=True))
    schema = Schema(title=TEXT(stored=True), authors=TEXT(stored=True), year=ID(stored=True), 
                    publication_url=ID(stored=True, unique=True), author_profile_url=ID(stored=True))
    
    if not os.path.exists(index_path):
        os.mkdir(index_path)
        
    ix = create_in(index_path, schema)
    writer = ix.writer()

    # Extract publication information
    for publication_div in soup.find_all('div', class_='result-container'):
        title_tag = publication_div.find('h3', class_="title")

        if title_tag:
            title = title_tag.get_text(strip = True)
        else:
            title = "N/A"
        
            
        authors_tags = publication_div.find_all('a', class_='link person')
        authors = [author.text.strip() for author in authors_tags] if authors_tags else ["N/A"]


        year_tag = publication_div.find('span', class_='date')
        year = year_tag.text.strip() if year_tag else "N/A"

        publication_url_tag = publication_div.find('a', class_='title')
        publication_url = urljoin(base_url, publication_url_tag['href']) if publication_url_tag else "N/A"

        author_profile_url_tag = publication_div.find('a', class_='link person')
        author_profile_url = urljoin(base_url, author_profile_url_tag['href']) if author_profile_url_tag else "N/A"
        
        # Add data to the Whoosh index
        try:
            writer.add_document(title=title, authors=', '.join(authors), year=year,
                            publication_url=publication_url, author_profile_url=author_profile_url)
            
            # print(title, authors, year, publication_url, author_profile_url)

        except LockError as e:
            print(f"LockError: {e}")
            print("Attempting to clean up lock files...")

            # Manually clean up lock files
            lock_file_path = f"{index_path}/write.lock"

            try:
                os.remove(lock_file_path)
                print(f"Lock file {lock_file_path} removed.")
            except Exception as cleanup_error:
                return {
                    "success": False,
                    "error": "Error Fetching Data"
                }
    writer.commit()
    return {
        "success": True
    }

# Function to search the index
def search(query, index_path):
    ix = open_dir(index_path)
    finalResult = []
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        query_parser = QueryParser("title", ix.schema)
        query = query_parser.parse(query)
        results = searcher.search(query, terms=True)
        for result in results:
            finalResult.append({
                "title": result['title'],
                "Authors": result['authors'],
                "Year": result['year'],
                "publication_url": result['publication_url'],
                "profile_url": result['author_profile_url'],
            })

    return {
        "result": finalResult
    }

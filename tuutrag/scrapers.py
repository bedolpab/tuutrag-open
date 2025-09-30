# ================================================================
# path: tuutrag/scrapers.py
# brief: tuutrag module exports
# ================================================================
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


chrome_options = Options()
chrome_options.add_argument("--headless=new")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://ccsds.org/publications/magentabooks/")


html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# Retrieve all links within table data elements
links = [row.find("a")["href"] for row in soup.select("td:has(a)")]

# Filters links to retrieve wanted PDF links only
links = [link for link in links if "gravity_forms" in link]

# Remove duplicates
links = list(dict.fromkeys(links))


Magenta = []
for i in range(40):
    book = []

    # Retrieves table data for each book
    rows = soup.select(f'td[data-row-index="{i}"]')
    link = links[i]

    # Adds link data to list
    book.append(link)

    for row in rows:
        # Removes html from row data
        row = row.get_text(strip=True)

        # Adds rest of metadata to list
        book.append(row)

    # Removes empty elements in list
    book = list(filter(None, book))

    # Adds each book(metadata) to a list of books
    Magenta.append(book)

file = "Magenta_Books.csv"
headers = [
    "Book Type:",
    "Issue Number:",
    "PDF Name:",
    "Link:",
    "Title:",
    "Published Date:",
    "Description:",
    "Working Group:",
    "ISO Equivalent:",
]

# Creates a csv to store and organize books with metadata
with open(file, "w", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)

    # Loops through books within Magenta values
    # and organizes the elements to match the headers
    for idx, book in enumerate(Magenta):
        row = [
            book[3],  # Book Type
            book[4],  # Issue Number
            book[1],  # PDF Name
            book[0],  # Link
            book[2],  # Title
            book[5],  # Published Date
            book[6],  # Description
            book[7],  # Working Group
            book[8] if len(book) > 8 else "",  # ISO Equivalent
        ]

        writer.writerow(row)

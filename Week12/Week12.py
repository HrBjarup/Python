import bs4
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import re

# Assignment link:
# http://www.gutenberg.org/ebooks/search/?query=sherlock+holmes+conan

# -------------------------------------------
# -------------------- 1 --------------------
# -------------------------------------------
# Brug selenium til at gennemgå de 25 
# populæreste Sherlock Holmes bøger

def get_25_most_popular_books():
    URL = "http://www.gutenberg.org/ebooks/search/?query=sherlock+holmes+conan"
    browser = webdriver.Firefox()

    browser.get(URL)
    browser.implicitly_wait(1)
    books = []
    for index in range(25):
        book = browser.find_elements_by_class_name("booklink")[index]
        book.click()
        html_text_link = browser.find_elements_by_class_name("link")[0]
        html_text_link.click()
        page_source = browser.page_source
        books.append(page_source)
        sleep(0.2)
        browser.back()
        sleep(0.2)
        browser.back()
        #stopping after first book - remove break to run through all 25 books
        break
    browser.close()
    return books


# -------------------------------------------
# -------------------- 2 --------------------
# -------------------------------------------
# Brug regex til at finde alle afsnit der 
# indeholder £ tegn, samt det fulde beløb der nævnes

def find_all_sections_with_money(books):
    sections = []
    for book in books:
        soup = bs4.BeautifulSoup(book, "html.parser")
        for p in soup.find_all("p"):
            # Creating regex
            price = re.compile(r'(£(?:\s|.)\d*.\d*)')
            # Getting raw text from paragraph
            text = p.text
            # Finding all prices mentioned in text
            mo = price.findall(text)
            # Creating new array to hold modified prices
            prices = []
            # Looping through prices
            for item in mo:
                # Rinsing the string
                temp = item.replace("£", "")
                temp = temp.replace("\n", "")
                try:
                    # Regex is flawed and may pick up a price with a succeeding comma or dot
                    int(temp[-1])
                    # If the last character in the string is a number, then we're good
                    # Do nothing
                except:
                    # If the last character is not a number (cannot be parsed as int)
                    # then we remove the last character
                    temp = temp[0:-1]
                temp = temp.strip()
                # In case they write the price as £ 80 20s. 
                temp = temp.replace(" ", ".")
                # In case they write the price as £ 80,200. 
                temp = temp.replace(",", "")
                prices.append(float(temp))
            # Get the highest price at index 0
            if len(prices) > 0:
                prices.sort(reverse=True)
                money_count = len(prices)
                # If the text has a price mentioned more than once - the highest price will be taken
                sections.append((prices[0], text, money_count))
    sections.sort(key=lambda tup: tup[0], reverse=True)
    return sections

# -------------------------------------------
# -------------------- 3 --------------------
# -------------------------------------------
# Hvor mange gange nævnes konkrete beløber i £?
# Udskriv hele det afsnit hvor det højeste £ beløb nævnes

def get_money_count_and_paragraph_with_highest(result_list):
    counter = 0
    for element in result_list:
        counter += element[2]
    result = {}
    result["Amount of times £ is mentioned"] = counter
    result["Paragraph with biggest amount of £"] = result_list[0][1]
    return result

# Testing
books = get_25_most_popular_books()
result_list = find_all_sections_with_money(books)
final_result = get_money_count_and_paragraph_with_highest(result_list)
print(final_result)
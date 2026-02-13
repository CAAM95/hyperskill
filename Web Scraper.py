import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import string
import os

def get_the_soup(url):
    request = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(request.content, 'lxml')
    return soup

def get_base_url(url):
    parsed = urlparse(url)
    base_url = f"{parsed.scheme}://{parsed.netloc}"
    return base_url

def get_articles(soup, base_url, input_type):
    articles = soup.find_all('article')
    data = {}
    i = 0
    for article in articles:
        article_type = article.find('span', {'data-test': 'article.type'})
        if article_type.text == input_type:
            link = article.find('a', {'data-track-action': 'view article'})
            article_url = link["href"]
            full_url = base_url + article_url
            title = article.find('a', {'class': 'c-card__link u-link-inherit'}).text
            data[i] = {"url": full_url}
            i += 1
    return data

def find_content_for_articles(articles):
    for i, article in enumerate(articles):
        soup = get_the_soup(articles[i]["url"])
        title = find_article_title(soup)
        articles[i]["title"] = title
        content = find_article_content(soup)
        articles[i]["content"] = content
    return articles

def find_article_title(soup):
    title_tag = soup.find('h1', {'class': 'c-article-magazine-title'})
    title = title_tag.text if title_tag else ""
    return title

def find_article_content(soup):
    content = soup.find('p', {'class': 'article__teaser'})
    return content.text

def create_files(articles):
    for i, article in enumerate(articles):
        title = articles[i]['title']
        title = title.translate(str.maketrans("", "", string.punctuation))
        title = title.replace(" ", "_")
        with open(f"{title}.txt", 'wb') as file:
            file.write(articles[i]["content"].encode('utf-8'))

def find_articles_for_page_n_times(number_of_pages, url, article_type):
    soup = get_the_soup(url)
    base_url = get_base_url(url)
    next_page = None
    for i in range(int(number_of_pages)):
        if next_page:
            url = urljoin(base_url, next_page.get('href', ''))
            soup = get_the_soup(url)
            base_url = get_base_url(url)

        articles = get_articles(soup, base_url, article_type)
        articles = find_content_for_articles(articles)
        os.makedirs(f"Page_{i + 1}", exist_ok=True)
        os.chdir(f"Page_{i + 1}")
        create_files(articles)
        os.chdir('..')
        next_page = soup.find('a', rel='next') or soup.find('a', {'class': 'c-pagination__link'})

def main():
    number_of_pages = input()
    url = "https://www.nature.com/nature/articles?year=2020"
    article_type = input()
    find_articles_for_page_n_times(number_of_pages, url, article_type)

if __name__ == "__main__":
    main()

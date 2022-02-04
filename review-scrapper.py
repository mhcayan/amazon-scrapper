import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import uuid
import time
import random

SPLASH_SERVICE_URL = 'http://localhost:8050/render.html'
AMAZON_BASE_URL = 'https://www.amazon.com/'
AMAZON_REVIEW_URL = AMAZON_BASE_URL + 'product-reviews/'
PROGESS_COUNTER = 60

def getPage(url):
    retry_count = 3
    while retry_count:
        res = requests.get(SPLASH_SERVICE_URL, params={'url':url, 'wait':2})
        if res.status_code != 200:
            print(res.status_code)
            print(url)
            time.sleep(2 + random.randint(0,5))
            retry_count = retry_count - 1
            with open(str(uuid.uuid4()), 'w') as f:
                f.write(res.text)
            continue
        else:
            break
    return BeautifulSoup(res.text, 'html.parser')

def getReviews(soup, product_id):
    review_list = []
    reviews = soup.find_all('div', {'data-hook':'review'})
    for review in reviews:

        try:
            review_dict = {}
            review_dict['product_id'] = product_id
            title = review.find('a', {'data-hook':'review-title'})
            if not title:
                title = review.find('span', {'data-hook':'review-title'})
            review_dict['review_title'] = title.text.strip()
            review_dict['review_body'] = review.find('span', {'data-hook': 'review-body'}).text.strip()
            rating = review.find('i', {'data-hook':'review-star-rating'})
            if not rating:
                rating = review.find('i', {'data-hook':'cmps-review-star-rating'})
            rating_str = rating.text.strip()
            result = re.search(r'(\d+(.\d+)?)\D+(\d+(.\d+)?)\D*', rating_str)
            review_dict['rating'] = float(result.group(1))
            review_dict['rating_scale'] = float(result.group(3))
            review_dict['reviewer'] = review.find('span', {'class': 'a-profile-name'}).text.strip()
            location_date_str = review.find('span', {'data-hook': 'review-date'}).text.strip()
            result = re.search(r'Reviewed in( the)? (.*) on (.*)', location_date_str)
            review_dict['location'] = result.group(2)
            review_dict['date'] = result.group(3)
            review_dict['helpful_vote_count'] = 0
            try:
                helpful_vote = review.find('span', {'data-hook': 'helpful-vote-statement'})
                if helpful_vote:
                    result = re.search(r'(\S+)\s.*', helpful_vote.text.strip())
                    vote_count_str = result.group(1)
                    if vote_count_str.isdecimal():
                        review_dict['helpful_vote_count'] = int(vote_count_str)
                    else: #One helpful vote
                        review_dict['helpful_vote_count'] = 1
            except:
                print(helpful_vote.text)
            
            review_list.append(review_dict)
        except Exception as e:
            print(e)
            print(review.text)
            
    return review_list

def getNextPageUrl(soup):
    if soup.find('li', {'class': 'a-disabled a-last'}):
        return ''
    next_button = soup.find('li', {'class': 'a-last'})
    if next_button:
        next_button_link = next_button.find('a')
        if next_button_link:
            return AMAZON_BASE_URL + str(next_button_link['href'])
    return ''

def getProductReviewById(product_id):
    review_url = AMAZON_REVIEW_URL + product_id
    return getProductReviewByUrl(review_url, product_id)

def getProductReviewByUrl(review_url, product_id):

    all_review_list = []
    while review_url:
        print(review_url)
        soup = getPage(review_url)
        print(soup.title)
        review_list = getReviews(soup, product_id)
        all_review_list.extend(review_list)
        review_url = getNextPageUrl(soup)

    return all_review_list

PRODUCT_FILE_NAME = 'product.txt'

with open(PRODUCT_FILE_NAME) as file:
    all_review_list =[]
    for line in file:
        product_id = line.strip()
        if product_id:
            print("-----Fetching review of product: " + product_id + " -------")
            all_review_list.extend(getProductReviewById(product_id))

    df = pd.DataFrame(all_review_list)
    df.to_excel('reviews.xlsx', engine='xlsxwriter', index=False)

#print(len(getProductReviewByUrl("https://www.amazon.com/product-reviews/B096BKVWZZ/ref=cm_cr_getr_d_paging_btm_next_32?pageNumber=32", 'lskdjf')))
import requests
from bs4 import BeautifulSoup

medicine_images = []

getting_text = requests.get(f"https://www.arogga.com/brands?cat_id=13&page=1")
page = BeautifulSoup(getting_text.text, 'lxml')

print(page)

medName = page.find_all('div', class_='product__slider')

print(medName)
# print(medicine_images)

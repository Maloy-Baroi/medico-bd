import requests
from bs4 import BeautifulSoup

allPharmaInBangladesh = []
genericName = []
herbalGenericName = []
medicines = []

# for i in range(1, 7):
#     getting_text = requests.get(f"https://medex.com.bd/companies?page={i}")
#     a = BeautifulSoup(getting_text.text, 'lxml')
#
#     com = a.findAll('div', class_='data-row-top')
#     for elem in com:
#         allPharmaInBangladesh.append(elem.find('a').text)

# for i in range(1, 79):
#     getting_text = requests.get(f"https://medex.com.bd/generics?herbal={i}")
#     a = BeautifulSoup(getting_text.text, 'lxml')
#
#     com = a.findAll('div', class_='dcind-title')
#     for elem in com:
#         herbalGenericName.append(elem.text.strip())
#
# print(herbalGenericName)

for i in range(1, 20):
    getting_text = requests.get(f"https://medex.com.bd/brands?page={i}")
    a = BeautifulSoup(getting_text.text, 'lxml')

    medName = a.findAll('div', class_='data-row-top')
    powers = a.findAll('span', class_='grey-ligten')
    companyName = a.findAll('span', class_='data-row-company')
    prices = a.findAll('span', class_='package-pricing')
    for name, strength, company, unit_price in zip(medName, powers, companyName, prices):
        diction = [name.text.strip(), strength.text.strip(), company.text.strip(), unit_price.text.strip()]
        medicines.append(diction)
        # medicines.append(elem.text.strip())

print(medicines)

womenCare = []

getting_text = requests.get(f"https://www.arogga.com/brands?cat_id=20")
a = BeautifulSoup(getting_text.text, 'lxml')

medName = a.findAll('div', class_='data-row-top')
powers = a.findAll('span', class_='grey-ligten')
companyName = a.findAll('span', class_='data-row-company')
prices = a.findAll('span', class_='package-pricing')
for name, strength, company, unit_price in zip(medName, powers, companyName, prices):
    diction = [name.text.strip(), strength.text.strip(), company.text.strip(), unit_price.text.strip()]
    medicines.append(diction)

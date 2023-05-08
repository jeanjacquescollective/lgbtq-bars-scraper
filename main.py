import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from scrape import main
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import csv
app = FastAPI()
url = 'https://www.google.com/maps/'



origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument('--blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
driver.get(url)
try:
		cookiesDecliner = WebDriverWait(driver, timeout=1).until(lambda b: b.find_element(By.XPATH,"//button[@class='VfPpkd-LgbsSe VfPpkd-LgbsSe-OWXEXe-k8QpJ VfPpkd-LgbsSe-OWXEXe-dgl2Hf nCP5yc AjY5Oe DuMIQc LQeN7 Nc7WLe']"))
		cookiesDecliner.click()
except:
		pass

wijken = [
  "Binnenstad",
  "Bloemekenswijk",
  "Brugse Poort - Rooigem",
  "Gentse Kanaaldorpen en -zone",
  "Sint-Amandsberg",
  "Dampoort",
  "Drongen",
  "Elisabethbegijnhof - Prinsenhof - Papegaai - Sint-Michiels",
  "Gentbrugge",
  "Ledeberg",
  "Macharius - Heirnis",
  "Mariakerke",
  "Moscou - Vogelhoek",
  "Muide - Meulestede - Afrikalaan",
  "Nieuw Gent - UZ",
  "Oostakker",
  "Oud Gentbrugge",
  "Rabot - Blaisantvest",
  "Sint-Denijs-Westrem - Afsnee",
  "Sluizeken - Tolhuis - Ham",
  "Stationsbuurt-Noord",
  "Stationsbuurt-Zuid",
  "Watersportbaan - Ekkergem",
  "Wondelgem",
  "Zwijnaarde"
]

# wijken = [
#   "Binnenstad",
# ]

totaldata = {}
for wijk in wijken:
		print(wijk)
		amount = 100
		# amount = 5
		query = 'lgbtq bars ' + wijk + ' Gent'
		totaldata = {**totaldata, **main(driver, query, amount)}
		# query = 'bars ' + wijk + ' Gent'
		# totaldata = {**totaldata, **main(driver, query, amount)}

result = {}

for key,value in totaldata.items():
    if key not in result.keys():
        result[key] = value
os.remove('lgbtq-bars.csv') 
with open('lgbtq-bars.csv', 'a', newline='', encoding="utf8") as csvfile:
		writer = csv.writer(csvfile)
		for key, value in result.items():
			 writer.writerow([key, value])

def writeJson():
    with open('json/scrapedPages'+ '' + '.json', 'w', encoding='utf-8') as f:
        json.dump(totaldata, f, ensure_ascii=False, indent=4)
	
writeJson()
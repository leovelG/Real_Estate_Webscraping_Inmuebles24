from selenium import webdriver
import numpy as np 
import pandas as pd 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pathlib import Path  
'''
This program was developed by: @leovelG (Leonel Velázquez)
The program uses selenium to get the html code, it's important to download the chromedriver that corresponds to your operating system to do this you can visit
the following website:  https://sites.google.com/a/chromium.org/chromedriver/downloads 
It works creating a cycle that opens each of the pages available on the webpage inmuebles24.com 
it gets the information of each post saving the value of the property, the cost of the maintainance if existing, 
total area of the property, constructed area of the property, no. of rooms, bathrooms, parking and lastly the location

Currently the program works creating a csv for each of the pages visited, however this can be modified if wanted    

'''
for i in range(1):  #On this part you can select the number of pages you want to webscrapt 
	page_lov = 1+int(i)
	PATH = "C:\Program Files (x86)\chromedriver.exe" #
	driver = webdriver.Chrome(PATH)

	base_url = "https://www.inmuebles24.com/"
	location = "en-aguascalientes" #Here we can change the name of the city we're interested in 
	operation="en-venta-"
	page = "-pagina-{}".format(page_lov)
	url = base_url+str("inmuebles-")+operation+location+page+str(".html")

	driver.get(url)
	driver.implicitly_wait(10) #Waits for 5 seconds to load the page


	#postings_container = driver.find_elements(By.CLASS_NAME,"posting-card")

	columns = ['name']
	data = pd.DataFrame(columns=columns)
	postings=driver.find_elements(By.XPATH,".//div[@class='components__CardContainer-sc-1tt2vbg-3 cAFdld']") 


	value=[]
	man_cost = []
	sell_price = []
	total_area = []
	const_area = []
	bathrooms = []
	parkings = []
	rooms = []
	location = []

	c=1
	for posting in postings:
		
		value = posting.text
		value = value.splitlines()
		value= np.array(value)
		k=0
		bathrooms.append(int(0))
		parkings.append(int(0))
		rooms.append(int(0))
		sell_price.append(int(0))
		man_cost.append(int(0))
		location.append(str('N/A'))
		total_area.append(int(0))
		const_area.append(int(0))


		for i in range(len(value)):
			#print(value[i])
			if i<=3 and len(value[i].split()) >= 1 and len(value[i].split()) < 15 and not(str(value[i]).startswith('MN')) and not(str(value[i]).endswith('m²')):
				location[c-1] = str(value[i])

			if str(value[i]).startswith('MN'):

				price = int(value[i].replace('MN','').replace(' ','').replace(',','').replace('Mantenimiento',''))
				if price>10000:
					sell_price[c-1] = price
				else:
					man_cost[c-1]=price

			if str(value[i]).endswith('m²'):
				l=0
				if str(value[i]).endswith('m²') and k==0 :
					area = int(value[i].replace('m²','').replace(' ',''))
					total_area[c-1] = area
					const_area[c-1] = int(0)	
					k=1

				elif k==1:
					area = int(value[i].replace('m²','').replace(' ',''))
					const_area[l-1] = area
				l=l+1

			if str(value[i]).endswith('ha'):
				l=0
				if str(value[i]).endswith('ha') and k==0 :
					area = int(value[i].replace('ha','').replace(' ',''))
					total_area[c-1] = area
					const_area[c-1] = int(0)	
					k=1
					
				elif k==1:
					area = int(value[i].replace('ha','').replace(' ',''))
					const_area[l-1] = area
				l=l+1

			if str(value[i]).endswith('baños') or str(value[i]).endswith('baño') and len(str(value[i]))<4:
				bathrooms[c-1] = int(value[i].replace('baños','').replace(' ','').replace('baño',''))

			if str(value[i]).endswith('estac.'):
				parkings[c-1] = int(value[i].replace('estac.','').replace(' ',''))

			if str(value[i]).endswith('rec.'):
				rooms[c-1] = int(value[i].replace('rec.','').replace(' ',''))
		c=c+1		


	array = np.column_stack((sell_price, man_cost, total_area, const_area, rooms, bathrooms, parkings, location))
 
	res = pd.DataFrame(data=array, columns=['Price','Mantainance_cost', 'Total_area [m^2]', 'Constructed_area[m^2]', 'No_rooms', 'No_bathrooms', 'No_parkings', 'Location'])
	file_name = 'C://Users//Oswaldo//Documents//Leonel//Leo//Master//Webscraping//res{}.csv'.format(page_lov)
	res.to_csv(file_name, encoding='utf-8')
	driver.quit()
import pandas as pd 

li = []
for i in range(117):
	page_loc = 1+int(i)
	loc = "res{}.csv".format(page_loc)
	df = pd.read_csv("C://Users//Oswaldo//Documents//Leonel//Leo//Master//Webscraping//{}".format(loc))
	li.append(df)

frame = pd.concat(li, axis = 0, ignore_index = True)

file_name = 'C://Users//Oswaldo//Documents//Leonel//Leo//Master//Webscraping//Inmuebles24_Aguascalientes.csv'
frame.to_csv(file_name)

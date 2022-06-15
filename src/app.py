# your app code here
# your app code here
import pandas as pd
import requests
import sqlite3

from bs4 import BeautifulSoup

url = " https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue"
html_data = requests.get(url).text #convertimos a texto lo q viene
#print(html_data)

soup = BeautifulSoup(html_data,"html.parser")

tables = soup.find_all('table') #busca la data en las tablas, buscamos el tag html <table>

for index,table in enumerate(tables):
    if ("Tesla Quarterly Revenue" in str(table)):
        table_index = index

#create a dataframe
Tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])

for row in tables[table_index].tbody.find_all("tr"):
    col = row.find_all("td")
    if (col != []):
        Date = col[0].text
        Revenue = col[1].text.replace("$", "").replace(",", "")
        Tesla_revenue = Tesla_revenue.append({"Date":Date, "Revenue":Revenue}, ignore_index=True)

Tesla_revenue = Tesla_revenue[Tesla_revenue['Revenue'] != ""] #limpiamos los rows, sacamos los vacios

#print(Tesla_revenue)

records = Tesla_revenue.to_records(index=False)

print(f"hay estos records :{len(records)}")

list_of_tuples = list(records)

#print(list_of_tuples)

#esta data ahora la grabo en la bd

connection = sqlite3.connect('Tesla.db') #la bd

c = connection.cursor() #cursor

# Create table
c.execute('''
        CREATE TABLE IF NOT EXISTS revenue
        (Date, Revenue)'''
        )

c.executemany('INSERT INTO revenue VALUES (?,?)', list_of_tuples)
# Save (commit) the changes
connection.commit() # manda el comit a la conexion de la bd, no se manda el cursor

for row in c.execute('SELECT * FROM revenue'):
    print(row)

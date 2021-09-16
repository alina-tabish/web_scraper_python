import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import re   
import urllib
import pandas as pd  


#let user enter their query
query=input("enter query: ")
print("googling...")


query = urllib.parse.quote_plus(query) # Format into URL encoding
num_of_results = 20
ua = UserAgent()

google_url = "https://www.google.com/search?q=" + query + "&num=" + str(num_of_results)
response = requests.get(google_url, {"User-Agent": ua.random})
soup = BeautifulSoup(response.text, "html.parser")

result_div = soup.find_all('div', attrs = {'class': 'ZINbbc'})

links = []
titles = []
descriptions = []
for r in result_div:
    # Checks if each element is present, else, raise exception
    try:
        link = r.find('a', href = True)
        title = r.find('div', attrs={'class':'vvjwJb'}).get_text()
        description = r.find('div', attrs={'class':'s3v9rd'}).get_text()
        
        # Check to make sure everything is present before appending
        if link != '' and title != '' and description != '': 
            links.append(link['href'])
            titles.append(title)
            descriptions.append(description)

    # Next loop if one element is not present
    except:
        continue

to_remove = []
clean_links = []
for i, l in enumerate(links):
    clean = re.search('\/url\?q\=(.*)\&sa',l)

    # Anything that doesn't fit the above pattern will be removed
    if clean is None:
        to_remove.append(i)
        continue
    clean_links.append(clean.group(1))

# Remove the corresponding titles & descriptions
for x in to_remove:
    del titles[x]
    del descriptions[x]

#print(clean_links)
#print(titles)
#print(descriptions)


# saving the results in a file
# dictionary of lists  
dict = {'Name': titles, 'Desc': descriptions, 'Links': clean_links}  
       
df = pd.DataFrame(dict) 

file_name=input("Enter file name with format: ") 

# saving the dataframe 
df.to_csv(file_name) 

print("results saved successfully")
from bs4 import BeautifulSoup as soup
import requests


#Base URL
base_url = 'https://github.com'

#Credentials
login_url = base_url+'/session'
username = '<Your Github Username>'
password = '<Your Github Password>'

# Search Parameters
search_url = base_url+'/search'
language = 'c#'
search = 'UXDivers.Artina'
type = 'code'
allign = 'desc'
sort = 'indexed'

# Others
selected_projects = list()
with requests.Session() as session:
    loginResponse = session.get(login_url)
    login_html = loginResponse.text
    login_soup = soup(login_html,"html.parser")
    loginInputs = login_soup.find_all("input")
    token = loginInputs[1]["value"]
    payload = {'commit':'Sign in','utf8': '✓','authenticity_token': token,'login':username,'password':password}
    res = session.post(login_url,data = payload, headers = dict(referer=login_url))
    if(res.status_code == 200):
       unique_links = list()
       for i in range(1,2):
           params = {'l': language,
                     'o': allign,
                     'p': i,
                     'q': search,
                     's': sort,
                     'type': type}
           res = session.get(search_url,params = params)
           search_soup = soup(res.text,"html.parser")
           links = search_soup.find_all("a" , {"class" : "text-bold"})
           for link in links:
               name = link["href"]
               if name not in unique_links:
                   unique_links.append(name)
                   print(name)
           print(unique_links)
           packages = list()
           selected_links = list()
           #link = unique_links[3]
           for link in unique_links:
               res = session.get(base_url+link)
               link_soup = soup(res.text,"html.parser")
               files_folders = link_soup.find_all("a",{"class":"js-navigation-open"}) 
               folders = list()
               for file in files_folders:
                   url = file["href"]
                   if not (url.endswith(".md")):
                       if not (url.endswith(".sln")):
                           if not (url.endswith(".gitignore")):
                                folders.append(url)
                                print(url)
               for folder in folders:
                   res = session.get(base_url+folder)
                   files_soup = soup(res.text,"html.parser")
                   files = files_soup.find_all("a",{"class":"js-navigation-open"})
                   for file in files:
                      url = file["href"]
                      if(url.endswith("packages.config")):
                         print(url)
                         res = session.get(base_url+url)
                         package_soup = soup(res.text,"html.parser")
                         ids = package_soup.find_all("span",{"class":"pl-s"})
                         library = search.lower()
                         #id = ids[113]
                         for id in ids:
                             name = id.text.lower()
                             #if(name.startswith(library)):
                             if library in name:
                                 print(id)
                                 if link not in selected_projects:
                                   selected_projects.append(link)
                                   break;
                         #packages.append(url)
       print(selected_projects)
filename="products.csv"
f=open(filename, "w")
headers="Projects , Link , Contain\n"
f.write(headers)
for link in unique_links:
    if link in selected_projects:
        f.write(link.split('/')[1] + "," + base_url+link + "," + "True" + "\n")
    else:
        f.write(link.split('/')[1] + "," + base_url+link + "," + "False" + "\n")   
input("End") 
#uClient = uReq(my_url)
#page_html= uClient.read()
#uClient.close()
#myToken = 'fdf1b5fe31332384dd5030ec959d1a5037322fb8'
#head = {'Authorization': 'token {}'.format(myToken)}
#res = requests.get(my_url, headers=head)
#page_html = res.text
#print(page_html)
#page_soup=soup(page_html , "html.parser")
#containers = page_soup.find_all("div" , {"class" : "col _2-gKeQ"})
##print(len(containers))
##print (soup.prettify(containers[0]))
#container = containers[0]
##print (container.div.img["alt"])
#price = container.findAll("div" , {"class" : "col col-5-12 _2o7WAb"})
##print (price[0].text)
#ratings= container.findAll("div" , {"class" : "niH0FQ"})
##print (ratings[0].text)
#filename="products.csv"
#f=open(filename, "w")
#headers="ProductName , Pricing , Ratings\n"
#f.write(headers)
#for container in containers:
#  product_name = container.div.img["alt"]
#  price_container = container.findAll("div" , {"class" : "col col-5-12 _2o7WAb"})
#  price= price_container[0].text.strip()
#  rating_container= container.findAll("div" , {"class" : "niH0FQ"})
#  rating=rating_container[0].text
#  # print("product_name:" + product_name )
#  # print("price:" + price )
#  # print("Ratings:" + rating )

#  #String Parsing
#  trim_price = ''.join(price.split(','))
#  rm_rupee = trim_price.split("₹")
#  add_rs_price= "Rs." + rm_rupee[1]
#  split_price = add_rs_price.split('E')
#  final_price = split_price[0]
#  split_rating = rating.split(" ")
#  final_rating = split_rating[0]
#  print (product_name.replace(",", "|") + "," + final_price + "," + final_rating + "\n")
#  f.write(product_name.replace(",", "|") + "," + final_price + "," + final_rating + "\n")
#f.close()
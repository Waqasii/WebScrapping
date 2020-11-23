from requests import get
from bs4 import BeautifulSoup
import pandas as pd

class RealiticaScrapper:
    
    def __init__(self,start_link):
        self.current_link=start_link
        self.visited_link=[]
        self.df = pd.DataFrame(columns=['Title','Type','District','Location','Address','Energy Label','Price','Year Built','Bedrooms','Baths','Living Area','Land Area','Parking Spots','From Shore (m)','Link'])
        print('Scrapping Start')
        # try:
        self.getInfo()
        # except:
        self.df.to_excel("output.xlsx") 
            
            
    def insert(self,row):
        insert_loc = self.df.index.max()

        if pd.isna(insert_loc):
            self.df.loc[0] = row
        else:
            self.df.loc[insert_loc + 1] = row
            
    def getColm(self,box):
        colms=[]
        colm_need=['Type','District','New Construction','Air Conditioning','Location','Address','Energy Label','Price','Year Built','Bedrooms','Baths','Living Area','Land Area','Parking Spots','From Shore (m)']
        
        #list split by :
        colms=box.split(':')
        
        result=[]
        result.append(colms[0])
        for i in range(1,len(colms)-1):
            two_str=str(colms[i])
            split_str=str(colm_need[self.getSplit(two_str,colm_need)])
            temp=two_str.split(split_str)
            
            result.append(temp[0])
            result.append(split_str)
        result.append(colms[len(colms)-1])
            
        
        return result

    def getInfo(self):
        if(self.current_link not in self.visited_link):
            self.visited_link.append(self.current_link)
            print(self.current_link)
            response = get(self.current_link)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            total_places=html_soup.find_all('div' , attrs={'class': None, 'id':None, 'style':None})
            
            # print('Total House On This Page:',len(total_places))
            
            
            for place in total_places:
                
                #get link of each house
                link=place.find('a')['href']
                # print(link)
                
                home_info=get(link)
                soup_data=BeautifulSoup(home_info.text, 'html.parser')
                data=str(soup_data.find("div", {"id": "listing_body"}).text)
                info=data[0:data.find('Description')].split("\n")
                info=[i for i in info if i] 
                #variables for files
                house_name=info[0]
                info_box=info[1]
                
                # print('-------------------------')
                # print(house_name)
                # print(info_box)
                result=self.getColm(info_box)
                last_num=self.checkLast(result[len(result)-1])
                result[len(result)-1]=last_num
                #create row of result to insert in dataframe
                df_row=self.createRow(result)
                #insert link of house
                df_row.append(link)
                df_row.insert(0,house_name)
                self.insert(df_row)
                
                # print(result)
                # print('-------------------------')
                # for i in range(0,len(result)-1,2):
                #     print(result[i]+':'+result[i+1])
                # print('-------------------------')
                
            # get next link
            try:   
                self.current_link=self.getNextLink(self.current_link)
            except:
                return
        else:
            print('Scrapping Completed')
            print('Visited Links:',len(self.visited_link))
            return
          
        self.getInfo()
    
    def createRow(self,result):
        colm_names=['Type','District','Location','Address','Energy Label','Price','Year Built','Bedrooms','Baths','Living Area','Land Area','Parking Spots','From Shore (m)']
        row=[]
        for i in range(0,len(colm_names)):
            colm=colm_names[i]
            try:
                index=result.index(colm)
                value=result[index+1]
            except:
                value='N/A'
            row.append(value)
        return row
        
    def checkLast(self,string):
        import re
        m = re.search(r"\d", string)
        if m is not None:
            start_index=m.start()
            m=re.search(r'(\d)[^\d]*$',string)
            last_index=m.start()+1
            # print(string)
            string=string[start_index:last_index]
        else:
            pass

        # print(string)

        return string

    def getSplit(self,two_str,store_str):
        for check in store_str:
            if(check in two_str):
                # print(store_str.index(check))
                return store_str.index(check)
            
    def getNextLink(self,link):
        response = get(link)
        html_soup = BeautifulSoup(response.text, 'html.parser')
        link=html_soup.find_all('a' , class_="bt_pages")[-1]['href']
        return link
    
      

    
    
        


#Main Page URL
start_link = 'https://www.realitica.com/?cur_page=0&for=Prodaja&pZpa=Crna+Gora&pState=Crna+Gora&type%5B%5D=Home&lng=en'

#Run Program
RealiticaScrapper(start_link)



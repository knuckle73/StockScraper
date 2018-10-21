import time
import easygui as eg  # http://www.ferg.org/easygui/easygui.html#-buttonbox
import os
from requests_html import HTMLSession
session = HTMLSession()
import urllib.error
#from progressbar import Bar
    
cdate = time.strftime("%m" + "_" + "%d" + "_" + "%y")


site = 'https://finance.google.com/finance?q='
symbols = []
output = [['Company Name','Last Price','DIV/Yield','Change']]

def Get_Qoute():

    GetSyms()

    for S in symbols:
        
        if S != '':
            url = site + S
            # print("Looking up " + S)
            
            try:
            
                print(url)
                r = session.get(url)

                #Get Company Name
                company = r.html.find(".kno-fb-ctx")
                if company:  #Check for data.
                    name = company[0].text.strip()
                    print("Looking up:  " + name + "\n")
                                    #Get current price of stock
                    price = r.html.find('.IsqQVc.NprOob', first=True).text
                    if price:  #Check for data.
                        P = price
                    else:
                        P = 'Unavailable'

                    #Get current dividen / yield.
                    div = r.html.find(".ZSM8k")[1].text.split("\n")[1]
                    if div != None and S != 'INDEXDJX:.DJI':  #Check for data.
                        D = div
                    else:
                        D = 'None'
                        
                    #Get amount of change dollar and percentage
                    change = r.html.find('.WlRRw.IsqQVc')[0].text
                    
                    if change:                      #Check for data.
                        C = change
                    else:
                        C = 'None'
                    
                    qoute = [(name + '  [' + S + ']'),P,D,C]  # Create list item for current qoute.
                    #print((name + '  [' + S + ']'),P,D,C)
                else:
                    name = "NULL"
                    print("Symbol " + S + " not found.")
                    qoute = [("Unable to find symbol:" + '  [' + S + ']'),"","",""] 
                
             
            except NameError:
                print("Oops: Symbol " + s + " not found.")
                qoute = [("Unable to find symbol:" + '  [' + S + ']'),"","",""] 
            except urllib.error.HTTPError:
                print("Invalid symbol or market\n")
                
            output.append(qoute)  # Append each qoute to the global output list.

def GetSyms():      # function opens the symboles file ant populates the symbols  list.
    f = open('C:\Stocks\symbolfile.txt', 'r')
    syms = f.readlines()   
    f.close()
    for t in syms:
        symbols.append(t.rstrip('\n'))

if __name__ == "__main__":

    #reply = eg.indexbox(msg='Select Option', title='MyPy Stock Reporter', choices=('Run Report','Edit Stocks'), image=None)

    #if reply == 1:
    #   os.system("start " + 'C:\Stocks\symbolfile.txt')    # This simply opens the text file of stock tickers inorder to edit it.
  
    #else:
    # Indent removed for code below. Above code disabled for simplicity
    fo = open('C:\\Stocks\\StockPrices' + cdate + '.txt', 'w', encoding='utf-8')

    Get_Qoute()
    
    header = "\n| " + output[0][0] + " "*(48-len(output[0][0])) + "| " + output[0][1] + " "*(10-len(output[0][1])) + " | " + output[0][2] + " "*(9-len(output[0][2])) + " | " + output[0][3] + "\n|" + "-"*90 + "\n"
    #header = ("\n| ",output[0][0]," "*(48-len(output[0][0])),"| ",output[0][1]," "*(10-len(output[0][1]))," | ",output[0][2]," "*(9-len(output[0][2]))," | ",output[0][3],"\n|","-"*90,"\n")
    fo.write(header)
    #print(header)
    for q in output[1:]:
        line = "| " + q[0] + " "*(48-len(q[0])) + "| " + q[1] + " "*(10-len(q[1])) + " | " + q[2] + " "*(9-len(q[2])) + " | " + q[3] + "\n"
        #line = "| ",q[0]," "*(48-len(q[0])),"| ",q[1]," "*(10-len(q[1]))," | ",q[2]," "*(9-len(q[2]))," | ",q[3],"\n"
        fo.write(line)
        #print(line)

    fo.close()

    eg.msgbox("Report Complete!", title="Report")
    os.system("start " + 'C:\\stocks\\StockPrices' + cdate + '.txt')

        


# http://chartapi.finance.yahoo.com/instrument/1.0/XOM/chartdata;type=quote;range=0d/csv

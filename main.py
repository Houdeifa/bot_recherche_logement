import pyautogui
import time
import pathlib
import pyperclip
import os
from parsel import Selector
import re
import sys
import csv
import datetime;

#open the search page firefox


OS_Name = "Linux" # Linux or Windows
Browser = "FireFox" # FireFox or Chrome (doesn't work perfectly with chrome)
WorkAdress = "12 Rue Jules Horowitz, 38019 Grenoble"

def execute_sript(scriptToPast,secondScript="",closeConsole=False): 
    #open console
    global Browser
    if Browser == "FireFox":
        pyautogui.keyDown("ctrl")
        pyautogui.keyDown("shift")
        pyautogui.press("k")
        pyautogui.keyUp("ctrl")
        pyautogui.keyUp("shift")
    elif Browser == "Chrome":
        pyautogui.press("f12")
    time.sleep(3)
    pyperclip.copy(scriptToPast)
    if Browser == "Chrome":
        # pyautogui.press("tab")
        # time.sleep(1)
        pass
    pyautogui.keyDown('ctrl')
    pyautogui.press("v")
    pyautogui.keyUp('ctrl')
    #execute past script
    pyautogui.keyDown("ctrl")
    pyautogui.press("enter")
    pyautogui.keyUp('ctrl')
    time.sleep(3)

    if secondScript != "":
        if Browser == "FireFox":
            #select old script
            pyautogui.keyDown("ctrl")
            pyautogui.press("a")
            pyautogui.keyUp('ctrl')
        #newscript :
        pyperclip.copy(secondScript)
        pyautogui.keyDown('ctrl')
        pyautogui.press("v")
        pyautogui.keyUp('ctrl')

        #execute past script
        pyautogui.keyDown("ctrl")
        pyautogui.press("enter")
        pyautogui.keyUp('ctrl')

    if Browser == "FireFox":
        #close console
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        pyautogui.keyUp('alt')
    elif Browser == "Chrome" and closeConsole == True:
        #close console
        pyautogui.keyDown("alt")
        pyautogui.press("f4")
        pyautogui.keyUp('alt')
    time.sleep(3)

def save_html_file():
    #save the html file to current dir
    try:
        os.remove("tmp.html") 
    except:
        print("no tmp.html found to delete (not a big problem)") 
    pyautogui.keyDown('ctrl')
    pyautogui.press("s")
    pyautogui.keyUp('ctrl')
    time.sleep(3)
    if(OS_Name == "Linux"):
    	s = str(pathlib.Path().absolute()) + "/tmp"
    else:
    	s = str(pathlib.Path().absolute()) + "\\tmp.html"
    pyperclip.copy(s)
    pyautogui.keyDown('ctrl')
    pyautogui.press("v")
    pyautogui.keyUp('ctrl')
    time.sleep(0.5)
    pyautogui.press("enter")

def waitForFile(fileName,time_out_s):
    timeout = time.time() + time_out_s
    canOpen = False
    while(time.time() < timeout and os.path.exists("tmp.html") == False ):
        time.sleep(1)
pagesNumer = 1
link = "https://www.seloger.com/list.htm?projects=1&types=2,1&places=[{%22inseeCodes%22:[380185]}]&price=NaN/550&sort=a_sqr_meter_price&mandatorycommodities=0&enterprise=0&qsVersion=1.0&m=search_refine-redirection-search_results"
if OS_Name == "Linux":
    os.system("firefox-esr --new-window \"" + link + "\" &")
    #wait to launch
<<<<<<< HEAD
    time.sleep(5)
=======
    time.sleep(7)
>>>>>>> ddc44c8 (TMP)
    save_html_file()
    waitForFile("tmp.html",30)
    try :
        f = open("tmp.html", "r",encoding="utf8")
        htmlText = f.read()
        sel = Selector(htmlText)
        f.close()
        aElms = sel.xpath("//a[@aria-label=\"Aller à la page 1\"]").get()
        classRE = re.search("(?<=class=[\"])[a-zA-Z0-9-_ ]+(?=[\"])", aElms)
        if classRE:
            aClass = str(classRE.group(0))
            aClass  = aClass.split(" ")[0]
            aElms = sel.css(aClass).getall()
            pagesNumer = len(aElms)
            print("pagesNumer = " + str(pagesNumer))
    except Exception as error:
        print(str(error) + " => error : couldn't extract pages number !")

    time.sleep(1)
    pyautogui.keyDown('alt')
    pyautogui.press("f4")
    pyautogui.keyUp('alt')
    time.sleep(1)

extractedInfos = []
for page in range(1,pagesNumer+1):
    link = "https://www.seloger.com/list.htm?projects=1&types=2%2C1&places=%5B%7B%22inseeCodes%22%3A%5B380185%5D%7D%5D&price=NaN%2F550&sort=a_sqr_meter_price&mandatorycommodities=0&enterprise=0&qsVersion=1.0&LISTING-LISTpg=" + str(page)

    if OS_Name == "Linux":
        os.system("firefox-esr --new-window \"" + link + "\" &")

    time.sleep(5)

    save_html_file()
    aClass = ""
    numberOfUrls = 0
    htmlText = ""
    waitForFile("tmp.html",30)
    try :
        f = open("tmp.html", "r",encoding="utf8")
        htmlText = f.read()
        sel = Selector(htmlText)
        f.close() 
        classElementText = sel.xpath("/html/body/div[3]/div/div[3]/div[2]/div[1]/div[" + str(3) + "]/a").get()
        classRE = re.search("(?<=class=[\"])[a-zA-Z0-9-_ ]+(?=[\"])", classElementText)
        if classRE:
            aClass = str(classRE.group(0))
            print("class = " + str(classRE.group(0)))
            aElms = sel.xpath("//a[@class=\"" + aClass +"\"]").getall()
            numberOfUrls = len(aElms)
            print("numberOfUrls = " + str(numberOfUrls))
    except :
        print("no tmp.html found !") 

    if (numberOfUrls == 0 or aClass == ""):
        sys.exit()
    sel = Selector(htmlText)
    aElms = sel.xpath("//a[@class=\"" + aClass +"\"]").getall()
    for i in range(numberOfUrls):
        infos = []
        hrefRE = re.search(r"<a\s+(?:[^>]*?\s+)?href=([\"'])(.*?)\1", aElms[i])
        print("i = " + str(i) + " of " + str(numberOfUrls))
        if hrefRE:
            print("link = " + str(hrefRE.group(2)))
            infos.append(str(hrefRE.group(2)))
        else:
            infos.append("NO_URL")
        execute_sript("document.getElementsByClassName(\"" + aClass + "\")[" + str(i) +"].click()")
        
        save_html_file()
        locationClass = ""
        waitForFile("tmp.html",30)
        try :
            f = open("tmp.html", "r",encoding="utf8")
            sel = Selector(f.read())
            f.close()
            PriceElementText = sel.xpath("/html/body/div[2]/div/main/div[2]/div/div[1]/div[1]/div[2]/div/div[2]/div[1]/div/span/span[1]").get()
            classElementParent = sel.xpath("/html/body/div[2]/div/main/div[2]/div/div[1]").get()
            infoElementText    = sel.xpath("/html/body/div[2]/div/main/div[2]/div/div[1]/div[1]/div[2]/div/div[1]/div[2]").get()
            neighborhoodElementText = sel.xpath("/html/body/div[2]/div/main/div[2]/div/div[1]/div[2]/p/span[1]")
            heatElementText = sel.xpath("/html/body/div[2]/div/main/div[2]/div/div[1]/section[1]/div[3]/div/div/div[1]/div/div[2]")
            calcMessage = "Calculer un temps de trajet"
            calcMessageIndex = classElementParent.index(calcMessage)
            classElementText = classElementParent[calcMessageIndex-61:calcMessageIndex+len(calcMessage)]
            classRE = re.search("(?<=class=[\"])[a-zA-Z0-9-_ ]+(?=[\"])", classElementText)
            PriceRE = re.search("([0-9]+[ ]*)+€", PriceElementText)
            RoomsN1RE = re.search("[0-9] pièces*", infoElementText)
            RoomsN2RE = re.search("[0-9] chambres*", infoElementText)
            AreaRE = re.search("[0-9]+ m²", infoElementText)
            neighborhood = ''.join(neighborhoodElementText.css('::text').getall())
            heatText = ''.join(heatElementText.css('::text').getall())
            p = 0
            a = 0
            if PriceRE:
                Price = str(PriceRE.group(0)).replace(" ","").replace("€","")
                infos.append(Price)
                p = int(Price)
            else:
                infos.append("NOT_MENTIONNED")

            if AreaRE:
                Area = str(AreaRE.group(0)).replace(" ","").replace("m²","")
                infos.append(Area)
                a = int(Area)
            else:
                infos.append("NOT_MENTIONNED")

            if PriceRE and AreaRE and a > 0:
                infos.append(str(p/a))
            else:
                infos.append("NOT_MENTIONNED")

            if(neighborhood == ""):
                infos.append("NOT_MENTIONNED")
            else:
                infos.append(neighborhood)

            if RoomsN1RE:
                infos.append(str(RoomsN1RE.group(0)))
            else:
                infos.append("NOT_MENTIONNED")

            if RoomsN2RE:
                infos.append(str(RoomsN2RE.group(0)))
            else:
                infos.append("NOT_MENTIONNED")

            if(heatText == ""):
                infos.append("NOT_MENTIONNED")
            else:
                infos.append(heatText)

            if classRE:
                locationClass = str(classRE.group(0))
        except Exception as error:
            print(str(error) + " => no tmp.html found !")
        if locationClass == "":
            #close tab
            pyautogui.keyDown('ctrl')
            pyautogui.press("w")
            pyautogui.keyUp('ctrl')
            continue
        time.sleep(3)
        s1_open_localisation = "document.getElementsByClassName(\"" + locationClass + "\")[1].click()"
        
        execute_sript(s1_open_localisation,closeConsole=True)

        save_html_file()
        inputClass = ""
        waitForFile("tmp.html",30)
        try :
            f = open("tmp.html", "r",encoding="utf8")
            sel = Selector(f.read())
            f.close() 
            classElementText = sel.xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/div/div[4]/div[5]/div/div[1]/label/div[2]/input").get()
            classRE = re.search("(?<=class=[\"])[a-zA-Z0-9-_ ]+(?=[\"])", classElementText)
            if classRE:
                inputClass = str(classRE.group(0))
                print("inputClass = " + str(classRE.group(0)))
        except :
            print("no tmp.html found !") 
        if inputClass == "":
            #close tab
            pyautogui.keyDown('ctrl')
            pyautogui.press("w")
            pyautogui.keyUp('ctrl')
            continue
        s2_focus_on_input = "document.getElementsByClassName(\"" + inputClass + "\")[0].focus()"
        if Browser == "Chrome":
            pyautogui.press("f2")
        execute_sript(s2_focus_on_input,closeConsole=True)
        pyautogui.write(WorkAdress)
        time.sleep(4)
        #choose the first address
        pyautogui.press("down")
        time.sleep(0.5)
        pyautogui.press("enter")
        time.sleep(7)

        save_html_file()

        waitForFile("tmp.html",30)
        #close tab
        pyautogui.keyDown('ctrl')
        pyautogui.press("w")
        pyautogui.keyUp('ctrl')

        try :
            f = open("tmp.html", "r",encoding="utf8")
            sel = Selector(f.read())
            f.close() 
            busTimeElementText = sel.xpath("/html/body/div[2]/div/div[3]/div/div/div[2]/div/div[4]/div[6]/span[4]").get()
            busTime = re.search("~[0-9]+ (min|h)", busTimeElementText)
            if busTime:
                print("busTime = " + str(busTime.group(0)))
                infos.append(str(busTime.group(0)))
            else:
                infos.append("NO_TIME")
        except :
            print("no tmp.html found !")
        extractedInfos.append(infos)

    pyautogui.keyDown('alt')
    pyautogui.press("f4")
    pyautogui.keyUp('alt')


# ct stores current time
ct = str(datetime.datetime.now()).replace(":","_").replace("-","_").replace(" ","_")

# open the file in the write mode
f = open('database_'+ct+'.csv', 'w')

# create the csv writer
writer = csv.writer(f)

# write a row to the csv file
writer.writerow(["URL","PRICE (m²)","AREA","PRICE/AREA (€/m²)","NEIGHBORHOOD","PIECES","BEDROOMS","HEAT","BUS TIME"])
for i in range(len(extractedInfos)):
    writer.writerow(extractedInfos[i])

# close the file
f.close()

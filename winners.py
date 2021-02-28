#!/usr/bin/python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import  bs4, time
import sys, os

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib


#SENDEREMAILADDRESS: the address you use to send the email (if it is a google account, you have to configure it in the security settings to allow external control of the account
#DESTINATIONEMAILADDRESS: the destination email address
#SERVER: the server email address. By default is configured for gmail account, but you can use your own
#PASSWORD_SENDEREMAILADDRESS: the password of the SENDEREMAILADDRESS
def sendMail(textToSend):
    fromaddr = "SENDEREMAILADDRESS"
    toaddr = "DESTINATIONEMAILADDRESS"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Equips primers"
    body = "Informacio dels equps primers de cada lliga:\n {}".format(textToSend)
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "PASSWORD_SENDEREMAILADDRESS")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()
    print("Correu enviat")


lliga=[]
primer_equip=[]
classificacio_final=[]
participants=[]
equips_avui=[]
partits_avui=[]


#You need to have the geckodriver or the chromedriver to configure the automatation of th web browser. You have to save the file to the c:\driver folder.(be sure the version is the same as your web browser version)
#driver = webdriver.Chrome(executable_path = "C:\\driver\\chromedriver")
driver = webdriver.Firefox(executable_path = "C:\\driver\\geckodriver.exe")

url = 'https://www.flashscore.com'

driver.get(url)

time.sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

cookies=driver.find_element_by_id("onetrust-accept-btn-handler").click()

classificacions=driver.find_elements_by_class_name("event__info")

mostra=[]

i=0
for c in classificacions:
    if "mostrar" in c.text:
        i=i+1
        mostra.append(c)

for i in range(0,len(mostra)):
    print(i)
    try:
        mostra[i].click()
    except:
        pos_act=driver.execute_script("return window.pageYOffset;");
        driver.execute_script("window.scrollTo({}, {})".format(pos_act+50,pos_act+50))
        mostra[i].click()



participant=driver.find_elements_by_class_name("event__participant")

for p in participant:
    try:
        participants.append(p.text.strip())
    except:
        pass

final_pagina=driver.execute_script("return document.documentElement.scrollHeight")

part=final_pagina/25
part1=part

classificacions=driver.find_elements_by_class_name("event__info")
classificats=[]
for c in classificacions:
    if "Clasifi" in c.text:
        classificats.append(c)

k=1
for c in classificats:
    #print(c.text)
    print("Iteration: ",k)
    window_principal=driver.window_handles[0]
    try:    
        #time.sleep(2)
        
        c.click()
        time.sleep(4)
        window_principal=driver.window_handles[0]
        print("Saltem a la finestra de la classificacio")
        window_class=driver.window_handles[1]
        driver.switch_to.window(window_class)
        print("Finestra actual: ",driver.title)
        positions=driver.find_elements_by_class_name("rowCellParticipantName___38vskiN")
        #del positions[0]
        print("Equip: ",positions[0].text.strip())
        print("Lliga: ",driver.title)
        primer_equip.append(positions[0].text.strip())
        lliga.append(driver.title)
        driver.close()
        driver.switch_to.window(window_principal)
    except:
        print("ERROR ACCESS")
        driver.close()
        driver.switch_to.window(window_principal)
        continue
    k=k+1

for p in primer_equip:
    for pa in participants:
        if p == pa:
            equips_avui.append(p)

sen=driver.find_elements_by_class_name("event__match")

for s in sen:
    for e in equips_avui:
        if e in s.text:
            partits_avui.append(s.text + "==>"+e)
            print(s.text + "==>"+e)

partits_avui.sort()

f3=open("partits_avui.txt","w")
for i in range(len(partits_avui)):
    f3.write("{}\n".format(partits_avui[i].replace("\n","")))

f3.close()

fitxer=open("partits_avui.txt","r")

text=fitxer.readlines()

fitxer.close()

textToSend=""

for t in text:
    textToSend=textToSend+t

sendMail(textToSend)

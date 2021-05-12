from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from bs4 import BeautifulSoup
import xlsxwriter
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://downtowndallas.com/experience/stay/")
sleep(1)

# remove ad
path2 = "/html/body/header"
element2 = driver.find_element_by_xpath(path2)
action2 = ActionChains(driver)
action2.click(on_element=element2)
action2.perform()

output = ''
imgurl = ''
output1 = ''
output2 = []
s = 2
# save data to csv
workbook = xlsxwriter.Workbook("ExtractData" + '.xlsx')
worksheet = workbook.add_worksheet()
bold = workbook.add_format({'bold': True})
worksheet.write('A1', 'NAME', bold)
worksheet.write('B1', 'Address', bold)
worksheet.write('C1', 'Phone', bold)
worksheet.write('D1', 'Area', bold)
worksheet.write('E1', 'ImageUrl', bold)

for i in range(1, 42):
    # open url

    sleep(1)
    t = str(i)
    print(t + " started")
    img = "hotel" + t + ".png"
    path = "/html/body/main/div/section[2]/div[" + t + "]/div[3]/a"
    element = driver.find_element_by_xpath(path)

    # save image and take url of img
    with open(img, 'wb') as file:

        path2 = "/html/body/main/div/section[2]/div[" + t + "]/div[1]/img"
        l = driver.find_element_by_xpath(path2)
        l.get_attribute('src')
        imgurl = l.get_attribute('src')
        print("Image Stored in project Folder ")
        print("Image Url "+l.get_attribute('src'))

        file.write(l.screenshot_as_png)

    # gather details
    action = ActionChains(driver)
    action.click(on_element=element)
    action.perform()
    sleep(1)
    get_url = driver.current_url
    sleep(1)

    # extract details
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    hotelname = soup.find('h1', class_="place-name")

    for data in soup.find_all('div', class_='place-content'):
        for a in data.find_all('a'):
            output2.append(a.text)

    name = hotelname.text
    sampleadress = str(output2[0])
    phone = str(output2[1])
    area = str(output2[2])

    # print details
    print("Hotel Name :-"+name)
    address = sampleadress.lstrip().rstrip()
    print("Address :-"+sampleadress.lstrip().rstrip())
    print("Phone Number :-"+phone)
    print("Area :-"+area)
    sleep(1)

    index = str(s)
    worksheet.write('A' + index, name)
    worksheet.write('B' + index, address)
    worksheet.write('C' + index, phone)
    worksheet.write('D' + index, area)
    worksheet.write('E' + index, imgurl)
    s = s + 1
    driver.back()
    # close the Excel file
workbook.close()

read_file = pd.read_excel("ExtractData.xlsx")
read_file.to_csv("HotelDataCSVFile.csv", index=None, header=True)

df = pd.DataFrame(pd.read_csv("HotelDataCSVFile.csv"))
gfg_csv_data = df.to_csv('HotelDataCSVFile.csv', index=True)
print(gfg_csv_data)

print("All data Extracted and Saved to HotelDataCSVFile.csv File in project Folder ")

#Code by Aki.no.Alice@Tyrant_Rex

from bs4 import BeautifulSoup
import requests,re,os

code = input("番號:")
while len(code) > 6:
    print("code error")
    code = input("番號:")

URL = f"https://nhentai.net/g/{code}"

ok = requests.get(URL)

if ok.status_code == 200:
    soup = BeautifulSoup(ok.text, "lxml")
    page = soup.find_all(src=re.compile("https://t.nhentai.net/galleries/"))
    trash = soup.find_all(src=re.compile("/thumb")) + soup.find_all(src=re.compile("/cover"))

    image_trash = [result.get("src") for result in trash]
    image = [result.get("src") for result in page]

    while len(image_trash) != 0:
        image.remove(image_trash[0])
        image_trash.remove(image_trash[0])
    try:
        os.makedirs(f"./{code}/")

        for link in image:
            url = link.replace("t.",".").replace("//","//i")
            name = url.replace("/","-")
            name = name.replace("https:--i.nhentai.net-galleries-","")
            name = name.replace(".png", ".jpg")
            img = requests.get(url)
            with open(f"./{code}/{name}", "wb") as f:
                f.write(img.content)
    except:
        print("folder already exists")

    print("DONE==>",code)
else:
    print("error",ok.status_code)
import requests
import traceback
from time import time
from bs4 import BeautifulSoup
from spider.services.image_service import ImageService
from flask_script import Command

index_url = "http://www.wwqun.com/m/"
base_img_url = "http://www.wwqun.com"


class SpiderScript(Command):

    def run(self):
        try:
            ImageService.delete_out_date_images()
            handler()
        except Exception:
            traceback.print_exc()


def find_class():

    resp = requests.get(index_url)

    a_li = []

    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')
        li = soup.find_all("tbody")
        tbody = li[0]
        li = tbody.find_all("a")

        for a_ele in li:

            strong_eles = a_ele.find_all("strong")

            if strong_eles:
                href = str(a_ele.get("href"))

                # if href.endswith("asp"):
                #     continue

                if "Product.asp" not in href:
                    continue

                strong = strong_eles[0]
                res = {
                    "url": href,
                    "name": str(strong.text).strip()
                }

                a_li.append(res)

    return a_li


def find_images(class_url, class_name, params=None):
    result = []
    retry_count = 0
    while retry_count <= 3:
        try:
            resp = requests.get(class_url, params=params, timeout=5)
            break
        except KeyboardInterrupt as e:
            raise e
        except Exception:
            retry_count += 1

    if retry_count > 3:
        return [], True
    # resp = requests.get(class_url, params=params)
    next_page = False
    if resp.status_code == 200:
        soup = BeautifulSoup(resp.text, 'lxml')
        li = soup.find_all("div", "goodslist")
        img_eles = li[0].find_all("img")
        for img in img_eles:
            url = base_img_url + img.get("src")
            result.append({
                "name": img.get("alt"),
                "url": url
            })

        page = soup.find("div", "page")
        if page:
            a_li = page.find_all("a")
            for a in a_li:
                if a.text == "下一页":
                    next_page = True
                    break

    return result, next_page


def handler():

    class_li = find_class()
    for class_info in class_li:
        print(class_info)
        result = []
        page = 1
        flag = True
        while flag:
            if page > 40:
                flag = False
                break
            start_time = time()
            imgs, flag = find_images(class_info["url"], class_info["name"], {"page": page})
            end_time = time()
            print(end_time - start_time, page)
            for img in imgs:
                result.append({
                    "class_name": class_info["name"],
                    "url": img["url"],
                    "name": img["name"]
                })
            page += 1

        print(len(result))
        for i in range(len(result)-1, -1, -1):

            image = result[i]
            if ImageService.check_url(class_info["name"], image["url"]):
                ImageService.create(image["name"], class_info["name"], image["url"], i)
            else:
                ImageService.update_index(class_info["name"], image["url"], i)


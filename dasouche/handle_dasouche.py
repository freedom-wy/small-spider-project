import requests
import json
import re
import pymongo
from pymongo.collection import Collection
from concurrent.futures.thread import ThreadPoolExecutor


class HandleDaSouChe(object):
    def __init__(self):
        #页码请求URL
        self.page_url = "https://aolai.souche.com/v1/searchApi/searchCar.json?_security_token=undefined"
        self.header = {
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
        }
        self.item_url_list = []
        mongo_client = pymongo.MongoClient(host="10.70.120.156", port=27017)
        self.db_data = mongo_client['oreo']

    def handle_save_data(self,item):
        db_collection = Collection(self.db_data, 'dasouche_data')
        db_collection.update({'carId':item['carId']},item,True)

    def handle_page(self):
        for page in range(1,5):
            #构造请求数据POST,每页可现实500条数据，共4页
            data = {
                "keyword":"",
                "brandCode":"",
                "seriesCode":"",
                "price":"",
                "carModel":"",
                "carAge":"",
                "mileage":"",
                "gearboxType":"",
                "displacement":"",
                "emissionStandard":"",
                "bodyColor":"",
                "fuelType":"",
                "seatingCapacity":"",
                "drivingMode":"",
                "country":"",
                "pageNo":page,
                "pageSize":"500",
                "from":"pc",
                "cityCode":"",
                "shopCode":"",
                "sort":"newsOnShelf",
            }
            page_result = self.handle_request(method='POST',url=self.page_url,data=data)
            for item in json.loads(page_result)['data']['items']:
                self.item_url_list.append(item['detailUrl'])

    #处理详情页
    def handle_detail(self,url):
        id_search = re.compile(r"carId=(.*?)&shopCode=(\d+)")
        car_id = id_search.search(url).group(1)
        shop_id = id_search.search(url).group(2)
        #车辆详情信息
        car_detail_url = "https://aolai.souche.com//v1/carDetailsApi/carDetailInfo.json?carId=%s"%car_id
        car_detail = self.handle_request(method='GET',url=car_detail_url)
        car_detail_result = json.loads(car_detail)['data']
        #售卖商店信息
        shop_detail_url = "https://aolai.souche.com//v1/shopApi/queryTangecheShopInfo.json?carId=%s&citycode=%s&shopCode=%s"%(car_id,car_detail_result['baseCarInfoView']['cityCode'],shop_id)
        shop_detail_result = self.handle_request(method='GET',url=shop_detail_url)
        car_detail_result.update(json.loads(shop_detail_result)['data'])
        #车辆厂商配置信息
        car_config_url = "https://aolai.souche.com/v1/carDetailsApi/carConfigDetailInfo.json?_security_token=undefined&carId=%s"%car_id
        car_config_result = self.handle_request(method='GET',url=car_config_url)
        car_detail_result.update(json.loads(car_config_result)['data'])
        car_detail_result['from_url'] = url
        self.handle_save_data(car_detail_result)



    def handle_request(self,method,url,data=None):
        if method == 'POST':
            response = requests.post(url=url,headers=self.header,data=data)
            return response.text
        elif method == 'GET':
            response = requests.get(url=url,headers=self.header)
            return response.text


    def run(self):
        self.handle_page()
        t = ThreadPoolExecutor()
        for url in self.item_url_list:
            t.submit(self.handle_detail,url)
        t.shutdown()


def main():
    dasouche = HandleDaSouChe()
    dasouche.run()


if __name__ == '__main__':
    main()

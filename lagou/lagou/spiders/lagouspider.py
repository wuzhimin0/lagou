# -*- coding: utf-8 -*-
from scrapy.spiders import CrawlSpider
from scrapy.http import Request
from lagou.items import LagouItem
from scrapy import FormRequest
from scrapy.conf import settings
import json
class LagouspiderSpider(CrawlSpider):
    name = 'lagouspider'
    allowed_domains = ['lagou.com']
    start_urls = ['https://www.lagou.com/jobs/positionAjax.json?needAddtionalResult=false']
    '''
    ajax请求的网址
    https://www.lagou.com/jobs/positionAjax.json?gj=3年及以下&xl=硕士&jd=天使轮&hy=电子商务&px=default&gm=15-50人&city=北京&needAddtionalResult=false
    # https://www.lagou.com/jobs/positionAjax.json?gj={gj}&xl={xl}&jd={jd}&hy={hy}&px=default&gm={gm}&city={city}&needAddtionalResult=false
    "city":"北京","gj":"3年及以下","gm":"15-50人","hy":"电子商务","jd":"天使轮","needAddtionalResult":"false","px":"default","xl":"硕士"
    '''
    # cookies有时间限制,拉勾网的cookie时间不知道多长
    cookies ={'JSESSIONID': 'ABAAABAABEEAAJA3C53DE1C8005269EF9EF6E2ADA1498A2', 'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1544076477,1544164769,1544234453,1544249417', 'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6': '1544249438', '_ga': 'GA1.2.77484379.1544249417', '_gat': '1', 'user_trace_token': '20181208140812-a4fc2321-faaf-11e8-8ce7-5254005c3644', 'LGSID': '20181208140812-a4fc256a-faaf-11e8-8ce7-5254005c3644', 'PRE_UTM': '', 'PRE_HOST': 'www.baidu.com', 'PRE_SITE': 'https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DURTJpj_kSph05gHouxqVcamc0au9WcQjpkOp0o2u7AC%26wd%3D%26eqid%3Dacdfffd90005d4e7000000035c0b5fc6', 'PRE_LAND': 'https%3A%2F%2Fwww.lagou.com%2F', 'LGRID': '20181208140833-b1758a72-faaf-11e8-8ce7-5254005c3644', 'LGUID': '20181208140812-a4fc2775-faaf-11e8-8ce7-5254005c3644', 'index_location_city': '%E5%85%A8%E5%9B%BD', 'X_HTTP_TOKEN': '42904a377e3ba26cbd80b015a2e4d729', 'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%221678c702b548a-017c2faede6ebc-45524133-2073600-1678c702b5533%22%2C%22%24device_id%22%3A%221678c702b548a-017c2faede6ebc-45524133-2073600-1678c702b5533%22%7D', 'sajssdk_2015_cross_new_user': '1', '_gid': 'GA1.2.289508789.1544249421', 'LG_LOGIN_USER_ID': 'bf8148f981407646307ecb791fecbafb63fa788c63498ae6b194825ff62e2bff', '_putrc': 'C0D0406357A43F6E123F89F2B170EADC', 'login': 'true', 'unick': '%E6%8B%89%E5%8B%BE%E7%94%A8%E6%88%B78821', 'showExpriedIndex': '1', 'showExpriedCompanyHome': '1', 'showExpriedMyPublish': '1', 'hasDeliver': '0', 'gate_login_token': 'e4d2d0a5fa3463a5b1cbc23ed56a25014d6edc386e1d8c7872e5995b65d5706c', 'TG-TRACK-CODE': 'index_user'}
    headers = settings["DEFAULT_REQUEST_HEADERS"]
    def start_requests(self):
        # for page in range(1,5):
        form_data = {
                "first": "false",
                "kd": "python爬虫",#kd代表要查找的工作
                "pn": "1"
            }
        yield FormRequest(url=self.start_urls[0],formdata=form_data,meta={"data":form_data})
    def parse(self, response):
        form_data = response.meta["data"]
        result = json.loads(response.body)
        # 判断，当没能获取到正确的信息时，就重新请求这个网址,在获取信息
        if "content" not in result:
            yield FormRequest(url=response.url,callback=self.parse,formdata=form_data,meta={"data":form_data},dont_filter=True,headers=self.headers)
        else:
            infos = result["content"]["positionResult"]["result"]
            for info in infos:
                item = LagouItem()
                item["positions"] = info["positionName"]
                position_id = info["positionId"]
                company_id = info["companyId"]
                # 工资
                item["salary"] = info["salary"]
                item["company_name"] = info["companyShortName"]
                item["city"] = info["city"]
                # 地区
                item["district"] = info["district"]
                item["workYear"] = info["workYear"]
                item["education"] = info["education"]
                # 工作标签
                item["industryLables"] = info["industryLables"]
                item["company_url"] = r"https://www.lagou.com/gongsi" + "/" + str(company_id) + ".html"
                # 获得工作详细页
                position_url = r"https://www.lagou.com/jobs" + "/" + str(position_id) + ".html"
                # 爬取详细页需要登录,用cookie模拟登陆
                yield Request(url=position_url,callback=self.detail_position,meta={"data":item},dont_filter=True,cookies=self.cookies,headers=self.headers)
            page = result["content"]["positionResult"]["totalCount"]
            if int(page) % 15 == 0:
                max_page = page / 15
            else:
                max_page = page // 15 + 1
            if max_page >= 30:
                max_page = 30
            else:
                max_page = max_page
            for i in range(2,max_page):
                form_data = {
                    "first": "false",
                    "kd": "python爬虫",  # kd代表要查找的工作
                    "pn": str(i)
                }
                yield FormRequest(url=response.url, formdata=form_data, meta={"data": form_data},headers=self.headers)
    def detail_position(self,response):
        item = response.meta["data"]
        details = response.xpath('//dd[@class="job_bt"]//text()').extract()
        job_detail = ""
        for detail in details:
            if "".join(detail.split()):
                job_detail = job_detail + "".join(detail.split()) + ","
        item["job_detail"] = job_detail[:-1]
        yield item
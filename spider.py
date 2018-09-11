import mitmproxy.http
from mitmproxy import ctx, http
import urllib

import json
import csv
import sys

class Spider(object):
    def __init__(self):
        pass
    
    def response(self, flow: mitmproxy.http.HTTPFlow):
        url = urllib.parse.unquote(flow.request.url)
        ctx.log.info(url)
        if 'api.amemv.com/aweme/v1/general/search/?' in url or 'api.amemv.com/aweme/v1/search/' in url:
            response = flow.response.get_text()
            self.parse_response(response)
        else:
            return
    
    def parse_response(self,response):
        response = json.loads(response)
        items = response.get('aweme_list')
        if items:
            for item in items:
                result = {}
                unique_id = item.get('author').get('unique_id')
                if unique_id:
                    result['id'] = unique_id #抖音号
                else:
                    result['id'] = item.get('author').get('short_id')
                result['nickname'] = item.get('author').get('nickname') #用户名
                result['url'] = item.get('share_url') #小视频链接
                result['like_num'] = item.get('statistics').get('digg_count') #点赞数
                result['comment_count'] = item.get('statistics').get('comment_count') #评论次数
                result['share_count'] = item.get('statistics').get('share_count') #分享次数
                result['info'] = item.get('desc') #视频说明
                self.save_to_csv(result)

    def save_to_csv(self,result):
        file = f'douyin.csv'
        with open(file,'a+',encoding='utf-8',newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(result.values())
        

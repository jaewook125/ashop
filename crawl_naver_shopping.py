import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ashop.settings")
#환경변수가 설정되있어야한다, manage.py와 동일

import django
django.setup()

import sys #코트를 인자로 받기위함
import requests
from bs4 import BeautifulSoup

from django.core.files import File #실제 파일을 저장하기위해 필요
from shop.models import Item 

def trim(s): #어떤 문자열을 받으면
    return ' '.join(s.split())#그 문자열을 화이트스페이스 단위로 나누고 다시 하나의 스페이스로 합치겠다.


def main(query):
	url = "https://search.shopping.naver.com/search/all.nhn"
	params = {'query' : query}
	res = requests.get(url, params=params)
	html = res.text
	soup = BeautifulSoup(html, 'html.parser')

	for item_tag in soup.select('#_search_list ._itemSection'):
	    name = trim(item_tag.select('a.tit')[0].text)
	    price = int(trim(item_tag.select('.price .num')[0].text).replace(',','')) #,를 빈칸으로 바꾼다
	    img_url = item_tag.select('img[data-original]')[0]['data-original'] #img에 data-original태그를 찾아서 data-original속성을 가지고온다

	    res = requests.get(img_url, stream=True)
	    image_name= os.path.basename(img_url.split('?',1)[0]) #? 한개만 해서 [0](앞부분)을 빼낸후에는

	    item = Item(name=name, amount=price, is_public=True)
	    item.photo.save(image_name, File(res.raw))
	    item.save()
	    #media경로와 upload_to 설정과image_name 세가지를 합쳐서
	    #실제 지정한 경로를 삼고 파일을 저장한 후에 저장경로를 photo필드에 저장한다


	    print(name, price, img_url)


if __name__=='__main__':
	try:
		query = sys.argv[1]
		main(query)
	except IndexError:
		print('usage> {} <query>'.format(sys.argv[0]))

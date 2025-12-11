import os
from dotenv import load_dotenv
import pymysql
import requests

load_dotenv()
db_name = os.getenv('DB_NAME')
kakao_rest_api_key = os.getenv('KAKAO_REST_API_KEY')


def query_filtering_test():
    mysql_conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                                 password=os.getenv('DB_PASSWORD'), db=db_name)
    mysql_cur = mysql_conn.cursor()

    request_url = 'https://dapi.kakao.com/v2/local/search/keyword.json?query='
    header = {'Authorization' : f'KakaoAK {kakao_rest_api_key}'}

    mysql_cur.execute(f'select * from {db_name}.place')
    place_list = list(mysql_cur.fetchall())

    count = 0
    for place in place_list:
        keyword = place[0]
        result_pages = 0

        while result_pages == 0:
            keyword_length = len(keyword)

            if keyword_length == 0:
                break

            response = requests.get(url=request_url + keyword, headers=header).json()
            result_pages = response['meta']['pageable_count']

            if result_pages != 0:
                count += 1
                break

            keyword = keyword[:keyword_length - 1]

        print(count)

def post_processing_place():
    mysql_conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('DB_USER'),
                                 password=os.getenv('DB_PASSWORD'), db=db_name)
    mysql_cur = mysql_conn.cursor()

    mysql_cur.execute(f'select * from {db_name}.place')
    place_list = list(mysql_cur.fetchall())

    print(place_list)


if __name__ == '__main__':
    # query_filtering_test()
    post_processing_place()
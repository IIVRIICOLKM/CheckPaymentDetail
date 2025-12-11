import requests
from paymentprocessing import get_messages, preprocessing_date, messages_to_columned_datas
import pymysql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
db_name = os.getenv('MYSQL_DATABASE')

def set_bank_table(banks : list, addresses : list, mysql_cur):
    try:
        mysql_cur.execute(f'select * from {db_name}.bank;')
        bank_infos_in_db = mysql_cur.fetchall()

        if len(bank_infos_in_db) == 0:
            mysql_cur.execute(
                f'insert into {db_name}.bank (name, phone_num) values ("{banks[0]}", "{addresses[0]}");')
        else:
            for bank_info_in_db in bank_infos_in_db:
                if bank_info_in_db[1] != banks[0]:
                    mysql_cur.execute(f'insert into {db_name}.bank (name, phone_num) values ("{banks[0]}", "{addresses[0]}");')

    except Exception as e:
        print(e)

def set_account_table(accountmap : dict, account_nums : list, mysql_cur):
    try:
        mysql_cur.execute(f'select * from {db_name}.bank;')
        bank_infos_in_db = mysql_cur.fetchall()

        mysql_cur.execute(f'select * from {db_name}.account;')
        account_infos_in_db = mysql_cur.fetchall()

        for bank_info_in_db in bank_infos_in_db:
            _bank_id, _bank_name = bank_info_in_db[0], bank_info_in_db[1]

            if len(account_infos_in_db) == 0:
                for account_num in account_nums:
                    if accountmap[account_num] == _bank_name:
                        mysql_cur.execute(
                            f'insert into {db_name}.account (number, created_at, bank_id, user_id) values ("{account_num}", "{datetime.now()}", "{_bank_id}", "djrlee1");')
            else:
                for account_num in account_nums:
                    count = 0
                    for account_info_in_db in account_infos_in_db:
                        _acc_num_in_db = account_info_in_db[1]
                        if _acc_num_in_db == account_num:
                            count += 1
                    if (count == 0) and (accountmap[account_num] == _bank_name):
                        mysql_cur.execute(
                            f'insert into {db_name}.account (number, created_at, bank_id, user_id) values ("{account_num}", "{datetime.now()}", "{_bank_id}", "djrlee1");')

    except Exception as e:
        print(e)


def set_place_table(place_name : str, mysql_cur):
    # 임시로 카테고리 1로 설정
    try:
        mysql_cur.execute(f'insert into {db_name}.place (name, is_financial_transaction, place_category_id) values ("{place_name}", 0, 1);')
        mysql_cur.execute('SELECT LAST_INSERT_ID();')
        new_id = mysql_cur.fetchone()[0]

        return new_id
    # 프로그램 중단 방지용 예외처리
    except Exception as e:
        mysql_cur.execute(f'SELECT id FROM {db_name}.place WHERE name = "{place_name}" LIMIT 1;')
        new_id = mysql_cur.fetchone()[0]

        return new_id

def parse_payment_to_database(table : list, banks : list, addresses : list, accountmap : dict, account_nums : list):
    mysql_conn = pymysql.connect(host=os.getenv('DB_HOST'), user=os.getenv('MYSQL_USER'), password=os.getenv('MYSQL_PASSWORD'), db=db_name)
    mysql_cur = mysql_conn.cursor()

    try:
        set_bank_table(banks=banks, addresses=addresses, mysql_cur=mysql_cur)
        set_account_table(accountmap=accountmap, account_nums=account_nums, mysql_cur=mysql_cur)
        mysql_cur.execute(f'truncate {db_name}.payment;')

        count = 0
        for row in table:
            _payment_day = str(row[0])
            _account_number = row[1]
            mysql_cur.execute(f'select id from {db_name}.account where number="{_account_number}";')
            _account_id = mysql_cur.fetchone()
            _account_id = _account_id[0]

            _place_name = row[2]

            new_id = set_place_table(row[2], mysql_cur=mysql_cur)

            _amount = row[3]
            _balance = row[4]

            mysql_cur.execute(f'insert into {db_name}.payment (payment_day, amount, balance, account_id, account_number, place_id, user_id)'
                              f'values ("{_payment_day}", "{_amount}", "{_balance}", "{_account_id}", "{_account_number}", "{new_id}", "djrlee1");')
            count += 1
        print(f'{count}개 레코드 생성 완료!!')
    except Exception as e:
        print('error in ppdb ' + str(e))
        return

    mysql_conn.commit()

def pipeline():
    messages = get_messages('sms_backup_20250729.csv')
    messages = preprocessing_date(messages)
    # 단일 은행의 전화번호만 가져온다고 가정하기
    address = messages[0][2]
    payment_table, banks, addresses, accountmap, account_nums = messages_to_columned_datas(messages)
    parse_payment_to_database(table=payment_table, banks=banks, addresses=addresses, accountmap=accountmap, account_nums=account_nums)

if __name__ == '__main__':
    pipeline()
import pandas as pd
import numpy as np
from datetime import datetime

def get_messages(filename):
    try:
        df = pd.read_csv(filename, encoding='cp949')
        df = df[['body', 'readable_date', 'address']]
        return df.values
    except Exception as e:
        print('error in get_messages' + str(e))

def preprocessing_date(messages):
    """
    csv 형태로 백업한 지출 내역 문자 데이터 중 날짜를 mysql 포맷으로 전처리하는 함수 \n
    messages : numpy.values \n
    return : numpy.values(modified readable_date column in messages)
    """
    msg = messages[2:]
    for i in range(len(msg)):
        pm_index = msg[i][1].find('오후')

        if pm_index != -1:
            hour_start_index = pm_index + 3
            if msg[i][1][hour_start_index + 1] == ':':
                msg[i][1] = (msg[i][1][:hour_start_index] +
                             str(int(msg[i][1][hour_start_index]) + 12) +
                             msg[i][1][hour_start_index + 1:])
            else:
                msg[i][1] = (msg[i][1][:hour_start_index] +
                             str(int(msg[i][1][hour_start_index]) + 12) +
                             msg[i][1][hour_start_index + 2:])

        processed_msg = (
                            msg[i][1].replace(' ', '')
                                .replace('오전', '')
                                .replace('오후', '')
                                .replace('.', '-')
                        )

        if processed_msg[8] == '-':
            processed_msg = processed_msg[:8] + ' ' + processed_msg[9:]
        elif processed_msg[9] == '-':
            processed_msg = processed_msg[:9] + ' ' + processed_msg[10:]
        elif processed_msg[10] == '-':
            processed_msg = processed_msg[:10] + ' ' + processed_msg[11:]

        processed_msg = datetime.strptime(processed_msg, '%Y-%m-%d %H:%M:%S')
        msg[i][1] = processed_msg
    return msg

# def messages_to_columned_datas(messages):
#     # csv 형태로 백업한 지출 내역 문자 데이터의 body에 있는 정보를 mysql 포맷으로 전처리하는 함수
#     # messages : numpy.values
#     # return : messages.reshpae(len(messages), column_counts)
#
#     msgs = messages
#     new_msgs = np.array([])
#     err_count = 0
#
#     for msg in msgs:
#         account_num, place, amount, balance = '', '', 0, 0
#
#         if not msg[0].startswith('['):
#             err_count += 1
#             continue
#
#         # Slice body datas with token
#         # account_num, place, deposit or withdraw, amount, balance
#         first_sliced = msg[0][16:].replace(',', '')
#         # place, deposit or withdraw, amount, balance
#         second_sliced = first_sliced[12:]
#         place_end_idx = second_sliced.find('\n')
#         # deposit or withdraw, amount, balance
#         third_sliced = second_sliced[place_end_idx + 1:]
#         payed_type_end_idx = third_sliced.find('\n')
#         # amount, balance
#         fourth_sliced = third_sliced[payed_type_end_idx + 1:]
#
#         # Process outlier datasets
#         if second_sliced[:place_end_idx].find('출금') != -1 or \
#         second_sliced[:place_end_idx].find('입금') != -1:
#             if third_sliced[:payed_type_end_idx].find('출금') == -1 and \
#             third_sliced[:payed_type_end_idx].find('입금') == -1:
#                 fourth_sliced = third_sliced
#                 third_sliced = second_sliced
#         else:
#             place = second_sliced[:place_end_idx]
#
#         amount_end_idx = fourth_sliced.find('\n')
#         # balance
#         fifth_sliced = fourth_sliced[amount_end_idx + 1:]
#
#         # Put preprocessed datas in column variables and append in array
#         account_num = first_sliced[:11]
#         amount = -1 * int(fourth_sliced[:amount_end_idx]) \
#             if third_sliced.find('입금') == -1 \
#             else int(fourth_sliced[:amount_end_idx])
#         balance = int(fifth_sliced[2:])
#
#         new_msg = np.array([])
#         new_msg = np.append(new_msg, np.array([msg[1], account_num, place, amount, balance]))
#         new_msgs = np.append(new_msgs, new_msg)
#     # Broadcast
#     return new_msgs.reshape(len(msgs) - err_count, 5)

def messages_to_columned_datas(messages):
    """
        csv 형태로 백업한 지출 내역 문자 데이터의 body에 있는 정보를 mysql 포맷으로 전처리하는 함수 \n
        messages : numpy.values \n
        return : np.array(msgs)
    """
    msgs, account_nums = [], []
    account_nums.append(messages[0][0][16:27])

    for msg in messages:
        if not msg[0].startswith('['):
            continue
        try:
            body = msg[0][16:].replace(',', '')
            account_num = body[:11]

            if account_num not in account_nums:
                account_nums.append(account_num)

            rest = body[12:]
            lines = rest.split('\n')

            if len(lines) < 4:
                lines.append('')

            # 출금/입금 판단 & 위치 보정
            if ('출금' in lines[0] or '입금' in lines[0]):
                if not ('출금' in lines[1] or '입금' in lines[1]):
                    lines[3] = lines[2]
                    lines[2] = lines[1]
                    lines[1] = lines[0]
                lines[0] = ''

            place, trans_type, amount_str, balance_str = lines[0], lines[1], lines[2], lines[3]

            amount = int(amount_str) if '입금' in trans_type else -int(amount_str)
            balance = int(balance_str[2:])

            msgs.append([msg[1], account_num, place, amount, balance])

        except Exception as e:
            print('error in messaged_to_columned_datas' + str(e))
            continue
    return np.array(msgs), account_nums
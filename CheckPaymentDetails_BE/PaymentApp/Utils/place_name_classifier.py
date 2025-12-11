import pandas as pd
from PaymentApp.DataSets.dataset_dir import dataset_dir

df_m, df_w = pd.read_csv(dataset_dir + 'men_names.csv'), pd.read_csv(dataset_dir + 'women_names.csv')
df_m, df_w = df_m[df_m['weight'] > 11], df_w[df_w['weight'] > 11]

import pandas as pd
from PaymentApp.DataSets.dataset_dir import dataset_dir

def place_name_classifier(place : str) -> float:
    # 인덱스 새로 바인딩
    df_m.index, df_w.index = [i for i in range (0, len(df_m))], [i for i in range (0, len(df_w))]
    men_names, women_names = df_m['name'].tolist(), df_w['name'].tolist()
    result_men, result_women = binary_searchNget_index(men_names, place), binary_searchNget_index(women_names, place)
    if result_men[0] & result_women[0]:
        return df_m['percentage'][result_men[1]] \
            if df_m['percentage'][result_men[1]] > df_w['percentage'][result_women[1]] \
            else df_w['percentage'][result_women[1]]
    elif result_men[0]:
        return df_m['percentage'][result_men[1]]
    elif result_women[0]:
        return df_w['percentage'][result_women[1]]
    else:
        return 0.0

def binary_searchNget_index(l : list, find_str : str):
    data_length = len(l)
    start, end = 0, data_length - 1
    mid = (start + end) // 2

    if l[mid] == find_str:
        return True, mid

    while start <= end:
        if l[mid] > find_str:
            end = mid - 1
        elif l[mid] < find_str:
            start = mid + 1
        else:
            return True, mid
        mid = (start + end) // 2
    return False, -1

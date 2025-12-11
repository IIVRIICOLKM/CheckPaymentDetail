import pandas as pd
import re
from PaymentApp.DataSets.dataset_dir import dataset_dir
from place_name_classifier import place_name_classifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt

df_fn = pd.read_csv(dataset_dir + 'first_names.csv')
SURNAMES = ''.join(df_fn['first_name'].tolist())
NAME_RE = re.compile(rf"^([{SURNAMES}])[가-힣]{{2}}|(토스)([{SURNAMES}])[가-힣]{{2}}$")

predicted_name_list = []

def get_fn_percentage(s: str, i: int) -> float:
    res = df_fn[df_fn['first_name'] == s[i]]['percentage']
    per = 0.0
    for row in res:
        per += row
    return per

def contains_korean_name_raw(s: str) -> bool:
    if not isinstance(s, str):
        return False
    m = NAME_RE.search(s)
    if bool(m):
        predicted_name = m.group(0)
        predicted_name_list.append(predicted_name)
        # 가능한 이름 여부 매칭
        if predicted_name.startswith('토스'):
            per_fn = get_fn_percentage(predicted_name, 2)
            per_n = place_name_classifier(predicted_name[3:5])
            return per_fn * per_n > 1e-7
        else:
            per_fn = get_fn_percentage(predicted_name, 0)
            per_n = place_name_classifier(predicted_name[1:3])
            return per_fn * per_n > 1e-7
    else:
        predicted_name_list.append('')
        return bool(m)

def label_people_in_csv(input_csv: str, output_csv: str = None):
    df = pd.read_csv(input_csv)
    if 'place_name' not in df.columns:
        raise ValueError("CSV에 'place_name' 컬럼이 필요합니다.")
    predicted_name_list.append('')
    df['pred_is_people'] = df['place_name'].apply(lambda x: int(contains_korean_name_raw(x)))

    new_df = df['place_name']
    new_df = pd.DataFrame(new_df)
    new_df['whether_calculated'] = df['whether_calculated'].tolist()
    new_df['is_people'] = df['is_people'].tolist()
    new_df['pred_is_people'] = df['pred_is_people'].tolist()
    new_df['predicted_name'] = predicted_name_list

    if output_csv:
        new_df.to_csv(output_csv, encoding='CP949', index=False)
    return new_df

if __name__ == "__main__":
    output_csv = label_people_in_csv(dataset_dir + "place_list.csv", dataset_dir + "place_list_labeled.csv")
    y_actual, y_pred = output_csv['is_people'].tolist(), output_csv['pred_is_people'].tolist()
    print('Accuracy = ', accuracy_score(y_actual, y_pred))
    print('Report = ', classification_report(y_actual, y_pred))

    cnf_matrix = confusion_matrix(y_actual, y_pred, labels=[0, 1])
    print(cnf_matrix)
    sns.heatmap(cnf_matrix, annot=True, cmap='Blues')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.title('Confusion Matrix')
    plt.show()
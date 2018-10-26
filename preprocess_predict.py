import pandas as pd
import os
import json
import statistics
import re
import math


# 対象レースデータファイルのパス
TARGET_RACE_DATA_PATH = './data/predict/20180914210705/2018091421070502.json'
# レースデータファイルを格納しているフォルダ
RACE_DATA_DIR = './data/train_test/'
# 騎手データファイルのパス
JOCKEY_DATA_PATH = './data/jockey.json'

# レースデータファイルのファイル名一覧を取得
file_list = []
for pathname, dirnames, filenames in os.walk(RACE_DATA_DIR):
    for filename in filenames:
        file_list.append(os.path.join(pathname, filename))

# 騎手データファイルを読込
f = open(JOCKEY_DATA_PATH, 'r', encoding='utf-8_sig')
jockey_dict = json.load(f)
f.close()

# 補間用の中央値を算出
median_rank_list = []
median_popularity_list = []
median_three_furlong_list = []
for file_path in file_list:
    f = open(file_path, 'r', encoding="utf-8_sig")
    json_list = json.load(f)
    if len(json_list) != 0:
        for json_data in json_list:
            if json_data['horse_number'].isdecimal() and json_data['rank'].isdecimal() and json_data['weight'].isdecimal():
                # 過去5走
                if 'prev1_rank' in json_data:
                    median_rank_list.append(float(json_data['prev1_rank']))
                    median_popularity_list.append(float(json_data['prev1_popularity']))
                    median_three_furlong_list.append(float(json_data['prev1_three_furlong']))
                if 'prev2_rank' in json_data:
                    median_rank_list.append(float(json_data['prev2_rank']))
                    median_popularity_list.append(float(json_data['prev2_popularity']))
                    median_three_furlong_list.append(float(json_data['prev2_three_furlong']))
                if 'prev3_rank' in json_data:
                    median_rank_list.append(float(json_data['prev3_rank']))
                    median_popularity_list.append(float(json_data['prev3_popularity']))
                    median_three_furlong_list.append(float(json_data['prev3_three_furlong']))
                if 'prev4_rank' in json_data:
                    median_rank_list.append(float(json_data['prev4_rank']))
                    median_popularity_list.append(float(json_data['prev4_popularity']))
                    median_three_furlong_list.append(float(json_data['prev4_three_furlong']))
                if 'prev5_rank' in json_data:
                    median_rank_list.append(float(json_data['prev5_rank']))
                    median_popularity_list.append(float(json_data['prev5_popularity']))
                    median_three_furlong_list.append(float(json_data['prev5_three_furlong']))
    f.close()

median_rank = statistics.median(median_rank_list)
median_popularity = statistics.median(median_popularity_list)
median_three_furlong = statistics.median(median_three_furlong_list)

# 予想するレースのデータを読込
data_list = []
f = open(TARGET_RACE_DATA_PATH, 'r', encoding="utf-8_sig")
json_list = json.load(f)
for json_data in json_list:
    if json_data['horse_number'].isdecimal() and json_data['weight'].isdecimal():
        # 性別
        sex = 1 if json_data['sex'] == '牝' else 0
        json_data['sex'] = sex

        # 斤量
        pattern = r'([+-]?[0-9]+\.?[0-9]*)'
        json_data['burden'] = float(re.findall(pattern, json_data['burden'])[0])

        # 増減
        pattern = r'[＋±]'
        margin = json_data['margin']
        if len(re.findall(pattern, margin)) > 0:
            json_data['margin'] = re.sub(pattern, '', margin)
        elif margin == '-':
            json_data['margin'] = -1
        else:
            json_data['margin'] = margin

        # トータル成績
        if math.isnan(float(json_data['total_win_rate'])):
            json_data['total_win_rate'] = 0
            json_data['total_ren_rate'] = 0
            json_data['total_fuku_rate'] = 0

        # 競馬場＆距離別成績
        if math.isnan(float(json_data['limit_win_rate'])):
            json_data['limit_win_rate'] = 0
            json_data['limit_ren_rate'] = 0
            json_data['limit_fuku_rate'] = 0

        # 過去5走
        if 'prev1_rank' not in json_data:
            json_data['prev1_rank'] = median_rank
            json_data['prev1_popularity'] = median_popularity
            json_data['prev1_three_furlong'] = median_three_furlong
        if 'prev2_rank' not in json_data:
            json_data['prev2_rank'] = median_rank
            json_data['prev2_popularity'] = median_popularity
            json_data['prev2_three_furlong'] = median_three_furlong
        if 'prev3_rank' not in json_data:
            json_data['prev3_rank'] = median_rank
            json_data['prev3_popularity'] = median_popularity
            json_data['prev3_three_furlong'] = median_three_furlong
        if 'prev4_rank' not in json_data:
            json_data['prev4_rank'] = median_rank
            json_data['prev4_popularity'] = median_popularity
            json_data['prev4_three_furlong'] = median_three_furlong
        if 'prev5_rank' not in json_data:
            json_data['prev5_rank'] = median_rank
            json_data['prev5_popularity'] = median_popularity
            json_data['prev5_three_furlong'] = median_three_furlong

        # 騎手
        jockey_id = json_data['jockey']
        if jockey_id in jockey_dict:
            json_data['jockey_this_win'] = jockey_dict[jockey_id]['this_win']
            json_data['jockey_this_ren'] = jockey_dict[jockey_id]['this_ren']
            json_data['jockey_last_win'] = jockey_dict[jockey_id]['last_win']
            json_data['jockey_last_ren'] = jockey_dict[jockey_id]['last_ren']
        else:
            json_data['jockey_this_win'] = 0
            json_data['jockey_this_ren'] = 0
            json_data['jockey_last_win'] = 0
            json_data['jockey_last_ren'] = 0

        # 不要な情報を削除
        if 'horse_name' in json_data:
            del json_data['horse_name']
        if 'trainer' in json_data:
            del json_data['trainer']
        if 'jockey' in json_data:
            del json_data['jockey']
        if 'three_furlong' in json_data:
            del json_data['three_furlong']
        if 'prev0_rank' in json_data:
            del json_data['prev0_rank']
        if 'prev0_popularity' in json_data:
            del json_data['prev0_popularity']
        if 'prev0_three_furlong' in json_data:
            del json_data['prev0_three_furlong']
        if 'prev0_time' in json_data:
            del json_data['prev0_time']
        if 'prev1_time' in json_data:
            del json_data['prev1_time']
        if 'prev2_time' in json_data:
            del json_data['prev2_time']
        if 'prev3_time' in json_data:
            del json_data['prev3_time']
        if 'prev4_time' in json_data:
            del json_data['prev4_time']
        if 'prev5_time' in json_data:
            del json_data['prev5_time']

        data_list.append(json_data)
f.close()

# デバッグ用
print(data_list[0])

# データフレームに変換
df = pd.DataFrame(data_list)
df = df.set_index('horse_number')

# CSVファイルに保存
df.to_csv('./dataset_predict.csv')

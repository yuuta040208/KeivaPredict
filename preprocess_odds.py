import os
import json
import pandas as pd
import matplotlib.pyplot as plt

# レースデータファイルのファイル名一覧を取得
file_list = []
for pathname, dirnames, filenames in os.walk('./unko'):
    for filename in filenames:
        file_list.append(os.path.join(pathname, filename))

# 全データ
all_df = pd.DataFrame()

for file_path in file_list:
    f = open(file_path, 'r', encoding="utf-8_sig")
    odds_dict = json.load(f)
    if len(odds_dict) != 0:

        # 単勝ランキング
        win_rank = []
        win_dict = {}
        for elem in odds_dict['win']:
            win_dict[elem['number']] = elem['odds']
            win_rank.append(elem['number'])

        # 複勝ランキング
        place_rank = []
        place_dict = {}
        for elem in odds_dict['place']:
            place_dict[elem['number']] = elem['odds']
            place_rank.append(elem['number'])

        # 馬単１着ランキング
        exacta1_rank = []
        exacta1_dict = {}
        for elem in odds_dict['exacta']:
            if elem['odds'] != 0:
                if elem['number'][0] in exacta1_dict:
                    exacta1_dict[elem['number'][0]] += 1 / elem['odds']
                else:
                    exacta1_dict[elem['number'][0]] = 1 / elem['odds']
        for k, v in sorted(exacta1_dict.items(), key=lambda x: -x[1]):
            exacta1_rank.append(k)

        # 馬単２着ランキング
        exacta2_rank = []
        exacta2_dict = {}
        for elem in odds_dict['exacta']:
            if elem['odds'] != 0:
                if elem['number'][1] in exacta2_dict:
                    exacta2_dict[elem['number'][1]] += 1 / elem['odds']
                else:
                    exacta2_dict[elem['number'][1]] = 1 / elem['odds']
        for k, v in sorted(exacta2_dict.items(), key=lambda x: -x[1]):
            exacta2_rank.append(k)

        # 馬連ランキング
        quinella_rank = []
        quinella_dict = {}
        for elem in odds_dict['quinella']:
            if elem['odds'] != 0:
                if elem['number'][0] in quinella_dict:
                    quinella_dict[elem['number'][0]] += 1 / elem['odds']
                else:
                    quinella_dict[elem['number'][0]] = 1 / elem['odds']
                if elem['number'][1] in quinella_dict:
                    quinella_dict[elem['number'][1]] += 1 / elem['odds']
                else:
                    quinella_dict[elem['number'][1]] = 1 / elem['odds']
        for k, v in sorted(quinella_dict.items(), key=lambda x: -x[1]):
            quinella_rank.append(k)

        # ワイドランキング
        quinella_place_rank = []
        quinella_place_dict = {}
        for elem in odds_dict['quinellaPlace']:
            if elem['odds'] != 0:
                if elem['number'][0] in quinella_place_dict:
                    quinella_place_dict[elem['number'][0]] += 1 / elem['odds']
                else:
                    quinella_place_dict[elem['number'][0]] = 1 / elem['odds']
                if elem['number'][1] in quinella_place_dict:
                    quinella_place_dict[elem['number'][1]] += 1 / elem['odds']
                else:
                    quinella_place_dict[elem['number'][1]] = 1 / elem['odds']
        for k, v in sorted(quinella_place_dict.items(), key=lambda x: -x[1]):
            quinella_place_rank.append(k)

        # ３連単１着ランキング
        tierce1_rank = []
        tierce1_dict = {}
        for elem in odds_dict['tierce']:
            if elem['odds'] != 0:
                if elem['number'][0] in tierce1_dict:
                    tierce1_dict[elem['number'][0]] += 1 / elem['odds']
                else:
                    tierce1_dict[elem['number'][0]] = 1 / elem['odds']
        for k, v in sorted(tierce1_dict.items(), key=lambda x: -x[1]):
            tierce1_rank.append(k)

        # ３連単２着ランキング
        tierce2_rank = []
        tierce2_dict = {}
        for elem in odds_dict['tierce']:
            if elem['odds'] != 0:
                if elem['number'][1] in tierce2_dict:
                    tierce2_dict[elem['number'][1]] += 1 / elem['odds']
                else:
                    tierce2_dict[elem['number'][1]] = 1 / elem['odds']
        for k, v in sorted(tierce2_dict.items(), key=lambda x: -x[1]):
            tierce2_rank.append(k)

        # ３連単３着ランキング
        tierce3_rank = []
        tierce3_dict = {}
        for elem in odds_dict['tierce']:
            if elem['odds'] != 0:
                if elem['number'][2] in tierce3_dict:
                    tierce3_dict[elem['number'][2]] += 1 / elem['odds']
                else:
                    tierce3_dict[elem['number'][2]] = 1 / elem['odds']
        for k, v in sorted(tierce3_dict.items(), key=lambda x: -x[1]):
            tierce3_rank.append(k)

        # ３連複ランキング
        trio_rank = []
        trio_dict = {}
        for elem in odds_dict['trio']:
            if elem['odds'] != 0:
                if elem['number'][0] in trio_dict:
                    trio_dict[elem['number'][0]] += 1 / elem['odds']
                else:
                    trio_dict[elem['number'][0]] = 1 / elem['odds']
                if elem['number'][1] in trio_dict:
                    trio_dict[elem['number'][1]] += 1 / elem['odds']
                else:
                    trio_dict[elem['number'][1]] = 1 / elem['odds']
                if elem['number'][2] in trio_dict:
                    trio_dict[elem['number'][2]] += 1 / elem['odds']
                else:
                    trio_dict[elem['number'][2]] = 1 / elem['odds']
        for k, v in sorted(quinella_dict.items(), key=lambda x: -x[1]):
            trio_rank.append(k)

        # ポイント付け
        # 単勝のランクを正解として、正解着順より上位にいる馬に差分を加算
        point_dict = {}
        place_dict = {}
        exacta1_dict = {}
        quinella_dict = {}
        quinella_place_dict = {}
        tierce1_dict = {}
        trio_dict = {}
        exacta2_dict = {}
        tierce2_dict = {}
        tierce3_dict = {}

        for i in win_rank:
            place_dict[i] = 0
            exacta1_dict[i] = 0
            quinella_dict[i] = 0
            quinella_place_dict[i] = 0
            tierce1_dict[i] = 0
            trio_dict[i] = 0
            exacta2_dict[i] = 0
            tierce2_dict[i] = 0
            tierce3_dict[i] = 0

        # 複勝
        for i, place in enumerate(place_rank):
            for j, win in enumerate(win_rank):
                if place == win:
                    if i < j:
                        if place in point_dict:
                            point_dict[place] += j - i
                            place_dict[place] += j - i
                        else:
                            point_dict[place] = j - i
                            place_dict[place] = j - i
                    break

        # 馬単１着
        for i, exacta1 in enumerate(exacta1_rank):
            for j, win in enumerate(win_rank):
                if exacta1 == win:
                    if i < j:
                        if exacta1 in point_dict:
                            point_dict[exacta1] += j - i
                            exacta1_dict[exacta1] += j - i
                        else:
                            point_dict[exacta1] = j - i
                            exacta1_dict[exacta1] = j - i
                    break

        # 馬連
        for i, quinella in enumerate(quinella_rank):
            for j, win in enumerate(win_rank):
                if quinella == win:
                    if i < j:
                        if quinella in point_dict:
                            point_dict[quinella] += j - i
                            quinella_dict[quinella] += j - i
                        else:
                            point_dict[quinella] = j - i
                            quinella_dict[quinella] = j - i
                    break

        # ワイド
        for i, quinella_place in enumerate(quinella_place_rank):
            for j, win in enumerate(win_rank):
                if quinella_place == win:
                    if i < j:
                        if quinella_place in point_dict:
                            point_dict[quinella_place] += j - i
                            quinella_place_dict[quinella_place] += j - i
                        else:
                            point_dict[quinella_place] = j - i
                            quinella_place_dict[quinella_place] = j - i
                    break

        # ３連単１着
        for i, tierce1 in enumerate(tierce1_rank):
            for j, win in enumerate(win_rank):
                if tierce1 == win:
                    if i < j:
                        if tierce1 in point_dict:
                            point_dict[tierce1] += j - i
                            tierce1_dict[tierce1] += j - i
                        else:
                            point_dict[tierce1] = j - i
                            tierce1_dict[tierce1] = j - i
                    break

        # ３連複
        for i, trio in enumerate(trio_rank):
            for j, win in enumerate(win_rank):
                if trio == win:
                    if i < j:
                        if trio in point_dict:
                            point_dict[trio] += j - i
                            trio_dict[trio] += j - i
                        else:
                            point_dict[trio] = j - i
                            trio_dict[trio] = j - i
                    break

        # 馬単２着
        for i, exacta2 in enumerate(exacta2_rank):
            for j, win in enumerate(win_rank):
                if exacta2 == win:
                    if i < j:
                        if exacta2 in point_dict:
                            point_dict[exacta2] += j - i
                            exacta2_dict[exacta2] += j - i
                        else:
                            point_dict[exacta2] = j - i
                            exacta2_dict[exacta2] = j - i
                    break

        # ３連単２着
        for i, tierce2 in enumerate(tierce2_rank):
            for j, win in enumerate(win_rank):
                if tierce2 == win:
                    if i < j:
                        if tierce2 in point_dict:
                            point_dict[tierce2] += j - i
                            tierce2_dict[tierce2] += j - i
                        else:
                            point_dict[tierce2] = j - i
                            tierce2_dict[tierce2] = j - i
                    break

        # ３連単３着
        for i, tierce3 in enumerate(tierce3_rank):
            for j, win in enumerate(win_rank):
                if tierce3 == win:
                    if i < j:
                        if tierce3 in point_dict:
                            point_dict[tierce3] += j - i
                            tierce3_dict[tierce3] += j - i
                        else:
                            point_dict[tierce3] = j - i
                            tierce3_dict[tierce3] = j - i
                    break

        # 単勝オッズ
        number_list = []
        win_list = []
        for win in odds_dict['win']:
            number_list.append(win['number'])
            win_list.append(win['odds'])

        # 複勝オッズ
        place_list = []
        for number in number_list:
            for place in odds_dict['place']:
                if place['number'] == number:
                    place_list.append(place['odds'])

        # オッズの断層を取得
        win_gap_list = []
        for i, elem in enumerate(odds_dict['win']):
            if i < len(win_rank) - 1:
                win_gap_list.append(odds_dict['win'][i + 1]['odds'] / elem['odds'])
        win_gap_list.append(1.0)

        win_gap_point = [0] * len(win_rank)
        for index, win_gap in enumerate(win_gap_list):
            if win_gap > 2:
                for i in range(index + 1):
                    win_gap_point[i] += 1

        place_gap_list = []
        for i, elem in enumerate(odds_dict['place']):
            if i < len(place_rank) - 1:
                place_gap_list.append(odds_dict['place'][i + 1]['odds'] / elem['odds'])

        # 複勝が発売されていないレースだった場合
        if len(place_list) == 0:
            for number in number_list:
                place_list.append(0)
                place_gap_list.append(1.0)
        else:
            place_gap_list.append(1.0)

        # 着順
        # rank_list = []
        # for number in number_list:
        #     for rank in odds_dict['result']:
        #         if int(rank['number']) == number:
        #             if rank['rank'].isdecimal():
        #                 rank_list.append(int(rank['rank']))
        #             else:
        #                 rank_list.append(-1)
        rank_list = []
        for number in number_list:
            for rank in odds_dict['result']:
                if int(rank['number']) == number:
                    if str(rank['rank']).isdecimal():
                        if int(rank['rank']) <= 3:
                            rank_list.append(1)
                        else:
                            rank_list.append(0)
                    else:
                        rank_list.append(0)

        # ポイント
        # 存在しない馬番を探索
        rm_list = []
        for index in range(1, max(number_list)):
            if index not in number_list:
                rm_list.append(index)

        point_list = [0] * (max(number_list))
        for key in point_dict:
            point_list[key - 1] = point_dict[key]

        place_point_list = [0] * (max(number_list))
        for key in place_dict:
            place_point_list[key - 1] = place_dict[key]

        exacta1_point_list = [0] * (max(number_list))
        for key in exacta1_dict:
            exacta1_point_list[key - 1] = exacta1_dict[key]

        quinella_point_list = [0] * (max(number_list))
        for key in quinella_dict:
            quinella_point_list[key - 1] = quinella_dict[key]

        quinella_place_point_list = [0] * (max(number_list))
        for key in quinella_place_dict:
            quinella_place_point_list[key - 1] = quinella_place_dict[key]

        tierce1_point_list = [0] * (max(number_list))
        for key in tierce1_dict:
            tierce1_point_list[key - 1] = tierce1_dict[key]

        trio_point_list = [0] * (max(number_list))
        for key in trio_dict:
            trio_point_list[key - 1] = trio_dict[key]

        exacta2_point_list = [0] * (max(number_list))
        for key in exacta2_dict:
            exacta2_point_list[key - 1] = exacta2_dict[key]

        tierce2_point_list = [0] * (max(number_list))
        for key in tierce2_dict:
            tierce2_point_list[key - 1] = tierce2_dict[key]

        tierce3_point_list = [0] * (max(number_list))
        for key in tierce3_dict:
            tierce3_point_list[key - 1] = tierce3_dict[key]

        if len(rm_list) > 0:
            for rm_number in rm_list:
                del point_list[rm_number - 1]
                del place_point_list[rm_number - 1]
                del exacta1_point_list[rm_number - 1]
                del quinella_point_list[rm_number - 1]
                del quinella_place_point_list[rm_number - 1]
                del tierce1_point_list[rm_number - 1]
                del trio_point_list[rm_number - 1]
                del exacta2_point_list[rm_number - 1]
                del tierce2_point_list[rm_number - 1]
                del tierce3_point_list[rm_number - 1]

        print('=====')
        print(file_path)
        print(number_list)
        print(rank_list)
        print(place_list)
        print(point_list)
        print(win_gap_list)
        print(place_gap_list)

        # データフレームを作成
        df = pd.DataFrame({"rank": rank_list,
                           "number": number_list,
                           "point": point_list,
                           "place_point": place_point_list,
                           "exacta1_point": exacta1_point_list,
                           "quinella_point": quinella_point_list,
                           "quinella_place_point": quinella_place_point_list,
                           "tierce1_point": tierce1_point_list,
                           "trio_point": trio_point_list,
                           "exacta2_point": exacta2_point_list,
                           "tierce2_point": tierce2_point_list,
                           "tierce3_point": tierce3_point_list,
                           "win_gap": win_gap_list,
                           "place_gap": place_gap_list,
                           # "win": win_list,
                           # "place": place_list,
                           "count": len(number_list)})
        df = df.set_index('number')

        # df = pd.DataFrame({"rank": rank_list,
        #                    "win": win_list,
        #                    "place": place_list})
        # df = df.set_index('rank')

        # データフレームを結合
        if len(all_df) != 0:
            all_df = pd.concat([all_df, df])
        else:
            all_df = df

all_df.to_csv('./dataset_odds.csv')
# all_df.to_csv('./answer_odds.csv')

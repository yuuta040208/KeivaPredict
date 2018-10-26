import os
import json
import matplotlib.pyplot as plt

# レースデータファイルのファイル名一覧を取得
file_list = []
for pathname, dirnames, filenames in os.walk('./unko'):
    for filename in filenames:
        file_list.append(os.path.join(pathname, filename))

# 購入金額
purchace_win_total = 0
purchace_place_total = 0
purchace_total_list = []
# 的中金額
hit_win_total = 0
hit_win_total_list = []
hit_place_total = 0
hit_place_total_list = []

count = 0
for file_path in file_list:
    if count < 12000:
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
            # ポイント付け
            # 単勝のランクを正解として、正解着順より上位にいる馬に差分を加算
            point_dict = {}
            place_dict = {}
            win_dict = {}

            for i in win_rank:
                place_dict[i] = 0
                win_dict[i] = 0

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
                                win_dict[exacta1] += j - i
                            else:
                                point_dict[exacta1] = j - i
                                win_dict[exacta1] = j - i
                        break

            # 馬連
            for i, quinella in enumerate(quinella_rank):
                for j, win in enumerate(win_rank):
                    if quinella == win:
                        if i < j:
                            if quinella in point_dict:
                                point_dict[quinella] += j - i
                                place_dict[quinella] += j - i
                            else:
                                point_dict[quinella] = j - i
                                place_dict[quinella] = j - i
                        break

            # ワイド
            for i, quinella_place in enumerate(quinella_place_rank):
                for j, win in enumerate(win_rank):
                    if quinella_place == win:
                        if i < j:
                            if quinella_place in point_dict:
                                point_dict[quinella_place] += j - i
                                place_dict[quinella_place] += j - i
                            else:
                                point_dict[quinella_place] = j - i
                                place_dict[quinella_place] = j - i
                        break

            # ３連単１着
            for i, tierce1 in enumerate(tierce1_rank):
                for j, win in enumerate(win_rank):
                    if tierce1 == win:
                        if i < j:
                            if tierce1 in point_dict:
                                point_dict[tierce1] += j - i
                                win_dict[tierce1] += j - i
                            else:
                                point_dict[tierce1] = j - i
                                win_dict[tierce1] = j - i
                        break

            # ３連複
            for i, trio in enumerate(trio_rank):
                for j, win in enumerate(win_rank):
                    if trio == win:
                        if i < j:
                            if trio in point_dict:
                                point_dict[trio] += j - i
                                place_dict[trio] += j - i
                            else:
                                point_dict[trio] = j - i
                                place_dict[trio] = j - i
                        break

            # 馬単２着
            for i, exacta2 in enumerate(exacta2_rank):
                for j, win in enumerate(win_rank):
                    if exacta2 == win:
                        if i < j:
                            if exacta2 in point_dict:
                                point_dict[exacta2] += j - i
                                place_dict[exacta2] += j - i
                            else:
                                point_dict[exacta2] = j - i
                                place_dict[exacta2] = j - i
                        break

            # ３連単３着
            for i, tierce3 in enumerate(tierce3_rank):
                for j, win in enumerate(win_rank):
                    if tierce3 == win:
                        if i < j:
                            if tierce3 in point_dict:
                                point_dict[tierce3] += j - i
                                place_dict[tierce3] += j - i
                            else:
                                point_dict[tierce3] = j - i
                                place_dict[tierce3] = j - i
                        break

            # ３連単２着
            for i, tierce2 in enumerate(tierce2_rank):
                for j, win in enumerate(win_rank):
                    if tierce2 == win:
                        if i < j:
                            if tierce2 in point_dict:
                                point_dict[tierce2] += j - i
                                place_dict[tierce2] += j - i
                            else:
                                point_dict[tierce2] = j - i
                                place_dict[tierce2] = j - i
                        break

            # オッズの断層を取得
            win_gap_list = []
            for i, elem in enumerate(odds_dict['win']):
                if i < len(win_rank) - 1:
                    win_gap_list.append(odds_dict['win'][i + 1]['odds'] / elem['odds'])

            place_gap_list = []
            for i, elem in enumerate(odds_dict['place']):
                if i < len(place_rank) - 1:
                    place_gap_list.append(odds_dict['place'][i + 1]['odds'] / elem['odds'])

            win_gap_point = [0] * (len(win_gap_list) + 1)
            for index, win_gap in enumerate(win_gap_list):
                if win_gap > 2:
                    for i in range(index):
                        win_gap_point[i] += 1

            # 単勝が１倍台の馬がいたら購入しない
            win_flag = False
            for win in odds_dict['win']:
                win_odds = win['odds']
                if win_odds < 1:
                    win_flag = True
                    break

            if not win_flag:
                # 単勝辞書を作成
                win_odds_dict = {}
                for win in odds_dict['win']:
                    win_odds_dict[win['number']] = win['odds']
                # 複勝辞書を作成
                place_odds_dict = {}
                for place in odds_dict['place']:
                    place_odds_dict[place['number']] = place['odds']

                # 閾値以上のポイントの馬券を購入
                purchace_win_list = []
                purchace_place_list = []

                # 断層の最大値を取得
                gap_max = max(win_gap_point)
                # 購入しようとしている馬が第1断層に入っているか
                for key in win_dict:
                    if win_dict[key] >= 1:
                        if gap_max > 0:
                            if win_gap_point[win_rank.index(key)] == gap_max:
                                purchace_win_list.append(key)

                # for key in win_dict:
                #     if win_dict[key] >= 2:
                #         purchace_win_list.append(key)
                # for key in tierce1_dict:
                #     if tierce1_dict[key] >= 1:
                #         purchace_win_list.append(key)
                #

                # purchace_place_list.append(max(place_dict, key=place_dict.get))

                # 結果
                result_win_list = []
                for i in range(1):
                    result_win_list.append(int(odds_dict['result'][i]['number']))
                result_place_list = []
                for i in range(3):
                    result_place_list.append(int(odds_dict['result'][i]['number']))

                # 購入したら
                purchace_win_total += len(purchace_win_list) * 100
                purchace_place_total += len(purchace_place_list) * 100
                purchace_total_list.append(purchace_win_total + purchace_place_total)

                # 的中したら
                # 単勝
                for result in result_win_list:
                    for purchase in purchace_win_list:
                        if result == purchase:
                            hit = int(win_odds_dict[purchase] * 100)
                            hit_win_total += hit
                            hit_win_total_list.append(hit_win_total)
                # 複勝
                for result in result_place_list:
                    for purchase in purchace_place_list:
                        if result == purchase:
                            hit = int(place_odds_dict[purchase] * 100)
                            hit_place_total += hit
                            hit_place_total_list.append(hit_place_total)

                print('=============')
                print(file_path)
                print(purchace_win_list)
                print(result_place_list)
                print(win_odds_dict)
                # print(win_gap_point)
                # print(win_rank)
                # print(win_dict)
                # print(purchace_win_list)
                print('購入金額合計：' + str(purchace_win_total + purchace_place_total))
                print('単勝当選金額合計：' + str(hit_win_total) + '(' + str(hit_win_total - purchace_win_total) + ')')
                print('複勝当選金額合計：' + str(hit_place_total) + '(' + str(hit_place_total - purchace_place_total) + ')')

    count += 1

plt.plot(purchace_total_list, label='purchase')
plt.plot(hit_win_total_list, label='win')
plt.plot(hit_place_total_list, label='place')
plt.legend()
plt.show()

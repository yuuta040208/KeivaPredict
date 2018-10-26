import numpy as np
import pandas as pd
import chainer.functions as F
from chainer import Variable

import chainer
import nn


# 設定
LAYER_NUM = 2048
OUTPUT_LAYER_NUM = 2
TRAIN_LENGTH = 20000
DATASET_PATH = './dataset_train.csv'
MODEL_PATH = './model.npz'


# テスト処理
def test(_x, _y, name, model):
    with chainer.using_config('train', False):
        xx = Variable(_x.values.astype(np.float32))
        pred = model(xx)

        # クラス確率を算出
        pred = F.softmax(pred)
        pred_label = np.argmax(pred.data, 1)

        # if name != 'pred':
        #     acc = np.sum(pred_label == _y['rank']) / np.sum(_y['rank'])
        #     print(acc)
        # else:
        #     print(pred_label)

        if name != 'pred':
            # 正答率を計算
            tp = fp = fn = tn = 1
            for i, label in enumerate(pred_label):
                if label == 1 and _y.iat[i, 0] == 1:
                    tp = tp + 1
                elif label == 1 and _y.iat[i, 0] == 0:
                    fp = fp + 1
                elif label == 0 and _y.iat[i, 0] == 1:
                    fn = fn + 1
                elif label == 0 and _y.iat[i, 0] == 0:
                    tn = tn + 1

            precision = tp / (tp + fp)
            recall = tp / (tp + fn)
            fscore = (2 * precision * recall) / (precision + recall)
            print('＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝')
            print('精度： ' + str(precision))
            print('再現率： ' + str(recall))
            print('F値： ' + str(fscore))

            # もろもろ評価
            pred_zero = np.sum(pred_label == 0)
            pred_one = np.sum(pred_label == 1)
            print('0と予測： ' + str(pred_zero))
            print('1と予測： ' + str(pred_one))

            act_zero = np.sum(_y['rank'] == 0)
            act_one = np.sum(_y['rank'] == 1)
            print('実測が0： ' + str(act_zero))
            print('実測が1： ' + str(act_one))

            # 的中の詳細
            if name == 'train':
                csv = pd.read_csv(DATASET_PATH, engine='python')
                csv = csv[0:TRAIN_LENGTH]
                for i, label in enumerate(pred_label):
                    if label == 1 and _y.iat[i, 0] == 1:
                        print(csv.iat[i, 15])
            elif name == 'test':
                csv = pd.read_csv(DATASET_PATH, engine='python')
                csv = csv[TRAIN_LENGTH + 1:len(csv)]
                for i, label in enumerate(pred_label):
                    if label == 1 and _y.iat[i, 0] == 1:
                        print(csv.iat[i, 15])

        else:
            print(pred)


def main():
    # CSVファイルを読込
    csv = pd.read_csv('./' + DATASET_PATH, engine='python')

    # データをx(入力値)とy(出力値)に分割する
    x = pd.DataFrame()
    y = pd.DataFrame()
    for i, key in enumerate(csv.columns):
        if i == 0:
            y[key] = csv[key]
        else:
            x[key] = csv[key]

    # スケーリングしない場合
    # ax = x
    ay = y

    # 標準化する場合
    ax = (x - x.mean()) / x.std()
    # ay = (y - y.mean()) / y.std()

    # x, yを教師データとテストデータに分割する
    train_len = TRAIN_LENGTH
    train_x = train_y = test_x = test_y = pd.DataFrame()

    train_x = ax[0:train_len]
    train_y = ay[0:train_len]
    test_x = ax[train_len + 1:len(x)]
    test_y = ay[train_len + 1:len(y)]

    # indexを修正
    train_x = train_x.reset_index()
    train_y = train_y.reset_index()
    del train_x['index']
    del train_y['index']
    test_x = test_x.reset_index()
    test_y = test_y.reset_index()
    del test_x['index']
    del test_y['index']

    model = nn.MLP(LAYER_NUM, OUTPUT_LAYER_NUM)
    chainer.serializers.load_npz(MODEL_PATH, model)

    # テストを実行
    test(train_x, train_y, 'train', model)
    test(test_x, test_y, 'test', model)


if __name__ == "__main__":
    main()

import configparser
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import codecs
import json
import chainer
import chainer.functions as F
from chainer import optimizers, Variable

import nn
from test_odds import test

# ConfigParserの設定
inifile = configparser.ConfigParser()
inifile.read('./config.ini', 'UTF-8')

# ハイパーパラメータ
BATCH_SIZE = int(inifile.get('basic', 'batch_size'))
EPOCH_SIZE = int(inifile.get('basic', 'epoch_size'))
LAYER_NUM = int(inifile.get('basic', 'hidden_layer'))
OUTPUT_LAYER_NUM = int(inifile.get('basic', 'output_layer'))
LEARNING_RATE = float(inifile.get('basic', 'learning_rate'))
TRAIN_LENGTH = int(inifile.get('basic', 'train_length'))

# 設定
DATASET_PATH = inifile.get('basic', 'dataset_path')
MODEL_PATH = inifile.get('basic', 'model_path')


# メイン処理
def main():
    # 学習処理
    def train(batch_size, epoch_size):
        np.random.seed(seed=4)

        loss_log = []

        for epoch in range(epoch_size):
            # ミニバッチ処理
            sffindx = np.random.permutation(train_len)

            for i in range(0, train_len, batch_size):
                xx = Variable(train_x.iloc[sffindx[i:(i + batch_size)],
                              range(len(train_x.columns))].values.astype(np.float32))
                yy = Variable(train_y.iloc[sffindx[i:(i + batch_size)],
                              range(len(train_y.columns))].values.astype(np.int32).flatten())

                model.cleargrads()
                pred_y = model(xx)

                loss = F.softmax_cross_entropy(pred_y, yy)
                loss.backward()
                optimizer.update()

                loss_log.append(loss.data)

            print(str(epoch + 1) + '/' + str(epoch_size) + ' ステップ完了')
            print('  loss = ' + str(loss_log[epoch]))

        plt.plot(loss_log)
        plt.show()

    # CSVファイルを読込
    csv = pd.read_csv(DATASET_PATH, engine='python')

    # データをx(入力値)とy(出力値)に分割する
    x = pd.DataFrame()
    y = pd.DataFrame()
    for i, key in enumerate(csv.columns):
        if i == 1:
            y[key] = csv[key]
        else:
            x[key] = csv[key]

    print(csv.corr()['rank'])

    # スケーリングしない場合
    ax = x
    ay = y

    # 標準化する場合
    # ax = (x - x.mean()) / x.std()
    # ay = (y - y.mean()) / y.std()

    # x, yを教師データとテストデータに分割する
    train_len = TRAIN_LENGTH
    train_x = train_y = test_x = test_y = pd.DataFrame()
    # 前半のデータを教師データとする場合
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

    # Optimizerの設定
    model = nn.MLP(LAYER_NUM, OUTPUT_LAYER_NUM)
    optimizer = optimizers.Adam(alpha=LEARNING_RATE)
    optimizer.setup(model)

    # 学習を実行
    train(BATCH_SIZE, EPOCH_SIZE)
    chainer.serializers.save_npz(MODEL_PATH, model)

    # テストを実行
    test(train_x, train_y, 'train', model)
    test(test_x, test_y, 'test', model)


if __name__ == "__main__":
    main()

import pandas as pd
import chainer

import nn
from test import test


# ハイパーパラメータ
LAYER_NUM = 2048
OUTPUT_LAYER_NUM = 2
DATASET_PATH = './dataset_predict.csv'
MODEL_PATH = './model.npz'


# メイン処理
def main():
    # 予測データの読込
    csv_predict = pd.read_csv(DATASET_PATH, engine='python')

    x_predict = pd.DataFrame()
    for i, key in enumerate(csv_predict.columns):
        x_predict[key] = csv_predict[key]

    ax_predict = (x_predict - x_predict.mean()) / x_predict.std()

    model = nn.MLP(LAYER_NUM, OUTPUT_LAYER_NUM)
    chainer.serializers.load_npz(MODEL_PATH, model)

    # テストを実行
    test(ax_predict, ax_predict, 'pred', model)


if __name__ == "__main__":
    main()

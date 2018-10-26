import chainer.functions as F
import chainer.links as L
from chainer import Chain


# レイヤを定義
class MLP(Chain):
    def __init__(self, n_units, n_out):
        super().__init__()

        with self.init_scope():
            self.l1 = L.Linear(None, n_units)
            self.l2 = L.Linear(None, n_units)
            self.l3 = L.Linear(None, n_units)
            self.l4 = L.Linear(None, n_units)
            self.l5 = L.Linear(None, n_units)
            self.l6 = L.Linear(None, n_units)
            self.l7 = L.Linear(None, n_units)
            self.l8 = L.Linear(None, n_units)
            self.l9 = L.Linear(None, n_units)
            self.l10 = L.Linear(None, n_out)

    def __call__(self, x):
        h1 = F.relu(self.l1(x))
        h2 = F.relu(self.l2(h1))
        h3 = F.relu(self.l3(h2))
        h4 = F.relu(self.l4(h3))
        h5 = F.relu(self.l5(h4))
        h6 = F.relu(self.l6(h5))
        h7 = F.relu(self.l7(h6))
        h8 = F.relu(self.l8(h7))
        h9 = F.relu(self.l9(h8))
        return self.l10(h9)

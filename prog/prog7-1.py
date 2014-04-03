# -*- coding: utf-8 -*-
from numpy import *
from scipy import linalg as LA
from matplotlib.pyplot import *

N = 50

D = 1   # 入力の次元
M = 3   # 隠れ層の数
K = 1   # 出力層の数

ALPHA = 0.3       # 最急降下法の勾配係数
ITER_MAX = 5000   # 最急降下法の反復回数上限
ITER_EPS = 5.0e-2 # 再急降下法の停止パラメータ

#=== 重みパラメータ ===
# 隠れ層の重みは M*(D+1) 行列w1で表現.
# 出力層の重みは K*(M+1) 行列w2で表現.
#
# w1[i, j] はj番目の入力と隠れ層のi番目の素子の間の重み.
# w2[i, j] は隠れ層のj番目素子と出力層のi番目の素子の間の重み.

#=== 順伝播 ===
# 入力 x に対して各素子への入力を計算する.
# 出力はタプル (a1, a2) であり,
# a1[i]が隠れ層の素子 i への入力, a2[i]が出力層の素子 i への入力

def forward(x, w1, w2):
    a1 = w1.dot([x, 1])         # 隠れ層への入力
    a2 = w2.dot(append(tanh(a1), 1))  # 出力層への入力
    return (a1, a2)

#=== 誤差逆伝播法 ===
# 各重みに関する偏微分係数を計算
def backpropagation(x, t, w1, w2):
    a1, a2 = forward(x, w1, w2)  # 順伝播
    delta2 = a2 - t              # 出力の誤差
    delta1 = (1- tanh(a1)**2)*w2[:,0:M].T.dot(delta2) # 隠れ層の誤差

    ## 偏微分係数の計算
    diff1 = zeros((M, D+1))
    diff2 = zeros((K, M+1))

    # 隠れ層
    for i in range(D+1):
        for j in range(M):
            if i == 0:
                diff1[j,i] = delta1[j]*x
            else:
                diff1[j,i] = delta1[j]

    # 出力層
    for i in range(M+1):
        for j in range(K):
            if i < M:
                diff2[j,i] = tanh(a1[i])*delta2[j]
            else:
                diff2[j,i] = delta2[j]

    return (diff1, diff2)

#=== 最急勾配降下法
def fit(outname, expr, f):
    print expr
    x = linspace(-1, 1, N)
    t = vectorize(f)(x)

    w1 = random.uniform(-1, 1, (M, D+1))
    w2 = random.uniform(-1, 1, (K, M+1))
    for i in range(ITER_MAX):
        finish = True
        for j in range(N):
            d1, d2 = backpropagation(x[j], t[j], w1, w2)
            w1 -= ALPHA*d1
            w2 -= ALPHA*d2
            if LA.norm(d1) >= ITER_EPS or LA.norm(d2) >= ITER_EPS:
                finish = False
        if finish: break
    count = i

    test_x = linspace(-1, 1, N)
    test_y = vectorize(lambda x: forward(x, w1, w2)[1][0])(test_x)

    xlim(-1, 1)
    scatter(x, t)
    plot(test_x, test_y)
    title("%s (iteration=%d)" % (expr, count))
    savefig("fig7-1-%s.png" % outname)
    clf()

fit("quadratic", "y=x^2", lambda x: x**2)
fit("sin", u"y=sin(πx)", lambda x: sin(pi*x))
fit("abs", "y=|x|", abs)

def heaviside(x):
    if x < 0:
        return 0
    else:
        return 1

fit("heaviside", "y=H(x) (Heaviside function)", heaviside)
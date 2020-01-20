# -*- coding: utf-8 -*-
"""...
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    plt.close('all')
    ts = pd.Series(np.random.randn(365), index = pd.date_range('1/1/2019', periods=365))
    df = pd.DataFrame(np.random.randn(365, 4), index = ts.index, columns = list('ABCD'))
    df = df.cumsum()
    # plt.figure()
    df.plot()
    plt.show()
    print('Ok')
    return


if __name__ == '__main__':
    main()
    print('main - done')
import numpy as np

def fun(x):
    if len(x)<4:
        return 8
    else:
        return int(x[:2])

def percentile(n):
    def percentile_(x):
        return np.percentile(x, n)
    percentile_.__name__ = 'percentile_%s' % n
    return percentile_
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


stones = ['Basalt',
                      'Limestone',
                      'Shale',
                      'Sand',
                      'Granite',
                      'Marble',
                      'Alabaster']
woods = ['Redwood',
                    'Pine',
                    'Willow',
                    'Olive',
                    'Oak',
                    'Ash',
                    'Holly']
gems = ['Ruby',
                    'Sapphire',
                    'Emerald',
                    'Topaz',
                    'Smoky Quartz',
                    'Amethyst',
                    'Diamond']
els = ['Sulfur',
                      'Hydrogen',
                      'Carbon',
                      'Nitrogen',
                      'Calcium',
                      'Silicon',
                      'Antimony']
fabrics = ['Flax',
                      'Silk',
                      'Jute',
                      'Hemp',
                      'Cotton',
                      'Cashmere',
                      'Wool']

met = ['Zinc',
                      'Tungsten',
                      'Tin',
                      'Copper',
                      'Iron',
                      'Aluminum',
                      'Titanium']

def categorise(row):
    if row['Deposits'] in stones:
        return 'Stones'
    elif row['Deposits'] in woods:
        return 'Woods'
    elif row['Deposits'] in gems:
        return 'Gems'
    elif row['Deposits'] in els:
        return 'Elements'
    elif row['Deposits'] in fabrics:
        return 'Fabrics'
    return 'Metals'
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


dict_elem = {'Ash': 0,
 'Holly': 0,
 'Oak': 0,
 'Olive': 0,
 'Pine': 0,
 'Redwood': 0,
 'Willow': 0,
 'Alabaster': 0,
 'Basalt': 0,
 'Granite': 0,
 'Limestone': 0,
 'Marble': 0,
 'Sand': 0,
 'Shale': 0,
 'Cashmere': 0,
 'Cotton': 0,
 'Flax': 0,
 'Hemp': 0,
 'Jute': 0,
 'Silk': 0,
 'Wool': 0,
 'Aluminum': 0,
 'Copper': 0,
 'Iron': 0,
 'Tin': 0,
 'Titanium': 0,
 'Tungsten': 0,
 'Zinc': 0,
 'Amethyst': 0,
 'Diamond': 0,
 'Emerald': 0,
 'Ruby': 0,
 'Sapphire': 0,
 'Smoky Quartz': 0,
 'Topaz': 0,
 'Antimony': 0,
 'Calcium': 0,
 'Carbon': 0,
 'Hydrogen': 0,
 'Nitrogen': 0,
 'Silicon': 0,
 'Sulfur': 0}
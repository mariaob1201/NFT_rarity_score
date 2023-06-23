# plots_ararity_score
Provides an score on [0, 100] points based on rarity of an item on a collection.

The idea is to provide an score on specific items to measure how rare they are based on its attributes. At the end, the items are NFT's that can be exchanged on secondary markets. Each item has own attributes based on an external game design. The idea here is then:

1. Chose a measurement on such attributes: the number of sub-items per family the item has.
2. The intensity on each sub-item.
3. Given a weighted score combining both measurements.

From a technological point of view, this tool reads an input from AWS and returns a new one on s3.

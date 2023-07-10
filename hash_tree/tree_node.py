class TreeNode:
    """
    Node structure for hash tree.

    Reference: https://github.com/Chang-Chia-Chi/Apriori-Hash-Tree
    :ivar bucket: A dictionary of hash bucket whose keys are itemsets and values are support count.
    :ivar children: A dictionary of child tree node whose keys are hash value and values are TreeNodes.
    :ivar isleaf: Boolean, indicating whether the tree node is leaf node.
    :ivar index: An integer that determines the element to be hashed.

    """
    __slots__ = ("bucket", "children", "isleaf", "index")

    def __init__(self):
        self.bucket = {}
        self.children = {}
        self.isleaf = True
        self.index = 0

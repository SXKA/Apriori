from tree_node import TreeNode


class HashTree:
    """
    Hash tree class for frequent itemset generation.

    Reference: https://github.com/Chang-Chia-Chi/Apriori-Hash-Tree
    :ivar _hash_func: The hash function of hash tree.
    :ivar _itemset_size: The size of candidate itemset is used to bound transaction subset size.
    :ivar _max_bucket_size: The max size of bucket is used to split.
    :ivar _max_children_size: The max size of children is used to hash.
    :ivar _root: The root of hash tree.
    :ivar _updated: The set of tree nodes already updated, used to avoid duplicate updates.
    """

    def __init__(self, itemset_size, max_bucket_size, max_children_size):
        """
        HashTree(itemset_size, max_bucket_size, max_children_size) -> new HashTree object
        :param itemset_size: The size of candidate itemset is used to bound transaction subset size.
        :param max_bucket_size: The max size of bucket is used to split.
        :param max_children_size: The max size of children is used to hash.
        """
        self._hash_func = lambda x: x % self._max_children_size
        self._itemset_size = itemset_size
        self._max_bucket_size = max_bucket_size
        self._max_children_size = max_children_size
        self._root = TreeNode()
        self._root.isleaf = False
        self._updated = set()

    def _insert(self, tree_node, itemset):
        """
        Insert tree node to hash tree recursively, if the bucket of tree node is full then split.
        :param tree_node: The parent tree node.
        :param itemset: The itemset to be inserted.
        """
        if tree_node.isleaf:
            tree_node.bucket[itemset] = 0

            if len(tree_node.bucket) > self._max_bucket_size:
                tree_node.index += 1

                for old_itemset in tree_node.bucket:
                    key = self._hash_func(old_itemset[tree_node.index])

                    tree_node.children.setdefault(key, TreeNode())
                    tree_node.children[key].index = min(tree_node.index, len(old_itemset) - 1)

                    self._insert(tree_node.children[key], old_itemset)

                tree_node.bucket.clear()
                tree_node.isleaf = False
        else:
            key = self._hash_func(itemset[tree_node.index])

            tree_node.children.setdefault(key, TreeNode())

            self._insert(tree_node.children[key], itemset)

    def _update(self, tree_node, pick, rest):
        """
        Update the support count of hash tree recursively by checking the transaction subset is superset of the itemset.
        :param tree_node: The tree node to be updated.
        :param pick: Itemset have been picked.
        :param rest: Itemset haven't been picked.
        """
        if tree_node.isleaf:
            for itemset in tree_node.bucket:
                if itemset not in self._updated and set(pick + rest).issuperset(itemset):
                    tree_node.bucket[itemset] += 1

                    self._updated.add(itemset)
        else:
            rest_size = len(rest)
            min_rest_size = self._itemset_size - len(pick) - 1

            if min_rest_size >= 0:
                for i in range(rest_size - min_rest_size):
                    curr_pick = pick + [rest[i]]
                    curr_rest = rest[i + 1:]

                    key = self._hash_func(curr_pick[tree_node.index])

                    if key in tree_node.children:
                        self._update(tree_node.children[key], curr_pick, curr_rest)

    def build(self, candidate):
        """
        Build a candidate hash tree.
        :param candidate: The candidate of frequent itemset.
        """
        for itemset in candidate:
            self._insert(self._root, itemset)

    def update_support_count(self, transaction):
        """
        Update the support count of hash tree.
        :param transaction: A transaction record.
        """
        self._update(self._root, [], list(transaction))
        self._updated.clear()

    def find_freq_itemset(self, min_support_count):
        """
        Find and return frequent itemset by using DFS.
        :param min_support_count: Minimum support count.
        :return: Frequent itemset.
        """
        freq_itemset = set()
        stack = [self._root]

        while stack:
            tree_node = stack.pop()

            if tree_node.isleaf:
                for itemset, count in tree_node.bucket.items():
                    if count >= min_support_count:
                        freq_itemset.add(frozenset(itemset))
            else:
                stack.extend(tree_node.children.values())

        return freq_itemset

class AprioriCodec:
    """
    Encoder/Decoder class for the Apriori algorithm.
    :ivar _encode_dict: A dictionary whose keys are items and values are IDs.
    :ivar _decode_dict: A dictionary whose keys are IDs and values are items.
    """

    def __init__(self):
        self._encode_dict = {}
        self._decode_dict = {}

    def encode(self, transactions):
        """
        Encode the items of transaction data into a set of integers.
        :param transactions: Transaction data.
        :return: Encoded transaction data.
        """
        encoded_transaction = []

        for transaction in transactions:
            encoded_transaction.append(set())

            for item in transaction:
                if item not in self._encode_dict:
                    self._encode_dict[item] = len(self._encode_dict)
                    self._decode_dict[len(self._decode_dict)] = item

                encoded_transaction[-1].add(self._encode_dict[item])

            encoded_transaction[-1] = frozenset(encoded_transaction[-1])

        return tuple(encoded_transaction)

    def decode(self, freq_itemsets):
        """
        Decode the integers of all frequent itemset into a set of items.
        :param freq_itemsets: All frequent itemset.
        :return: All Decoded frequent itemset.
        """
        decode_freq_itemsets = []

        for freq_itemset in freq_itemsets:
            decode_freq_itemsets.append(set())

            for itemset in freq_itemset:
                decode_freq_itemsets[-1].add(frozenset({self._decode_dict[item] for item in itemset}))

        return tuple(decode_freq_itemsets)

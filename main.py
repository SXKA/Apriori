from time import time

from matplotlib import pyplot as plt

from codec.aprior_codec import AprioriCodec
from hash_tree.hash_tree import HashTree


def main():
    transactions = {}

    for record in parse("Music.txt"):
        user_id, product_id_set = record.popitem()

        transactions.setdefault(user_id, set()).add(product_id_set)

    apriori_codec = AprioriCodec()
    transactions = apriori_codec.encode(tuple(frozenset(product_id_set) for product_id_set in transactions.values()))
    freq_itemsets = None
    exec_time_list = []
    min_supports = (0.0003, 0.0006, 0.0009)

    for min_support in min_supports:
        freq_itemsets, exec_time = apriori(transactions, min_support)

        exec_time_list.append(exec_time / 60)

    freq_itemsets = apriori_codec.decode(freq_itemsets)

    print("The amount of frequent itemset having at least 3 items: {}".format(
        sum(len(freq_itemset) for freq_itemset in freq_itemsets[2:])))

    top_10_freq_itemsets = [sorted(itemset) for freq_itemset in reversed(freq_itemsets) for itemset in
                            freq_itemset][:10]
    top_10_freq_itemsets = sorted(top_10_freq_itemsets, key=lambda x: (-len(x), x))

    print("The top-10 longest frequent itemsets: {}".format(top_10_freq_itemsets))

    plt.title("Execution Time at Different Minimum Support Levels")
    plt.xlabel("Minimum support")
    plt.xticks(range(len(min_supports)), min_supports)
    plt.ylabel("Execution time (min)")
    plt.plot(exec_time_list, marker='.')
    plt.show()


def measure_time(func):
    """
    Measure the execution time of input function.
    :param func: The function to be measured.
    :return: A tuple of function output and execution time.
    """

    def wrapper(*args, **kwargs):
        """
        Wrap the input function.
        :param args: Positional arguments.
        :param kwargs: Keyword arguments.
        :return: A tuple of function output and execution time.
        """
        begin_time = time()
        result = func(*args, **kwargs)
        end_time = time()

        return result, end_time - begin_time

    return wrapper


def parse(filename):
    """
    Parse a text file into a generator of dictionary and return it.
    :param filename: Text file name.
    :return: A dictionary of transaction record whose keys are user IDs and values are product ID sets.
    """
    record = {}

    with open(filename) as data:
        for line in data:
            line = line.strip()
            colon_pos = line.find(':')

            if colon_pos != -1:
                key = line[:colon_pos]
                value = line[colon_pos + 2:]

                if key == "product/productId":
                    last_product_id = value
                elif key == "review/userId" and value != "unknown":
                    record[value] = last_product_id
            elif record:
                yield record

                record = {}


@measure_time
def apriori(transactions, min_support):
    """
    Frequent itemset generation of the Apriori algorithm.
    :param transactions: Transaction data.
    :param min_support: Minimum support.
    :return: All frequent itemset.
    """
    candidate = {}
    min_support_count = int(min_support * len(transactions))

    for transaction in transactions:
        for item in transaction:
            candidate.setdefault(item, 0)
            candidate[item] += 1

    transactions = tuple(tuple(sorted(transaction)) for transaction in transactions)
    freq_itemsets = [{frozenset({item}) for item, support_count in candidate.items() if
                      support_count >= min_support_count}]

    while True:
        candidate = candidate_gen(freq_itemsets[-1])
        candidate = candidate_prune(candidate, freq_itemsets[-1])
        candidate = {tuple(sorted(itemset)) for itemset in candidate}
        candidate_size = len(candidate)

        if not candidate_size:
            break

        itemset_size = len(next(iter(candidate)))
        hash_tree = HashTree(itemset_size, candidate_size, candidate_size)
        hash_tree.build(candidate)

        for transaction in transactions:
            if len(transaction) >= itemset_size:
                hash_tree.update_support_count(transaction)

        freq_itemsets.append(hash_tree.find_freq_itemset(min_support_count))

    return freq_itemsets


def candidate_gen(freq_itemset):
    """
    Candidate generation of the Apriori algorithm by using Fk-1 x Fk-1 method.
    :param freq_itemset: An itemset whose support is greater than or equal to a minimum support.
    :return: The candidate of next frequent itemset.
    """
    freq_itemset_list = list(freq_itemset)

    return {x | y for i, x in enumerate(freq_itemset_list) for y in freq_itemset_list[i + 1:] if len(x - y) == 1}


def candidate_prune(candidate, freq_itemset):
    """
    Candidate prune of the Apriori algorithm.
    :param candidate: The candidate of frequent itemset.
    :param freq_itemset: An itemset whose support is greater than or equal to a minimum support.
    :return: The candidate after prune.
    """
    return {itemset for itemset in candidate if all(itemset - frozenset({item}) in freq_itemset for item in itemset)}


if __name__ == "__main__":
    main()

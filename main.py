import csv

# this dictionary will include all candidate itemsets to calcualte strong rules later
candidate_item_sets = {}


# convert csv file into dictionaries
def convert_csv_dictionaries(csv_file_name):
    f = open(csv_file_name, 'r')
    reader = csv.reader(f)
    item_sets = {}
    for row in reader:
        item_sets[row[0]] = set(row[1].split(","))
    item_sets.pop(next(iter(item_sets)))
    return item_sets


def get_candidate_item_sets(item_sets, item_set_length, count, min_support=2):
    # get all keys in a list
    all_keys = list(item_sets.keys())
    count = 0
    items_length = len(all_keys)
    if (item_set_length == 0):
        for i in range(0, items_length):
            item_length = len(item_sets[all_keys[i]])
            if (item_length >= min_support):
                count = count + 1
                candidate_item_sets[all_keys[i]] = item_sets[all_keys[i]]

    # if length of itemsets is 1 , then you can join every two keys
    if (item_set_length == 1):
        for i in range(0, items_length):  # trying to join rows to get all possibiliteies
            for j in range(i + 1, items_length):
                intersect = item_sets[all_keys[i]].intersection(item_sets[all_keys[j]])
                if (len(intersect) >= min_support):
                    count = count + 1
                    new_key = all_keys[i] + ',' + all_keys[j]
                    candidate_item_sets[new_key] = intersect
    elif (item_set_length > 1):
        for i in range(0, items_length):  # trying to join rows to get all possibiliteies
            for j in range(i + 1, items_length):
                i_keysplit = all_keys[i].rsplit(',', 100)
                j_keysplit = all_keys[j].rsplit(',', 100)
                if (len(i_keysplit) == item_set_length and len(j_keysplit) == item_set_length):
                    if (all_keys[i].rsplit(',', 1)[0] == all_keys[j].rsplit(',', 1)[0]):
                        intersect = item_sets[all_keys[i]].intersection(item_sets[all_keys[j]])
                        if (len(intersect) >= min_support):
                            count = count + 1
                            new_key = ','.join(dict.fromkeys((all_keys[i] + ',' + all_keys[j]).split(
                                ',')))  # joining two keys with repsect to order and keeping it unique
                            candidate_item_sets[new_key] = intersect

    if (count <= 1):
        return
    get_candidate_item_sets(candidate_item_sets, item_set_length + 1, count, min_support)


# calculate strong roles
def get_strong_rules(min_support):
    candidate_strong_rules = {}
    all_keys = list(candidate_item_sets.keys())

    for i in range(0, len(candidate_item_sets)):
        key_split_length = len(all_keys[i].rsplit(',', 100))
        if (key_split_length > 1):
            key_split = all_keys[i].rsplit(',', 1)  # separate two keys for example : 'Milk,Cheese' -> 'Milk' , 'Cheese'
            # calculate support = number of all transactions that contains the current itemset / number of transactoins of the first split
            fisrt_sup = len(candidate_item_sets[all_keys[i]]) / len(candidate_item_sets[key_split[0]])
            second_sup = len(candidate_item_sets[all_keys[i]]) / len(candidate_item_sets[key_split[1]])
            if (fisrt_sup >= min_support):
                new_key = key_split[0] + '->' + key_split[1]
                candidate_strong_rules[new_key] = fisrt_sup

            if (second_sup >= min_support):
                new_key = key_split[1] + '->' + key_split[0]
                candidate_strong_rules[new_key] = second_sup

    return candidate_strong_rules


def eclat_algorithm(csv_file_name, min_support):
    item_sets = convert_csv_dictionaries(csv_file_name)
    min_support_number = int(min_support * len(item_sets))
    get_candidate_item_sets(item_sets, 0, min_support_number)
    print('Candidate Item sets')
    print(candidate_item_sets)
    print('=========================================')
    candidate_strong_rules = get_strong_rules(min_support)
    print('Strong Rules')
    print(candidate_strong_rules)


eclat_algorithm('eclat_vertical_dataset.csv', 1 / 3)





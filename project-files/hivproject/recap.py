

from project1_solution import *



def predict_subtype(unknown):
    max_similarities_dict = get_all_similarities(unknown)

    value_list = []
    subtype_list = []
    for subtype in max_similarities_dict:
        subtype_list.append(subtype)
        value_list.append(max_similarities_dict[subtype])

    max_value = 0
    index_of_max = 0
    for i in range(len(value_list)):
        if value_list[i] > max_value:
            max_value = value_list[i]
            index_of_max = i

    return subtype_list[index_of_max]


print('Prediction: {}'.format(predict_subtype(unknown_list[0])))
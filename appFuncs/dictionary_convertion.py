def seperate_col_val(data_list, num_of_features):
    cols = []
    vals = []
    for i in range(len(data_list)):
        data_list[i] = data_list[i].split(':', 1)

    for i in range(len(data_list)):
        vals.append(data_list[i][1])
    for i in range(num_of_features):
        cols.append(data_list[i][0])

    return cols, vals

def create_dictionaries(cols, vals, num_of_features):
    num_of_dicts = len(cols)/num_of_features
    dict_names = []
    dicts = []
    c = 0
    while c < num_of_dicts:
        j = c*num_of_features
        dict_names.append(vals[j])
        c = c+1

    temp = dict.fromkeys(cols[0:num_of_features])

    if dict_names is not None:
        c = 0
        for name in dict_names:
            name = temp.copy()
            for i in range(num_of_features):
                j = c*num_of_features
                name[cols[j+i]] = vals[j+i]
            dicts.append(name)
            c = c+1

    return dicts[0]

def data_dict(data_list, col_labels):
    num_of_features = len(col_labels)
    cols, vals = seperate_col_val(data_list, num_of_features)
    dictionary = create_dictionaries(cols, vals, num_of_features)
    return dictionary
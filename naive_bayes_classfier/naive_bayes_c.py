def pre_process_sample(sample,labels):
    labels_set = set(labels)
    features = set(sample.columns)
    P_label_dict = {}
    P_l_f_dict = {}
    for label in list(labels_set):
        label_count = labels.count(label)
        P_label_dict[label] = float(label_count)/len(labels)
        for fea in list(features):
            l_f_count = len(sample[sample.loc[[True if i == label else False for i in labels ],fea] == 1])
            P_l_f_dict[(fea,label)] = float(l_f_count)/len(label_count)
    return P_l_f_dict,P_label_dict


def predict(sample,P_l_f_dict,P_label_dict):

    labels = []
    for row in list(sample.index):
        compare = []
        for label in P_label_dict.keys():
            v = P_label_dict[label]
            for fea in list(sample.columns):
                if sample.loc[row,fea] == 1:
                    v = v * P_l_f_dict[(fea,label)]
            compare.append((v,label))
        labels.append(max(compare)[1])
    return labels


if __name__ == '__main__':
    P_l_f_dict, P_label_dict = pre_process_sample(sample,labels)


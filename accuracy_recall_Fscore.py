# author: houda.najeh@imt-atlantique.fr
""
" import librairies "
""
import datetime
import fonction_union_intersection

def _inter(interv1: list, interv2: list): #calculate the intersection between two intervals
    if interv2[0] < interv1[0]:
        interv1, interv2 = interv2, interv1
    if interv1[-1] < interv2[0]:
        return None
    if interv2[0] > interv1[0] and interv2[-1] < interv1[-1]:
        return interv2
    return [interv2[0], interv1[-1]]

def inter(interv_set: list): #calculate the intersection between a set of intervals
    for i in range(len(interv_set) - 1):
        for j in range(i + 1, len(interv_set)):
            intersection = _inter(interv_set[i], interv_set[j])
            if intersection is not None:
                interv1 = interv_set.pop(i)
                interv2 = interv_set.pop(j - 1)
                interv_set.append(_inter(interv1, interv2))
                return inter(interv_set)
            else:
                return None
    return interv_set

def true_positive(seg1, seg2):
    " TP represents the intersection between intervals "
    TP = fonction_union_intersection.inter([seg1, seg2])
    print('TP=', TP)
    delta_TP_in_sec = abs(((TP[0])[-1]-(TP[0])[0]).total_seconds())
    print('delta_TP_in_sec=', delta_TP_in_sec)
    return delta_TP_in_sec


def false_positive(seg1, seg2):
    " FP represents the false positive (samples estimated in advance) "
    inf_bound_seg1 = ([seg1[0]])[0]
    inf_bound_seg2 = ([seg2[0]])[0]
    print('inf_bound_seg1=', inf_bound_seg1)
    print('inf_bound_seg2=', inf_bound_seg2)
    delta_FP_in_sec = abs((inf_bound_seg2-inf_bound_seg1).total_seconds())
    return delta_FP_in_sec

def false_negative(seg1, seg2):
    " FN represents the false positive (samples estimated with a delay) "
    sup_bound_seg1 = ([seg1[-1]])[-1]
    sup_bound_seg2 = ([seg2[-1]])[-1]
    print('sup_bound_seg1=', sup_bound_seg1)
    print('sup_bound_seg2=', sup_bound_seg2)
    delta_FN_in_sec = abs((sup_bound_seg2-sup_bound_seg1).total_seconds())
    return delta_FN_in_sec



def accuracy(seg1, seg2):
    num = true_positive(seg1, seg2)
    denom = true_positive(seg1, seg2) + false_positive(seg1, seg2)
    P = num/denom
    return P

def recall(seg1, seg2):
    num = true_positive(seg1, seg2)
    denom = true_positive(seg1, seg2) + false_negative(seg1, seg2)
    R = num/denom
    return R

def Fscore(seg1, seg2):
    P = accuracy(seg1, seg2)
    R = recall(seg1, seg2)
    num = 2*P*R
    denom = P+R
    F_score = num / denom
    return F_score
if __name__ == '__main__':
    "example of two segments"
    seg1 = (datetime.datetime(2010, 11, 6, 20, 26, 53), datetime.datetime(2010, 11, 6, 23, 26, 59))
    seg2 = (datetime.datetime(2010, 11, 6, 20, 25, 50), datetime.datetime(2010, 11, 6, 23, 23, 00))

    print('res_TP=', true_positive(seg1, seg2))
    print('res_FP=', false_positive(seg1, seg2))
    print('res_FN=', false_negative(seg1, seg2))
    print('accuracy=', accuracy(seg1, seg2))
    print('recall=', recall(seg1, seg2))
    print('Fscore=', Fscore(seg1, seg2))

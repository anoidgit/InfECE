import numpy as np
import argparse

from utils import *
from calibration_utils import *


def parse_args():
    parser = argparse.ArgumentParser(description="Prepare the gap and acc in each bin to plot reliability diagram")
    parser.add_argument("--prob", default="prob.txt")
    parser.add_argument("--trans", default="trans.txt")
    parser.add_argument("--label", default="label.txt")
    parser.add_argument("--vocabulary", default="vocab.en.txt")
    parser.add_argument("--bins", type=int, default=10)

    return parser.parse_args()


def main(args):
    prob = file2words(args.prob, chain=True)
    trans = file2words(args.trans, chain=True)
    label = file2words(args.label, chain=True)

    prob = [np.exp(float(p)) for p in prob]
    float_label = []
    for ll in label:
        if ll == 'C' or ll == '1' or ll == '1.0':
            float_label.append(1.0)
        else:
            float_label.append(0.0)
    vocab = load_vocab(args.vocabulary)

    err_mtrx, hit_mtrx, _, count_mtrx = error_matrix(prob, trans, float_label, vocab, bins=args.bins)

    infece = calculate_ece(err_mtrx, count_mtrx)

    print("{:.4f}\t{:.4f}\t{:.4f}".format(infece, np.mean(prob), np.mean(float_label)))

    acc_list, gap_list, count_list = extract_bin_info(hit_mtrx, count_mtrx)

    for i in range(args.bins):
        print("{:.4f}\t{:.4f}\t{}".format(acc_list[i], gap_list[i], count_list[i]))


if __name__ == '__main__':
    main(parse_args())
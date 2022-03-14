import logging
import os
# from sacremoses import MosesTokenizer, MosesDetokenizer
import argparse

logger = logging.getLogger()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir", type=str, required=True, help="directory of the corpus")
    parser.add_argument("--output_dir", type=str, required=True, help="directory of the output")
    parser.add_argument("--corpus_name", type=str, required=True, help="corpus name without")
    parser.add_argument("--src", type=str, required=True, help="source language name in short as filename extention")
    parser.add_argument("--tgt", type=str, required=True, help="target language name in short as filename extention")
    parser.add_argument("--ratio", type=float, default=3, help="the len ration between src and tgt")
    parser.add_argument("--longest", type=int, default=100, help="the limits of  longest sentence")
    parser.add_argument("--word_limit", type=int, default=40, help="the limits of longest word")

    args = parser.parse_args()
    data_dir = args.data_dir
    output_dir = args.output_dir
    file_src_name = os.path.join(data_dir, args.corpus_name + "." + args.src)
    file_tgt_name = os.path.join(data_dir, args.corpus_name + "." + args.tgt)

    flitered_file_src_name = os.path.join(output_dir, args.corpus_name + ".filtered." + args.src)
    flitered_file_tgt_name = os.path.join(output_dir, args.corpus_name + ".filtered." + args.tgt)

    count_discarded = 0
    filtered_info = {"empty_line":0, "over_ratio":0, "too_long_sen":0, "too_long_word":0}
    # print(file_src_name)
    with open(file_src_name, "r") as fs, open(file_tgt_name, mode='r') as ft, \
        open(flitered_file_src_name, "w+") as f_fs, open(flitered_file_tgt_name, "w+") as f_ft:
        for i, (src, tgt) in enumerate(zip(fs, ft)):
            src = src.strip()
            tgt = tgt.strip()
            if i%10000 == 0:
                logger.error(f"{i}")
            src_word_list = src.split()
            tgt_word_list = tgt.split()
            src_len = len(src_word_list)
            tgt_len = len(tgt_word_list)
            # empty line
            if src_len ==0 or tgt_len ==0:
                filtered_info["empty_line"] += 1
                continue
            # too long sentence
            if src_len > args.longest or tgt_len > args.longest:
                filtered_info["too_long_sen"] += 1
                continue
            # ratio is to large
            ratio_src2tgt = float(src_len)/tgt_len
            ratio_tgt2src = float(tgt_len)/src_len
            if ratio_src2tgt > args.ratio or ratio_tgt2src > args.ratio:
                filtered_info["over_ratio"] += 1

            # filter sentences contain very big words
            for word in src_word_list:
                if len(word) > args.word_limit:
                    # filtered_info["too_long_word"] += 1
                    print(" ".join(src_word_list))
                    continue
            for word in tgt_word_list:
                if len(word) > args.word_limit:
                    # print(" ".join(tgt_word_list))
                    filtered_info["too_long_word"] += 1
                    continue
            #output line pairs
            f_fs.write(src)
            f_fs.write("\n")
            f_ft.write(tgt)
            f_ft.write("\n")
    print(filtered_info)
    # logger.error("f{count_discarded}")

    # mt = MosesTokenizer(lang='en')
    # # text = u'This, is a sentence with weird\xbb symbols\u2026 appearing everywhere\xbf'
    # expected_tokenized = u'This , is a sentence with weird \xbb symbols \u2026 appearing everywhere \xbf'
    # tokenized_text = mt.tokenize(text, return_str=True)
    # tokenized_text == expected_tokenized

    # print(file_src_name)
    # print(file_tgt_name)
    # print(file_src_name)
    # text = "Hello!"
    # print(text)


if __name__ == "__main__":
    main()

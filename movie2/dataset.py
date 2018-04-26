"""
kin dataset 
"""

import os
import numpy as np
# from kor_char_parser import decompose_str_as_one_hot

import text_helpers
from konlpy.tag import Twitter
pos_tagger = Twitter()

class KinQueryDataset:
    """
        지식인 데이터를 읽어서, tuple (데이터, 레이블)의 형태로 리턴하는 파이썬 오브젝트 입니다.
    """
    def __init__(self, dataset_path: str, max_length: int):
        """
        :param dataset_path: 데이터셋 root path
        :param max_length: 문자열의 최대 길이
        """
        # 데이터, 레이블 각각의 경로
        queries_path = os.path.join(dataset_path, 'train', 'train_data')
        labels_path = os.path.join(dataset_path, 'train', 'train_label')

        # 지식인 데이터를 읽고 preprocess까지 진행합니다
        with open(queries_path, 'rt', encoding='utf8') as f:
            self.queries = preprocess(f.readlines(), max_length)
        # 지식인 레이블을 읽고 preprocess까지 진행합니다.
        with open(labels_path) as f:
            self.labels = np.array([[np.float32(x)] for x in f.readlines()])

    def __len__(self):
        """
        :return: 전체 데이터의 수를 리턴합니다
        """
        return len(self.queries)

    def __getitem__(self, idx):
        """
        :param idx: 필요한 데이터의 인덱스
        :return: 인덱스에 맞는 데이터, 레이블 pair를 리턴합니다
        """
        return self.queries[idx], self.labels[idx]

def tokenize(doc):
    # norm, stem은 optional
    return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

def preprocess(data: list, max_length: int):
    train_docs = [(tokenize(row[0]), tokenize(row[1])) for row in data]


# -*- coding: utf-8 -*-
from konlpy.corpus import kolaw
def read_data(filename):
    with open(filename, 'r') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]   # header 제외
    return data

train_data = kolaw.open('constitution.txt').read()

print(len(train_data))      # nrows: 150000
print(len(train_data[0]))

from konlpy.tag import Twitter
pos_tagger = Twitter()

def tokenize(doc):
    # norm, stem은 optional
    return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

train_docs = []
for row in train_data:
    train_docs.append((tokenize(row[0]), '0'))
    # train_docs.append((tokenize(row[1]), '0'))

# 잘 들어갔는지 확인
from pprint import pprint
pprint(train_docs[0])

from gensim.models.doc2vec import TaggedDocument
tagged_train_docs = [TaggedDocument(d, [c]) for d, c in train_docs]

from gensim.models import doc2vec
import multiprocessing
cores = multiprocessing.cpu_count()

# 사전 구축
doc_vectorizer = doc2vec.Doc2Vec(vector_size=1000, alpha=0.025, min_alpha=0.025, seed=1234, epochs=100, workers=cores, hs=1)
doc_vectorizer.build_vocab(tagged_train_docs)
doc_vectorizer.train(tagged_train_docs, epochs=doc_vectorizer.epochs, total_examples=doc_vectorizer.corpus_count)

# To save
doc_vectorizer.save('doc2vec.model')

doc_vectorizer = doc2vec.Doc2Vec.load('doc2vec.model')
pprint(doc_vectorizer.wv.most_similar('한국/Noun'))

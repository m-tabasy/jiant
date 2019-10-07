"""
Tasks from Senteval: https://github.com/facebookresearch/SentEval/tree/master/data/probing
"""
import collections
import itertools
import json
import logging as log
import os
from typing import Any, Dict, Iterable, List, Sequence, Type

import numpy as np
import pandas as pd
import torch


# Fields for instance processing
from allennlp.data import Instance, Token, vocabulary
from allennlp.data.fields import (
    LabelField,
    ListField,
    MetadataField,
    MultiLabelField,
    SpanField,
    TextField,
)
from allennlp.data.token_indexers import SingleIdTokenIndexer
from allennlp.training.metrics import Average, BooleanAccuracy, CategoricalAccuracy, F1Measure
from sklearn.metrics import mean_squared_error

from jiant.allennlp_mods.correlation import Correlation
from jiant.allennlp_mods.numeric_field import NumericField
from jiant.utils import utils
from jiant.utils.data_loaders import (
    get_tag_list,
    load_diagnostic_tsv,
    load_span_data,
    load_tsv,
    tokenize_and_truncate,
    load_pair_nli_jsonl,
)
from jiant.utils.tokenizers import get_tokenizer
from jiant.tasks.registry import register_task  # global task registry



@register_task("senteval-sentence-length", rel_path="sentence_length/")
class SentevalSentenceLengthTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalSentenceLengthTask, self).__init__(name, n_classes=7, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(6))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences



@register_task("senteval-bigram-shift", rel_path="bigram_shift/")
class SentevalBigramShiftTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalBigramShiftTask, self).__init__(name, n_classes=2, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(2))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences
        

@register_task("senteval-past-present", rel_path="past_present/")
class SentevalPastPresentTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalPastPresentTask, self).__init__(name, n_classes=2, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return ["PAST", "PRES"]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences
        


@register_task("senteval-odd-man-out", rel_path="odd_man_out/")
class SentevalOddManOutTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalOddManOutTask, self).__init__(name, n_classes=6, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(6))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences



@register_task("senteval-coordination-inversion", rel_path="coordination_inversion/")
class SentevalCoordinationInversionTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalCoordinationInversionTask, self).__init__(name, n_classes=6, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(6))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences

@register_task("senteval-word-content", rel_path="word_content")
class SentevalWordContentTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalWordContentTask, self).__init__(name, n_classes=1000, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(1000))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences

@register_task("senteval-tree-depth", rel_path="tree_depth")
class SentevalWordContentTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalWordContentTask, self).__init__(name, n_classes=8, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(8))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences


@register_task("senteval-top-constituents", rel_path="top_constituents/")
class SentevalTopConstituentsTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super(SentevalTopConstituentsTask, self).__init__(name, n_classes=20, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return [str(x) for x in list(range(20))]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences

@register_task("senteval-subj-number", rel_path="subj_number")
class SentevalSubjNumberTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super( SentevalSubjNumberTask, self).__init__(name, n_classes=2, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return ["NN", "NNS"]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences


@register_task("senteval-obj-number", rel_path="obj_number")
class SentevalSubjNumberTask(SingleClassificationTask):
    """ Sentene length task from Senteval.  """

    def __init__(self, path, max_seq_len, name, **kw):
        """ """
        super( SentevalSubjNumberTask, self).__init__(name, n_classes=2, **kw)
        self.path = path
        self.max_seq_len = max_seq_len
        self._label_namespace = self.name + "_tags"
        self.train_data_text = None
        self.val_data_text = None
        self.test_data_text = None

    def get_all_labels(self):
        return ["NN", "NNS"]

    def get_sentences(self):
        return self.sentences

    def load_data(self):
        """ Load data """
        def load_json(data_file):
            rows = pd.read_csv(data_file, encoding = "ISO-8859-1")
            rows["s1"] = rows['2'].apply(lambda x: tokenize_and_truncate(
                    self._tokenizer_name, x, self.max_seq_len
                ))
            return rows['s1'].tolist(), [], rows['1'].tolist(), list(range(len(rows)))

        self.train_data_text = load_json(os.path.join(self.path, "train.tsv"))
        self.val_data_text = load_json(os.path.join(self.path, "val.tsv"))
        self.test_data_text = load_json(os.path.join(self.path, "test.tsv"))

        sentences = []
        for split in ["train", "val", "test"]:
            split_data = getattr(self, "%s_data_text" % split)
            sentences.extend(split_data[0])
        self.sentences = sentences
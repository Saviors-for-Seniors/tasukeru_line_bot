# -*- coding: utf-8 -*-
import os
import sys
import numpy as np
import pandas as pd
import datasets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '../../knowledge'))
from bert_model.reader import read_3class_problems, read_40class_problems, read_40class_multilabel_problems


class BertMultiClassAttributeExtractorTemplate:
    def __init__(self):
        '''
        多クラス分類専用BERTモデルのテンプレート
        '''
        self._tokenizer, self._model, self._trainer = read_3class_problems()
        # 以下に{クラスラベル(int): クラス名(str)}の辞書をセットする
        self._class_labels = {}

    def extract(self, text, threshold=0.45):
        '''
        textから各属性の属性値を抽出する。ここでは属性名は'PROBLEM'の1種類
        textをBERTモデルに入れると、3クラスのPROBLEMのうちどれが含まれているか確率値で出力される。
        ある閾値を超える属性値をこの関数の戻り値とする。
        
        Parameters
        -------------
        text : str
            文字列
        threshold : float
            閾値
        
        Returns
        -------------
        attribute : dict
            キーに属性名、値に属性値リスト。
        '''
        attribute = {'PROBLEM': self._extract_problem(text, threshold)}
        return attribute

    def _extract_problem(self, text, threshold=0.45):
        '''
        textから問題を抽出する
        
        Parameters
        -----------
        text : str
            文字列
        threshold : float
            閾値
        
        Returns
        -------------
        problems : list of str
            textから抽出した問題名のリスト。正規表現にヒットしなかった場合は空のリストを返す
        '''
        # textの前処理
        testdata = datasets.Dataset.from_dict({'sentence': [text]})
        encoded_testdata = testdata.map(self._preprocess_function, batched=True)
        # 予測
        predictions = self._trainer.predict(encoded_testdata)
        p = _softmax(predictions.predictions)[0]
        choose_labels = np.where(p > threshold)[0]
        problems = [self._class_labels[l] for l in choose_labels]

        return problems
    
    def _preprocess_function(self, examples):
        '''トークン化'''
        return self._tokenizer(examples['sentence'], truncation=True)



class BertMultiClassAttributeExtractor_BestK_Template:
    def __init__(self):
        '''
        多クラス分類専用BERTモデルのテンプレート
        上位Kクラスと確率値を返す
        '''
        self._tokenizer, self._model, self._trainer = read_3class_problems()
        # 以下に{クラスラベル(int): クラス名(str)}の辞書をセットする
        self._class_labels = {}

    def extract(self, text, K=5):
        '''
        textから各属性の属性値を抽出する。ここでは属性名は'PROBLEM'の1種類
        textをBERTモデルに入れると、40クラスのPROBLEMのうちどれが含まれているか確率値で出力される。
        上位K個の属性値をこの関数の戻り値とする。
        
        Parameters
        -------------
        text : str
            文字列
        threshold : float
            閾値
        
        Returns
        -------------
        attribute : dict
            キーに属性名、値に属性値リスト。
        '''
        # textの前処理
        testdata = datasets.Dataset.from_dict({'sentence': [text]})
        encoded_testdata = testdata.map(self._preprocess_function, batched=True)
        # 予測
        predictions = self._trainer.predict(encoded_testdata)
        p = _softmax(predictions.predictions)[0]
        choose_labels = _get_K_indices(p, K)
        problems = {self._class_labels[l]: p[l] for l in choose_labels}
        attribute = {'PROBLEM': problems}
        return attribute

    def _preprocess_function(self, examples):
        '''トークン化'''
        return self._tokenizer(examples['sentence'], truncation=True)
    
def _get_K_indices(arr, K):
    '''np.arrayのうち値の大きさが上位K件のインデックスを取得する'''
    # ソートはされていない上位k件のインデックス
    unsorted_max_indices = np.argpartition(-arr, K)[:K]
    # 上位k件の値
    y = arr[unsorted_max_indices]
    # 大きい順にソートし、インデックスを取得
    indices = np.argsort(-y)
    # 類似度上位k件のインデックス
    max_k_indices = unsorted_max_indices[indices]
    return max_k_indices


class Bert3ClassAttributeExtractor(BertMultiClassAttributeExtractorTemplate):

    def __init__(self):
        '''
        3クラス分類専用BERTモデル（「足が悪い」:0, 「耳が遠い」:1, 「認知症」:2）
        '''
        self._tokenizer, self._model, self._trainer = read_3class_problems()
        self._class_labels = {0: '足が悪い', 1: '耳が遠い', 2: '認知症'}



#class Bert40ClassAttributeExtractor(BertMultiClassAttributeExtractorTemplate):  # 確率が閾値以上を検出
class Bert40ClassAttributeExtractor(BertMultiClassAttributeExtractor_BestK_Template):  # 確率の上位K件を取得

    def __init__(self):
        '''
        40クラス分類専用BERTモデル
        '''
        self._tokenizer, self._model, self._trainer = read_40class_problems()
        self._class_labels = pd.read_csv(os.path.join(BASE_DIR, '../../knowledge/bert_model/models/keywords_40class.csv'))\
                                .set_index('label')['keyword'].to_dict()
    """
    # 確率が閾値以上、の場合
    def extract(self, text, threshold=0.2):
        attribute = {'PROBLEM': self._extract_problem(text, threshold)}
        return attribute
    """



class BertMultiClassMultiLabelAttributeExtractor_BestK_Template:
    def __init__(self):
        '''
        多クラス多ラベル分類専用BERTモデルのテンプレート
        上位Kクラスと確率値を返す
        '''
        self._tokenizer, self._model, self._trainer = read_40class_multilabel_problems()
        # 以下に{クラスラベル(int): クラス名(str)}の辞書をセットする
        self._class_labels = {}

    def extract(self, text, K=5):
        '''
        textから各属性の属性値を抽出する。ここでは属性名は'PROBLEM'の1種類
        textをBERTモデルに入れると、40クラスのPROBLEMのうちどれが含まれているか確率値で出力される。
        上位K個の属性値をこの関数の戻り値とする。
        
        Parameters
        -------------
        text : str
            文字列
        threshold : float
            閾値
        
        Returns
        -------------
        attribute : dict
            キーに属性名、値に属性値リスト。
        '''
        # textの前処理
        testdata = datasets.Dataset.from_dict({'sentence': [text]})
        encoded_testdata = testdata.map(self._preprocess_function, batched=True)
        # 予測
        predictions = self._trainer.predict(encoded_testdata)
        p = _sigmoid(predictions.predictions)[0]
        choose_labels = _get_K_indices(p, K)
        problems = {self._class_labels[l]: p[l] for l in choose_labels}
        attribute = {'PROBLEM': problems}
        return attribute

    def _preprocess_function(self, examples):
        '''トークン化'''
        return self._tokenizer(examples['sentence'], truncation=True)


class Bert40ClassMultiLabelAttributeExtractor(BertMultiClassMultiLabelAttributeExtractor_BestK_Template):  # 確率の上位K件を取得

    def __init__(self):
        '''
        40クラス分類専用BERTモデル
        '''
        self._tokenizer, self._model, self._trainer = read_40class_multilabel_problems()
        self._class_labels = pd.read_csv(os.path.join(BASE_DIR, '../../knowledge/bert_model/models/keywords_40class_multilabel.csv'))\
                                .set_index('label')['keyword'].to_dict()
    """
    # 確率が閾値以上、の場合
    def extract(self, text, threshold=0.2):
        attribute = {'PROBLEM': self._extract_problem(text, threshold)}
        return attribute
    """


def _softmax(x):
    if (x.ndim == 1):
        x = x[None,:]    # ベクトル形状なら行列形状に変換
    # テンソル（x：行列）、軸（axis=1： 列の横方向に計算）
    return np.exp(x) / np.sum(np.exp(x), axis=1, keepdims=True)


def _sigmoid(arr):
    return 1 / (1 + np.exp(-arr))
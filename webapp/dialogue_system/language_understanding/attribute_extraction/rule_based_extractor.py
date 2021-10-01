# -*- coding: utf-8 -*-
import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, '../..'))
from knowledge.rule_base.reader import read_3class_problems


class RuleBasedAttributeExtractor(object):

    def __init__(self):
        self._problems_dict = read_3class_problems()

    def extract(self, text):
        '''
        textから各属性の属性値を抽出する（ルールベース。正規表現にヒットするかで判定）
        ここでは属性名は'PROBLEM'の1種類
        
        Parameters
        -------------
        text : str
            文字列
        
        Returns
        -------------
        attribute : dict
            キーに属性名、値に属性値リスト。
        '''
        attribute = {'PROBLEM': self._extract_problem(text)}
        return attribute

    def _extract_problem(self, text):
        '''
        textから問題を抽出する
        
        Parameters
        -----------
        text : str
            文字列
        
        Returns
        -------------
        problems : list of str
            textから抽出した問題名のリスト。正規表現にヒットしなかった場合は空のリストを返す
        '''
        problems = []
        for problem, search_words in self._problems_dict.items():
            for search_word in search_words:
                if not search_word is None:  # TODO:全項目に検索ワードを与えたら消す
                    if not re.search(search_word, text) is None:
                        problems.append(problem)
                        break
        return problems
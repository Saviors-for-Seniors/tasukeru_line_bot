
# -*- coding: utf-8 -*-
import copy

from .attribute_extraction.rule_based_extractor import RuleBasedAttributeExtractor
from .attribute_extraction.bert_based_extractor import Bert3ClassAttributeExtractor, Bert40ClassAttributeExtractor, Bert40ClassMultiLabelAttributeExtractor
from .dialogue_act_type.rule_based_estimator import RuleBasedDialogueActTypeEstimator


class LanguageUnderstandingTemplate:

    def __init__(self):
        '''言語理解を行うテンプレートクラス'''
        self._extractor = lambda sent: {'PROBLEM': []}
        self._estimator = lambda attribute: 'OTHER'

    def execute(self, sent):
        '''
        文章(sent)に対して言語理解を行い、抽出した属性と対話行為タイプを返す
        
        Parameters
        -------------
        sent : str
            文章
        
        Returns
        ----------
        dialogue_act : dict
            キーにuser_act_type(対話行動タイプ), utt(元の文章), 属性名(今回は'PROBLEM'のみ)
        '''
        attribute = self._extractor.extract(sent)
        act_type = self._estimator.estimate(attribute)

        dialogue_act = {'user_act_type': act_type, 'utt': sent}
        attribute_cp = copy.copy(attribute)
        for k, v in attribute_cp.items():
            if v == '':
                del attribute[k]
        dialogue_act.update(attribute)

        return dialogue_act


class RuleBasedLanguageUnderstanding(LanguageUnderstandingTemplate):

    def __init__(self):
        '''
        ルールベースで言語理解を行うクラス（属性抽出＋対話行為タイプの推定ともにルールベース）
        '''
        self._extractor = RuleBasedAttributeExtractor()
        self._estimator = RuleBasedDialogueActTypeEstimator()


class Bert3ClassLanguageUnderstanding(LanguageUnderstandingTemplate):

    def __init__(self):
        '''
        3クラスBERTモデルにより言語理解を行うクラス
        （BERTによる属性抽出＋ルールベースによる対話行為タイプの推定）
        '''
        self._extractor = Bert3ClassAttributeExtractor()
        self._estimator = RuleBasedDialogueActTypeEstimator()


class Bert40ClassLanguageUnderstanding(LanguageUnderstandingTemplate):

    def __init__(self):
        '''
        40クラスBERTモデルにより言語理解を行うクラス
        （BERTによる属性抽出＋ルールベースによる対話行為タイプの推定）
        '''
        self._extractor = Bert40ClassAttributeExtractor()
        self._estimator = RuleBasedDialogueActTypeEstimator()


class Bert40ClassMultiLabelLanguageUnderstanding(LanguageUnderstandingTemplate):

    def __init__(self):
        '''
        40クラス多ラベルBERTモデルにより言語理解を行うクラス
        （BERTによる属性抽出＋ルールベースによる対話行為タイプの推定）
        '''
        self._extractor = Bert40ClassMultiLabelAttributeExtractor()
        self._estimator = RuleBasedDialogueActTypeEstimator()
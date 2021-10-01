
# -*- coding: utf-8 -*-


class RuleBasedDialogueActTypeEstimator(object):

    def __init__(self):
        pass

    def estimate(self, attribute):
        '''
        extractorで抽出された属性名、属性値に基づいて対話行為タイプを推定
        今回、対話行為タイプは[TALK_PROBLEM, OTHER]の2種類
        
        Parameters
        -----------
        attribute : dict
            キーに属性名、値に属性値
            今回キーは'PROBLEM'のみ、属性値は問題名のリスト
        
        Returns
        ---------
        act_type : str
            推定された対話行為タイプ
        '''
        # 問題が抽出された　→悩み相談
        if len(attribute['PROBLEM']) >= 1:
            act_type = 'TALK_PROBLEM'
        
        # 問題が抽出されなかった　→自由会話
        else:
            act_type = 'OTHER'
        
        return act_type
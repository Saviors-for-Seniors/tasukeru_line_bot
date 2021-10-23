# -*- coding: utf-8 -*-
import sys
from copy import deepcopy
from .state import DialogueState


class DialogueManager(object):

    def __init__(self):
        '''対話管理用クラス'''
        self.dialogue_state = DialogueState()


    def update_dialogue_state(self, dialogue_act):
        '''
        対話行為と現在の内部状態から、次の内部状態へ更新する
        
        Parameters
        ------------
        dialogue_act : dict
            属性と対話行動タイプ
            キーにuser_act_type(対話行動タイプ), utt(元の文章), 属性名(今回は'PROBLEM'のみ)
        '''
        self.dialogue_state.update(dialogue_act)


    def select_action(self):
        '''
        内部状態から次の行動を選択する
        今回、行動は['SUGGEST_GOODS', 'DEFAULT_MESSAGE']の2種類

        (※元々dialogue_actを引数に渡していたが、次の行動は内部状態だけで決めればいいと思う)
        
        Returns
        ------------
        sys_act : dict
            次の行動を表す辞書
            キーにsys_act_type(行動タイプ) +α
        '''
        sys_act = {}

        # ユーザの問題がわかっていれば商品・解決法を提案する
        # TODO: 内部状態に確率値をもたせ、不確かであればもう一度確認するという行動を選択してもよい
        if len(self.dialogue_state.get_problem()) >= 1:
            sys_act['sys_act_type'] = 'SUGGEST_GOODS'
            # 次の行動に必要な情報を格納
            sys_act['PROBLEM'] = self.dialogue_state.get_problem()
            # 内部状態初期化
            self.dialogue_state.clear()
        
        # 属性が認識できなかった場合はデフォルトメッセージを出す
        else:
            sys_act['sys_act_type'] = 'DEFAULT_MESSAGE'

        return sys_act
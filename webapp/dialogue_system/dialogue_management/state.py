# -*- coding: utf-8 -*-
import pprint


class DialogueState(object):

    def __init__(self):
        '''内部状態操作用クラス'''
        # 初期化
        self._state = {'PROBLEM': None}

    def update(self, dialogue_act):
        '''
        対話行為と現在の内部状態から次の内部状態へ更新する

        Parameters
        -----------
        dialogue_act : dict
            属性と対話行動タイプ
            キーにuser_act_type(対話行動タイプ), utt(元の文章), 属性名(今回は'PROBLEM'のみ)
        '''
        # TODO: 2回目以降の質問ですでにわかっている属性が上書きされる可能性がある？（対話行動タイプを見て更新する箇所を限定すべき？）
        self._state['PROBLEM'] = dialogue_act.get('PROBLEM', self._state['PROBLEM'])

    def has(self, name):
        return self._state.get(name, None) != None

    def get_problem(self):
        return self._state['PROBLEM']

    def clear(self):
        self.__init__()

    def __str__(self):
        return pprint.pformat(self._state)
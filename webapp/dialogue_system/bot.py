
# -*- coding: utf-8 -*-
from .dialogue_management.manager import DialogueManager
from .language_generation.generator import LanguageGenerator
from .language_understanding.language_understanding import RuleBasedLanguageUnderstanding, Bert3ClassLanguageUnderstanding, Bert40ClassLanguageUnderstanding, Bert40ClassMultiLabelLanguageUnderstanding


class Bot(object):

    def __init__(self):
        self.generator = LanguageGenerator()
        #self.language_understanding = RuleBasedLanguageUnderstanding()  # ルールベース
        #self.language_understanding = Bert3ClassLanguageUnderstanding()  # 3クラスお試し
        #self.language_understanding = Bert40ClassLanguageUnderstanding()  # 40クラスお試し
        self.language_understanding = Bert40ClassMultiLabelLanguageUnderstanding()  # 40クラス多ラベルお試し
        self.manager = DialogueManager()

    def reply(self, sent):
        # 言語理解
        dialogue_act = self.language_understanding.execute(sent)

        # 対話管理（内部状態更新、行動選択）
        self.manager.update_dialogue_state(dialogue_act)
        sys_act_type = self.manager.select_action()

        # 言語生成
        sent = self.generator.generate_sentence(sys_act_type)

        return sent
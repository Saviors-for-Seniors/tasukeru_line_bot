# -*- coding: utf-8 -*-
import os
import yaml

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_3class_problems():
    '''
    3クラス用のデータをyamlから取得する

    Returns
    -----------
    problems_dict : dict of list
        キーに問題名、値にその問題を検出するための正規表現(str)をリストにしたもの
    '''
    file_path = os.path.join(BASE_DIR, 'problems_3class.yaml')
    with open(file_path, 'rb') as f:
        problems_dict = yaml.load(f)

    return problems_dict


def read_symptoms():
    file_path = os.path.join(BASE_DIR, 'symptoms.yaml')
    with open(file_path, 'rb') as f:
        symptoms = yaml.load(f)

    return symptoms


def read_problems():
    file_path = os.path.join(BASE_DIR, 'problems.yaml')
    with open(file_path, 'rb') as f:
        problems = yaml.load(f)

    return problems
# -*- coding: utf-8 -*-
import os
from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForSequenceClassification, TrainingArguments, Trainer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_3class_problems():
    '''
    3クラス用（「足が悪い」:0, 「耳が遠い」:1, 「認知症」:2）のBERTモデルを取得する

    Returns
    -----------
    tokenizer
        BERTのトークナイザ
    model
        BERTモデル
    Trainer
        Trainer。訓練データ等も読み込ませているができれば消したい
    '''
    NUM_LABELS = 3

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking', use_fast=True)

    # model
    model = AutoModelForSequenceClassification.from_pretrained(
        os.path.join(BASE_DIR, './models/trial_3class'), num_labels=NUM_LABELS)

    # trainer
    # 訓練用ダミーデータ読み込み
    dataset = load_dataset('csv', data_files=[os.path.join(BASE_DIR, './dummy_data/dummy_data.csv')], split='train')
    dataset = dataset.train_test_split(test_size=0.34)
    def preprocess_function(examples):
        return tokenizer(examples['sentence'], truncation=True)
    encoded_dataset = dataset.map(preprocess_function, batched=True)
    batch_size = 1
    args = TrainingArguments(
        "./outputs",
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model='accuracy',
        logging_steps=500
    )
    # ※こっちのmetricsもどうするかわからないが、多クラス分類でやってそうなMNLIのもの(accuracy)を使用
    from datasets import load_metric
    metric = load_metric('accuracy')
    import numpy as np
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return metric.compute(predictions=predictions, references=labels)
    trainer = Trainer(
        model,
        args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset['test'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    return tokenizer, model, trainer



def read_40class_problems():
    '''
    40クラス用BERTモデルを取得する

    Returns
    -----------
    tokenizer
        BERTのトークナイザ
    model
        BERTモデル
    Trainer
        Trainer。訓練データ等も読み込ませているができれば消したい
    '''
    NUM_LABELS = 40

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking', use_fast=True)

    # model
    model = AutoModelForSequenceClassification.from_pretrained(
        os.path.join(BASE_DIR, './models/40class_augumented_32batch_10epoch'), num_labels=NUM_LABELS)

    # trainer
    # 訓練用ダミーデータ読み込み
    dataset = load_dataset('csv', data_files=[os.path.join(BASE_DIR, './dummy_data/dummy_data.csv')], split='train')
    dataset = dataset.train_test_split(test_size=0.34)
    def preprocess_function(examples):
        return tokenizer(examples['sentence'], truncation=True)
    encoded_dataset = dataset.map(preprocess_function, batched=True)
    batch_size = 1
    args = TrainingArguments(
        "./outputs",
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=True,
        metric_for_best_model='accuracy',
        logging_steps=500
    )
    # ※こっちのmetricsもどうするかわからないが、多クラス分類でやってそうなMNLIのもの(accuracy)を使用
    from datasets import load_metric
    metric = load_metric('accuracy')
    import numpy as np
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions = np.argmax(predictions, axis=1)
        return metric.compute(predictions=predictions, references=labels)
    trainer = Trainer(
        model,
        args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset['test'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    return tokenizer, model, trainer


def read_40class_multilabel_problems():
    '''
    40クラス多ラベル分類用BERTモデルを取得する

    Returns
    -----------
    tokenizer
        BERTのトークナイザ
    model
        BERTモデル
    Trainer
        Trainer。訓練データ等も読み込ませているができれば消したい
    '''
    NUM_LABELS = 40

    # tokenizer
    tokenizer = AutoTokenizer.from_pretrained('cl-tohoku/bert-base-japanese-whole-word-masking', use_fast=True,
                                              problem_type='multi_label_classification')

    # model
    model = AutoModelForSequenceClassification.from_pretrained(
        os.path.join(BASE_DIR, './models/40class_multilabel_augumented_32batch_10epoch'), num_labels=NUM_LABELS,
                     problem_type='multi_label_classification')

    # trainer
    # 訓練用ダミーデータ読み込み
    dataset = load_dataset('csv', data_files=[os.path.join(BASE_DIR, './dummy_data/dummy_data.csv')], split='train')
    dataset = dataset.train_test_split(test_size=0.34)
    def preprocess_function(examples):
        return tokenizer(examples['sentence'], truncation=True)
    encoded_dataset = dataset.map(preprocess_function, batched=True)
    batch_size = 1
    args = TrainingArguments(
        os.path.join(BASE_DIR, "./outputs"),
        evaluation_strategy = "epoch",
        learning_rate=2e-5,
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=5,
        weight_decay=0.01,
        load_best_model_at_end=False,
        metric_for_best_model='accuracy',
        logging_steps=500
    )
    # metricsは完答の精度（total accuracy）
    # (真の値が「0 1 1 0」で、予測値が「0 1 1 1」と1つでも違ったら間違い（0）)
    import numpy as np
    def sigmoid(arr):
        return 1 / (1 + np.exp(-arr))
    def compute_metrics(eval_pred):
        predictions, labels = eval_pred
        predictions_prob = sigmoid(predictions)
        predictions_label = np.where(predictions_prob < 0.5, 0, 1)
        is_match = predictions_label == labels
        is_correct = is_match.all(axis=1)  # 各データで全ラベル一致ならTrue、それ以外はFalse
        accuracy = is_correct.sum() / len(is_correct)  # 正解数 / データ数
        return {'accuracy': accuracy}
    trainer = Trainer(
        model,
        args,
        train_dataset=encoded_dataset["train"],
        eval_dataset=encoded_dataset['test'],
        tokenizer=tokenizer,
        compute_metrics=compute_metrics
    )
    return tokenizer, model, trainer

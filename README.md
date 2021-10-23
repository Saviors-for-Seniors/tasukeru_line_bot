# Amazon ECRへのプッシュ、lambdaでのデプロイ方法
## 1. リポジトリのクローン
```
https://github.com/Saviors-for-Seniors/tasukeru_line_bot.git
```

## 2. 学習済みモデル、ラベルファイルの追加
クローンしたリポジトリの下記フォルダに学習済みモデル、ラベルファイルを格納する。
+ 格納フォルダ：tasukeru_line_bot/webapp/dialogue_system/knowledge/bert_model
+ 学習済みモデル：[リンク](https://drive.google.com/drive/folders/1PSQrWhFNUZO6z-a3vzk9p6g1q13l3OiX)
+ ラベルファイル：[リンク](https://drive.google.com/drive/folders/16mpuQw_p3l3VMaeVDNiLuue2Dmq3PqFq)

## 3. Imageのbuild〜push

※下記、関数名（func2）、URLはちゃんと設定すること
```
# build
docker build -t func2 .
# タグ付け
docker tag func2:latest 075960133323.dkr.ecr.ap-northeast-1.amazonaws.com/func2:latest
# プッシュ
docker push 075960133323.dkr.ecr.ap-northeast-1.amazonaws.com/func2:latest
```
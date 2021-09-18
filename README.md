# FlaskのDockerイメージをHerokuにデプロイする

## はじめに

`macOS環境の記事ですが、Windows環境も同じ手順になります。環境依存の部分は読み替えてお試しください。`

### 目的

この記事を最後まで読むと、次のことができるようになります。

| No.  | 概要                            | キーワード                   |
| :--- | :------------------------------ | :--------------------------- |
| 1    | Dockerイメージのビルド/プッシュ | heroku container:push web    |
| 2    | Dockerイメージのリリース        | heroku container:release web |

### 実行環境

| 環境           | Ver.     |
| :------------- | :------- |
| macOS Catalina | 10.15.6  |
| Python         | 3.7.3    |
| Heroku         | 7.42.13  |
| Docker         | 19.03.12 |
| Flask          | 1.1.2    |
| gunicorn       | 20.0.4   |
| Jinja2         | 2.11.2   |
| Werkzeug       | 1.0.1    |

### ソースコード

実際に実装内容やソースコードを追いながら読むとより理解が深まるかと思います。是非ご活用ください。

- [GitHub](https://github.com/nsuhara/heroku-docker.git)

### 関連する記事

- [Container Registry & Runtime (Docker Deploys)](https://devcenter.heroku.com/articles/container-registry-and-runtime)

## 手順

### 1. Container Registry ログイン

```command.sh
~% heroku container:login
```

### 2. サンプルコード取得

```command.sh
~% git clone https://github.com/nsuhara/heroku-docker.git -b master
```

```tree.sh
heroku-docker
    ├── Dockerfile
    ├── docker-compose.yml
    ├── docker_compose_up.sh
    └── webapp
            ├── app.py
            ├── requirements.txt
            ├── tests
            │       ├── __init__.py
            │       └── tests.py
            └── wsgi.py
```

### 3. ディレクトリ移動

```command.sh
~% cd heroku-docker
```

### 4. Herokuアプリ作成

`※今回のアプリ名は自動生成とします`

```command.sh
~% heroku create
Creating app... done, ⬢ {app-name}
```

### 5. リモートリポジトリ設定

```command.sh
~% heroku git:remote -a {app-name}
```

### 6. イメージビルド & Container Registry プッシュ

```command.sh
~% heroku container:push web
```

### 7. Container Registry リリース

```command.sh
~% heroku container:release web
```

### 8. アプリ表示

```command.sh
~% heroku open
```

## おまけ

### ローカル環境アプリ表示

```command.sh
~% sh docker_compose_up.sh
```

```command.sh
~% open http://0.0.0.0:5000/
```

### コードチェック (pylint)

```command.sh
~% python -B -m pylint --rcfile=.pylintrc -f parseable `find webapp -name "*.py" -not -path "webapp/tests"`
```

### コードテスト (unittest)

```command.sh
~% python -B -m unittest discover tests
```

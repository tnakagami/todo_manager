# Django
## makemigrationsとmigrateの実行
以下のコマンドでmakemigrationsを実行する。ここで、`app-name`は実行対象のアプリ名である。

```bash
python manage.py makemigrations app-name
# ex.
# python manage.py makemigrations sns
```

そして、以下のコマンドで`migrate`を実行する。

```bash
python manage.py migrate
```

上記の操作は、モデルを変更した場合に実施すること。

## スーパーユーザアカウントの作成
以下のコマンドでスーパーユーザアカウントを作成する。これは、最初に1度だけ実施すればよい。

ここで、`DJANGO_SUPERUSER_EMAIL`, `DJANGO_SUPERUSER_PASSWORD`は、`env_file/django/.env`で定義される環境変数である。

```bash
python manage.py custom_createsuperuser --email ${DJANGO_SUPERUSER_EMAIL} --password ${DJANGO_SUPERUSER_PASSWORD}
```

## 多言語対応
以下のコマンドで多言語対応を行う。

```bash
django-admin.py makemessages -l ja
# .po filesの変更
django-admin.py compilemessages
```

## 静的ファイルの取得
以下のコマンドで静的ファイルを作成する。そして、作成したファイルをホストOS側にコピーする。
```bash
# コンテナ内で実行
python manage.py collectstatic

# コンテナ外で実行（ホストOS側で実行）
docker cp django:/static/admin staticfiles/static
docker cp django:/static/import_export staticfiles/static
```

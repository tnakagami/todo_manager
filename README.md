# ToDoリストの管理
## 環境変数の設定
### mysql
* 環境変数設定先のファイルパス

    ```bash
    env_file/mysql/.env
    ```

* 環境変数のサンプル

    ```bash
    env_file/mysql/Readme.md
    ```

* 環境変数の説明

    | 変数名 | 説明 |
    | :--- | :--- |
    | MYSQL_ROOT_PASSWORD | rootユーザのパスワード |
    | MYSQL_DATABASE | djangoで利用するデータベース名 |
    | MYSQL_USER | djangoからデータベースに接続する際のユーザ名 |
    | MYSQL_PASSWORD | djangoからデータベースに接続する際のパスワード（上記のユーザ名に対応） |
    | MYSQL_CHARSET | mysqlの文字コード。「utf8mb4」を設定すること。 |
    | MYSQL_COLLATION | mysqlの照合順序。「utf8mb4_unicode_ci」を設定すること。 |

### nginx
* 環境変数設定先のファイルパス

    ```bash
    env_file/nginx/.env
    ```

* 環境変数のサンプル

    ```bash
    env_file/nginx/Readme.md
    ```

* 環境変数の説明
    * ここでは、MyDNSのアカウントを用いてLet's Encryptの更新を行う場合の例を示す。異なるドメインを用いる場合、nginxディレクトリ以下にある「`direct_edit`」や「`execute.sh`」を編集すること。
    * Let's Encryptを用いて、SSLサーバ証明書を作成する際にワイルドカードを用いる。このため、サブドメインを除いたドメイン名を指定すること。
        * 例：www.example.comの場合、BASE_DOMAIN_NAMEには、example.comを指定する。

    | 変数名 | 説明 |
    | :--- | :--- |
    | MYDNSJP_MASTER_ID | MyDNSのマスターID |
    | MYDNSJP_PASSWORD | MyDNSのパスワード |
    | MYDNS_EMAIL_ADDR | MyDNSに登録しているE-mailアドレス |
    | BASE_DOMAIN_NAME | ドメイン名 |
    | VHOST_NAME | Nginxで待ち受けるサブドメイン名 | 
    | SSL_CERT_PATH | Let's Encryptのfullchain.pemの絶対パス |
    | SSL_CERTKEY_PATH | Let's Encryptのprivkey.pemの絶対パス |
    | SSL_STAPLING_VERIFY | 証明書の検証の実施有無（on/off） | 
    | SSL_TRUSTED_CERTIFICATE_PATH | Let's Encryptのchain.pemの絶対パス（証明書の検証を行う場合） |

### django
* 環境変数設定先のファイルパス

    ```bash
    env_file/django/.env
    ```

* 環境変数のサンプル

    ```bash
    env_file/django/Readme.md
    ```

* 環境変数の説明
    * DJANGO_WWW_VHOSTは、Nginxで設定した「VHOST_NAME」と同一のものを指定すること。
    * 本番環境では、DJANGO_DEBUG_FLAGをFalseに設定すること。
    * DJANGO_SECRET_KEYは、以下のサイトを参考に再生成すること。

        [Django 秘密鍵生成](https://miniwebtool.com/ja/django-secret-key-generator/)

    | 変数名 | 説明 |
    | :--- | :--- |
    | DJANGO_SECRET_KEY | Djangoの秘密鍵 |
    | DJANGO_SUPERUSER_EMAIL | DjangoのスーパーユーザのE-mailアドレス |
    | DJANGO_SUPERUSER_PASSWORD | Djangoのスーパーユーザのパスワード |
    | DJANGO_DEBUG_FLAG | 開発時のモード（True：デバッグ、False：本番） |
    | DJANGO_WWW_VHOST | Nginxで待ち受けるサブドメイン名 |

## Docker Imageのビルド
以下のコマンドを実行し、Docker Imageのビルドを行う。

```bash
./wrapper.sh build
```

## Docker Containerの起動
以下のコマンドを実行し、Docker Containerを起動する。

```bash
./wrapper.sh start
```
# pw-zipper

## 概要

D&Dでランダムパスワード付きZipを生成するプログラムです。

## インストール

1. 7-Zipをインストールする。
2. `settings.ini`にインストールパスを記載する。
3. 好みの圧縮率を設定する。
4. `py-zipper.exe`のショートカットをデスクトップに配置すると便利。

## 使い方

- Exeもしくはそのショートカットに対して、圧縮したいファイルかフォルダをD&Dすると、元ファイルと同じ場所にパスワード付きZipファイルが生成される。
- 出力結果をコピーして、メール送付するなど。

## リリース作業

1. Exe化

  ```bash
  python -m venv .venv
  source .venv/bin/activate
  ```

  ```bash
  pip install nuitka
  ```

  ```bash
  python -m nuitka --onefile --windows-icon-from-ico=icon.ico main.py
  ```

1. リリース用ファイルの取り出し

  ```bash
  mkdir pw-zipper-vx.x.x/
  mv main.exe pw-zipper-vx.x.x/pw-zipper.exe
  cp template.txt pw-zipper-vx.x.x/template.txt
  cp settings.ini pw-zipper-vx.x.x/settings.ini
  ```

  リリース用のフォルダはどこかに移動する。

1. Exeの電子署名 (ウイルス誤検出対策)

  実行ファイルは電子署名しておく。
  以下参考 (WindowsSDKのインストールが必要)

  GitBash

  ```bash
  # 秘密鍵の生成
  openssl genrsa -out private_key.pem 2048

  # CSR(証明書署名要求)の作成
  openssl req -new -key private_key.pem -out certificate.csr

  # 自己署名証明書の生成 (3,650日にした)
  openssl x509 -req -days 3650 -in certificate.csr -signkey private_key.pem -out certificate.crt
  Certificate request self-signature ok
  subject=C=JP, ST=Aichi, L=Nagoya, O=RSfact, OU=Developers, CN=RSfact, emailAddress=info@rsfact.com

  # SignToolで使用するためにPFX形式に変換します
  openssl pkcs12 -export -out certificate.pfx -inkey private_key.pem -in certificate.crt
  ```

  コマンドプロンプト (管理者権限)

  ```cmd
  cd C:\Program Files (x86)\Windows Kits\10\bin\10.0.26100.0\x64

  signtool.exe sign /fd SHA256 /f "C:\path\to\certificate.pfx" /p "password" /t "http://timestamp.digicert.com" /d "PW-Zipper" "C:\path\to\pw-zipper-vx.x.x\pw-zipper.exe"
  ```

1. GitHubにてリリース

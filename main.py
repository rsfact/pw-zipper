import string
import secrets
import os
import sys
import subprocess
import configparser
import pyperclip


config = configparser.ConfigParser()
config.read('settings.ini', encoding="utf-8")

SEVENZIP = str(config['DEFAULT']['7zip'])
MX = int(config['DEFAULT']['level'])

def create_pass(num):
    alphabet = string.ascii_letters + string.digits
    alphabet = ''.join(c for c in alphabet if ord(c) < 128)
    password = ''.join(secrets.choice(alphabet) for _ in range(num))
    return password

def read_template(template_file):
    with open(template_file, 'r', encoding='utf-8') as file:
        return file.read()

def generate_output(template, file_name, password):
    return template.format(file=file_name, pw=password)

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        print("複数ファイルの場合はフォルダをドロップしてください。\n\n")
        input("Enterキーを押して画面を閉じます。")
        sys.exit(1)

    print(f"圧縮率: {(MX+1)*10}%")
    print("圧縮中...")

    input_path = os.path.abspath(sys.argv[1])
    if os.path.isfile(input_path):
        input_dir_path = os.path.dirname(input_path)
        input_file_name = os.path.basename(input_path)
        is_file = True
        output_dir_path = input_dir_path
    elif os.path.isdir(input_path):
        input_dir_path = input_path
        input_file_name = '*'
        is_file = False
        output_dir_path = os.path.dirname(input_dir_path)

    template = read_template('template.txt')

    if is_file:
        output_file_name = os.path.splitext(input_file_name)[0] + '.zip'
    else:
        output_file_name = os.path.basename(input_dir_path) + '.zip'

    pw = create_pass(10)

    args = [
        SEVENZIP,
        'a',
        os.path.join(output_dir_path, output_file_name),
        os.path.join(input_dir_path, input_file_name),
        f'-mx={MX}',
        f'-p{pw}'
    ]

    result = subprocess.run(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    output = generate_output(template, output_file_name, pw)

    print("完了\n")
    print("-----コピー: ここから-----\n\n")
    print(output)
    print("-----コピー: ここまで-----\n\n")
    input("Enterキーを押すとコピーされます。")
    pyperclip.copy(output)

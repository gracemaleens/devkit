import string
import subprocess
import random

import click

from dependencies import *


@click.group()
def devkit():
    pass


@devkit.command('gen-key')
@click.option('-ks', '--keystore', prompt='密钥库路径', help='密钥库绝对路径')
@click.option('-ks-pass', '--ks-pass', prompt='密钥库口令', help='密钥库口令')
@click.option('-alias', '--alias', prompt='别名', help='别名')
@click.option('-key-pass', '--key-pass', prompt='密钥口令', help='密钥口令，如果与密钥库口令相同，则不需指定')
def generate_key(keystore, ks_pass, alias, key_pass):
    """生成签名"""
    cmd = (
        'keytool '
        '-genkeypair '
        '-v '
        f'-keystore {keystore} '
        '-keyalg RSA '
        '-keysize 2048 '
        '-validity 10000 '
        f'-storepass {ks_pass} '
        f'-alias {alias} '
        '-noprompt '
        '-dname '
        '"'
        f'CN={_generate_random_string(random.randint(5, 10))}, '
        f'OU={_generate_random_string(random.randint(5, 10))}, '
        f'O={_generate_random_string(random.randint(5, 10))}, '
        f'L={_generate_random_string(random.randint(5, 10))}, '
        f'S={_generate_random_string(random.randint(5, 10))}, '
        f'C={_generate_random_string(random.randint(5, 10))}'
        '"'
    )
    if key_pass is not None:
        cmd += f' -keypass {key_pass}'
    os.system(cmd)


def _generate_random_string(length: int):
    return ''.join(random.choices(string.ascii_letters, k=length))


@devkit.command('export-pepk')
@click.option('-ks', '--keystore', prompt='密钥库路径', help='密钥库绝对路径')
@click.option('-ks-pass', '--ks-pass', prompt='密钥库口令', help='密钥库口令')
@click.option('-a', '--alias', prompt='别名', help='别名')
@click.option('-key-pass', '--key-pass', prompt='密钥口令', help='密钥口令')
@click.option('-o', '--output', default='', help='输出路径')
@click.option('-epk', '--encryption-public-key-path', prompt='加密公钥',
              help='从Google Play Console下载的pem格式的加密公钥')
def export_play_encrypt_private_key(keystore, ks_pass, alias, key_pass, output, encryption_public_key_path):
    if output is None or len(output) <= 0:
        output = f'{os.path.splitext(keystore)[0]}-encrypted.zip'

    if os.path.exists(output):
        os.remove(output)

    """导出Google play签名私钥"""
    cmd = f'"D:\\Program Files\\OpenLogic\\jdk-11.0.20.8-hotspot\\bin\\java" -jar {PEPK} ' \
          f'--keystore={keystore} ' \
          f'--alias={alias} ' \
          f'--output={output} ' \
          f'--include-cert ' \
          f'--rsa-aes-encryption ' \
          f'--encryption-key-path="{encryption_public_key_path}" ' \
          f'--keystore-pass={ks_pass} ' \
          f'--key-pass={key_pass}'

    subprocess.run(cmd)


@devkit.command('install-apks')
@click.option('-apks', '--apks', prompt='apks路径', help='apks路径')
@click.option('-d', '--device-id', help='如果连接了多个设备，需要指定目标设备id')
def install_apks(apks, device_id):
    cmd = f'java -jar {BUNDLETOOL} install-apks --apks={apks}'
    if device_id is not None:
        cmd += f' --device-id {device_id}'
    subprocess.run(cmd)


if __name__ == '__main__':
    devkit()
    # export_play_encrypt_private_key(
    #     'D:\\Codes\\Signings\\flappy-fish.keystore',
    #     '123456',
    #     '123456',
    #     'flappy-fish',
    #     None,
    #     'D:\\Work\\Games\\FlappyFish\\FlappyFishUnderseaExploration.pem'
    # )

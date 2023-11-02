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
    cmd = f'keytool ' \
          f'-genkeypair ' \
          f'-v ' \
          f'-keystore {keystore} ' \
          f'-keyalg RSA ' \
          f'-keysize 2048 ' \
          f'-validity 10000 ' \
          f'-storepass {ks_pass} ' \
          f'-alias {alias}'
    if key_pass is not None:
        cmd += f' -keypass {key_pass}'
    os.system(cmd)
    
    
@devkit.command('export-pepk')
@click.option('-ks', '--keystore', prompt='密钥库路径', help='密钥库绝对路径')
@click.option('-a', '--alias', prompt='别名', help='别名')
@click.option('-o', '--output', default='', help='输出路径')
@click.option('-epk', '--encryption-public-key-path', prompt='加密公钥', help='从Google Play Console下载的pem格式的加密公钥')
def export_play_encrypt_private_key(keystore, alias, output, encryption_public_key_path):
    if output is None or len(output) <= 0:
        output = f'{os.path.splitext(keystore)[0]}-encrypted.zip'

    """导出Google play签名私钥"""
    cmd = f'java -jar {PEPK} ' \
          f'--keystore={keystore} ' \
          f'--alias={alias} ' \
          f'--output={output} ' \
          f'--include-cert '\
          f'--rsa-aes-encryption ' \
          f'--encryption-key-path={encryption_public_key_path}'
    os.system(cmd)
    
    
@devkit.command('install-apks')
@click.option('-apks', '--apks', prompt='apks路径', help='apks路径')
@click.option('-d', '--device-id', help='如果连接了多个设备，需要指定目标设备id')
def install_apks(apks, device_id):
    cmd = f'java -jar {BUNDLETOOL} install-apks --apks={apks}'
    if device_id is not None:
        cmd += f' --device-id {device_id}'
    os.system(cmd)
    

if __name__ == '__main__':
    devkit()

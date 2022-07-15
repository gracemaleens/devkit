import os

import click


@click.group()
def devkit():
    pass


@devkit.command('gen-key')
@click.option('-ks', '--keystore', prompt='密钥库名称', help='密钥库名称')
@click.option('-ks-pass', '--ks-pass', prompt='密钥库口令', help='密钥库口令')
@click.option('-alias', '--alias', prompt='别名', help='别名')
@click.option('-key-pass', '--key-pass', prompt='密钥口令', help='密钥口令，如果与密钥库口令相同，则不需指定')
def generate_key(keystore, ks_pass, alias, key_pass):
    """生成签名"""
    cmd = f'keytool -genkeypair -v -keystore {keystore} -keyalg RSA -keysize 2048 -validity 10000 ' \
          f'-storepass {ks_pass} -alias {alias}'
    if key_pass is not None:
        cmd += f' -keypass {key_pass}'
    os.system(cmd)
    
    
@devkit.command('export-pepk')
@click.option('-ks', '--keystore', prompt='密钥库名称', help='密钥库名称')
@click.option('-a', '--alias', prompt='别名', help='别名')
@click.option('-o', '--output', prompt='输出路径', help='输出路径')
def export_play_encrypt_private_key(keystore, alias, output):
    """导出Google play签名私钥"""
    cmd = f'%pepk% --keystore={keystore} --alias={alias} --output={output} --include-cert '\
          f'--encryptionkey'\
          f'=eb10fe8f7c7c9df715022017b00c6471f8ba8170b13049a11e6c09ffe3056a104a3bbe4ac5a955f4ba4fe93fc8cef27558a3eb'\
          f'9d2a529a2092761fb833b656cd48b9de6a'
    os.system(cmd)
    
    
@devkit.command('install-apks')
@click.option('-apks', '--apks', prompt='apks路径', help='apks路径')
@click.option('-d', '--device-id', help='如果连接了多个设备，需要指定目标设备id')
def install_apks(apks, device_id):
    cmd = f'%bundletool% install-apks --apks={apks}'
    if device_id is not None:
        cmd += f' --device-id {device_id}'
    os.system(cmd)
    

if __name__ == '__main__':
    devkit()

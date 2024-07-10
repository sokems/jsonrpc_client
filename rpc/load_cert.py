def load_cert_and_key(cert_path, key_path):
    with open(cert_path, 'r') as cert_file:
        cert = cert_file.read()
    with open(key_path, 'r') as key_file:
        key = key_file.read()
    return cert, key

# Путь к файлам сертификата и ключа
CERT_PATH = 'rpc/client2024test.crt'
KEY_PATH = 'rpc/client2024test.key'

# Содержимое сертификата и ключа
CERTIFICATE, PRIVATE_KEY = load_cert_and_key(CERT_PATH, KEY_PATH)
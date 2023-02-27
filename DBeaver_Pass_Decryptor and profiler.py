# https://stackoverflow.com/questions/39928401/recover-db-password-stored-in-my-dbeaver-connection

# requires pycryptodome lib (pip install pycryptodome)

import sys
import base64
import os
import json
import platform
from ast import literal_eval

# pip install pycryptodome

from Crypto.Cipher import AES

if (platform.system()) == 'Windows':
    default_paths = [
        # '~/Library/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        # '~/.local/share/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        # '~/.local/share/.DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        # '~/AppData/Roaming/DBeaverData/workspace6/General/.dbeaver/credentials-config.json',
        r'C:\Users\TalW\AppData\Local\Packages\DBeaverCorp.DBeaverCE_1b7tdvn0p0f9y\LocalCache\Roaming\DBeaverData'
        r'\workspace6\General\.dbeaver\credentials-config.json'
    ]
elif (platform.system()) == 'Darwin':
    print('TODO')

if len(sys.argv) < 2:
    for path in default_paths:
        filepath = os.path.expanduser(path)
        try:
            f = open(filepath, 'rb')
            f.close()
            break
        except Exception as e:
            pass
else:
    filepath = sys.argv[1]

print(filepath)

# PASSWORD_DECRYPTION_KEY = bytes([-70, -69, 74, -97, 119, 74, -72, 83, -55, 108, 45, 101, 61, -2, 84, 74])
PASSWORD_DECRYPTION_KEY = bytes([186, 187, 74, 159, 119, 74, 184, 83, 201, 108, 45, 101, 61, 254, 84, 74])

# opening the object as a bytes object (Raw Binary), not a str object
data = open(filepath, 'rb').read()

decryptor = AES.new(PASSWORD_DECRYPTION_KEY, AES.MODE_CBC, data[:16])
padded_output = decryptor.decrypt(data[16:])
output = padded_output.rstrip(padded_output[-1:])
print(type(output))
output_to_json = literal_eval(output.decode('utf8'))
print(type(output_to_json))


# JSON data that we want to add to a new data-sources 2.json file in the \.dbeaver folder
def create_new_data_sources_file(name=None, host=None, database=None):
    data_sources = {
        "folders": {},
        "connections": {
            "postgres-jdbc-1840428109c-5738813cb6c37d2b": {
                "provider": "postgresql",
                "driver": "postgres-jdbc",
                "name": name,
                "save-password": true,
                "read-only": false,
                "configuration": {
                    "host": host,
                    "port": "5432",
                    "database": database,
                    "url": "jdbc:postgresql://" + host + ":5432/" + database + "\"",
                    "type": "dev",
                    "provider-properties": {
                        "@dbeaver-show-non-default-db@": "false",
                        "@dbeaver-show-template-db@": "false",
                        "@dbeaver-show-unavailable-db@": "false",
                        "show-database-statistics": "false",
                        "@dbeaver-read-all-data-types-db@": "false",
                        "read-keys-with-columns": "false",
                        "@dbeaver-use-prepared-statements-db@": "false",
                        "postgresql.dd.plain.string": "false",
                        "postgresql.dd.tag.string": "false"
                    },
                    "auth-model": "native"
                }
            }
        }
    }
    with open(default_paths / "data-sources - 2.json", "w") as outfile:
        json.dump(data_sources, outfile)


try:
    print(json.dumps(json.loads(output), indent=4, sort_keys=True))
except:
    print(output)

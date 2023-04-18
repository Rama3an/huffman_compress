from huffman_compress import HuffmanCompress
import argparse
from hashlib import sha256
from loguru import logger

logger.remove()

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='file', type=str, help='path to compress')
parser.add_argument('-d', '--DEBUG', help='DEBUG, default False', action='store_true')
parser.add_argument('-c', '--compress', help='huffman compress file', action='store_true')
parser.add_argument('-dc', '--decompress', help='huffman decompress file', action='store_true')
args = parser.parse_args()
path = args.path

logger.add('log/loging.log', format='{time} {level} {message}', rotation='1 day') if args.DEBUG else None

dict_arg = {args.compress: HuffmanCompress(path).compress,
            args.decompress: HuffmanCompress(path).decompress}

for k in dict_arg.keys():
    if k:
        try:
            dict_arg.get(k, None)()
        except Exception:
            logger.error('File is warning')

if path == 'help':
    HuffmanCompress.print_help()
elif not (args.decompress or args.compress):
    h_comp = HuffmanCompress(path).compress()
    h_dec = HuffmanCompress(h_comp).decompress()
    with open(h_comp, 'rb') as file_comp, open(h_dec, 'r') as file_dec:
        hash_file_comp = file_comp.readlines()[1][:-1].decode()
        hash_file_dec = sha256(file_dec.read().encode()).hexdigest()
        if hash_file_dec != hash_file_comp:
            logger.error('File not compiling')
        else:
            logger.debug('File compile')

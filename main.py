from huffman_compress import HuffmanCompress
import argparse
from loguru import logger

logger.remove()

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='file', type=str, help='path to compress')
parser.add_argument('-d', '--DEBUG', help='DEBUG, default False', action='store_true')
parser.add_argument('-c', '--compress', help='huffman compress file', action='store_true')
parser.add_argument('-dc', '--decompress', help='huffman decompress file', action='store_true')
args = parser.parse_args()

logger.add('debug.log', format='{time} {level} {message}', rotation='1 day') if args.DEBUG else None

path = args.path
dict_arg = {args.compress: HuffmanCompress(path).compress,
            args.decompress: HuffmanCompress(path).decompress}

for k in dict_arg.keys():
    if k:
        try:
            dict_arg.get(k, None)()
        except:
            logger.error('File is warning')

if path == 'help':
    HuffmanCompress.print_help()
elif not (args.decompress or args.compress):
    h_comp = HuffmanCompress(path).compress()
    h_dec = HuffmanCompress(h_comp).decompress()
    with open(path, 'rb') as file_base, open(h_dec, 'rb') as file_dec:
        if file_dec.read().split() != file_base.read().split():
            logger.error('File not compiling')

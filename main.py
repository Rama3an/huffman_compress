from huffman_compress import HuffmanCompress
import argparse
from loguru import logger

logger.remove()
log = lambda: logger.add('debug.log', format='{time} {level} {message}', level='DEBUG', rotation='1 day')

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='file', type=str, help='path to compress')
parser.add_argument('-d', '--DEBAG', help='DEBAG, default False', action='store_true')
parser.add_argument('-c', '--compress', help='huffman compress file', action='store_true')
args = parser.parse_args()
path = args.path
dict_arg = {args.DEBAG: log, args.compress: HuffmanCompress(path).compress}

for k in dict_arg.keys():
    if k:
        dict_arg.get(k)()

if path == 'help':
    HuffmanCompress.print_help()
else:
    h = HuffmanCompress(path)
    output_path = h.compress()
    h.decompress(output_path)

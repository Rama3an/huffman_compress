from huffman_compress import HuffmanCompress, check_hash_logging, check_password_logging
import argparse
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

try:
    if args.decompress:
        h_dec = HuffmanCompress(path).decompress()
        check_password_logging(path)
        check_hash_logging(path, h_dec)
    elif args.compress:
        h_dec = HuffmanCompress(path).compress()
except:
    logger.error('File is warning')

if path == 'help':
    HuffmanCompress.print_help()
elif not (args.decompress or args.compress):
    try:
        h_comp = HuffmanCompress(path).compress()
        check_password_logging(h_comp)
        h_dec = HuffmanCompress(h_comp).decompress()
        check_hash_logging(h_comp, h_dec)
    except:
        logger.error('File is warning')

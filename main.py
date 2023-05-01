from huffman_compress import HuffmanCompress, check_hash_logging, check_password_logging, get_result_compress
import argparse
from loguru import logger

logger.remove()

parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='file', type=str,
                    help='path to compress')
parser.add_argument('-d', '--DEBUG',
                    help='DEBUG, default False', action='store_true')
parser.add_argument('-c', '--compress',
                    help='huffman compress file', action='store_true')
parser.add_argument('-dc', '--decompress',
                    help='huffman decompress file', action='store_true')
parser.add_argument('-t', '--test',
                    help='huffman test file', action='store_true')
args = parser.parse_args()
path = args.path

logger.add('log/loging.log', format='{time} {level} {message}',
           rotation='1 day') if args.DEBUG else None

directory_key = 'file/'
if args.test:
    directory_key = 'test/'

try:
    if args.decompress:
        check_password_logging(path, test_key=args.test)
        path_dec = HuffmanCompress(path).decompress()
        check_hash_logging(path, path_dec, test_key=args.test)
    elif args.compress:
        path_comp = HuffmanCompress(path).compress(
            directory_key_codes=directory_key, test_key=args.test)
        print(get_result_compress(path, path_comp))
except:
    logger.error('file is warning')

if path == 'help':
    HuffmanCompress.return_help()
elif not (args.decompress or args.compress):
    try:
        path_comp = HuffmanCompress(path).compress(
            directory_key_codes=directory_key, test_key=args.test)
        print(get_result_compress(path, path_comp))
        check_password_logging(path_comp, test_key=args.test)
        path_dec = HuffmanCompress(path_comp).decompress()
        check_hash_logging(path_comp, path_dec, test_key=args.test)
    except:
        logger.error('file is warning')

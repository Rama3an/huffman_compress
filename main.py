from huffman_compress import HuffmanCompress
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('path', metavar='file', type=str, help='path to compress')
args = parser.parse_args()
path = args.path

if path == 'help':
    HuffmanCompress.print_help()
else:
    h = HuffmanCompress(path)
    output_path = h.compress()
    h.decompress(output_path)


#while True:
#    input_data = input()
#    if input_data == 'continue':
#        path = input()
#        try:
#            h = HuffmanCompress(path)
#            output_path = h.compress()
#            h.decompress(output_path)
#            break
#        except FileNotFoundError:
#            raise FileNotFoundError('Файл не найден')
#    if input_data == 'help':
#        HuffmanCompress.print_help()
#        continue

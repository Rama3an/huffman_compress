from unittest import main, TestCase

from huffman_compress import *


class TestHuffmanCoding(TestCase):

    def setUp(self):
        self.path_compress = 'test_input.txt'
        self.path_decompress = 'test_input_compressed.bin'
        self.hc = HuffmanCompress(self.path_compress)
        self.hdc = HuffmanCompress(self.path_decompress)
        self.path_compress_positive = 'test_input_positive.txt'
        self.path_decompress_positive = 'test_input_positive_compressed.bin'

    def test_make_frequency_dict(self):
        text = "abbc"
        expected_result = {'a': 1, 'b': 2, 'c': 1}
        result = self.hc.make_frequency_dict(text)
        self.assertEqual(result, expected_result)

    def test_merge_nodes(self):
        frequency = {'a': 1, 'b': 2, 'c': 1}
        self.hc.make_heap(frequency)
        expected_result = self.hc.HeapNode(None, 4)
        expected_result.left = self.hc.HeapNode('b', 2)
        expected_result.right = self.hc.HeapNode(None, 2)
        expected_result.right.left = self.hc.HeapNode('a', 1)
        expected_result.right.right = self.hc.HeapNode('c', 1)
        self.hc.merge_nodes()
        result = self.hc.heap[0]
        self.assertEqual(result.freq, expected_result.freq)
        self.assertEqual(result.left.char, expected_result.left.char)
        self.assertEqual(result.right.char, expected_result.right.char)

    def test_make_codes_helper(self):
        frequency = {'a': 1, 'b': 2, 'c': 1}
        self.hc.make_heap(frequency)
        self.hc.merge_nodes()
        expected_result = {'a': '10', 'c': '11', 'b': '0'}
        root = self.hc.heap[0]
        current_code = ""
        self.hc.make_codes_helper(root, current_code)
        result = self.hc.codes
        self.assertEqual(result, expected_result)

    def test_get_encoded_text(self):
        text = "abbc"
        expected_result = '100011'
        frequency = self.hc.make_frequency_dict(text)
        self.hc.make_heap(frequency)
        self.hc.merge_nodes()
        self.hc.make_codes()
        result = self.hc.get_encoded_text(text)
        self.assertEqual(result, expected_result)

    def test_pad_encoded_text(self):
        encoded_text = '01110'
        expected_result = '0000001101110000'
        result = self.hc.pad_encoded_text(encoded_text)
        self.assertEqual(result, expected_result)

    def test_get_byte_array(self):
        padded_encoded_text = '0000001101110000'
        expected_result = bytearray(b'\x03p')
        result = self.hc.get_byte_array(padded_encoded_text)
        self.assertEqual(result, expected_result)

    def test_compress(self):
        with (open(self.path_decompress, 'rb') as expected_path,
              open(self.hc.compress(test_key=True), 'rb') as path):
            expected_result = expected_path.read().split()
            result = path.read().split()
        self.assertEqual(result, expected_result)

    def test_decompress(self):
        with open(self.path_compress, 'r') as expected_path, \
                open(self.hdc.decompress(test_key=True), 'r') as path:
            expected_result = expected_path.read().split()
            result = path.read().split()
        self.assertEqual(result, expected_result)

    def test_make_file_codes(self):
        expected_result = 'code_0.txt'
        self.hc.compress(test_key=True)
        self.hc.make_file_codes()
        result = f'code_{self.hc.count}.txt'
        self.assertEqual(result, expected_result)

    def test_check_hash_logging_matched(self):
        expected_result = 'Hashes matched'
        result = check_hash_logging(self.hc.compress(test_key=True),
                                    self.hdc.decompress(test_key=True),
                                    test_key=True)
        self.assertEqual(result, expected_result)

    def test_check_password_logging_correct(self):
        expected_result = 'Password correct'
        result = check_password_logging(self.hc.compress(test_key=True),
                                        test_key=True)
        self.assertEqual(result, expected_result)

    def test_check_password_logging_incorrect(self):
        expected_result = 'Password incorrect'
        result = check_password_logging(self.hc.compress(test_key=True),
                                        test_key=True, password='incorrect')
        self.assertEqual(result, expected_result)

    def test_get_result_compress_negative(self):
        expected_result = 'Compress: -16.47%'
        result = get_result_compress(self.path_compress,
                                     self.path_decompress)
        self.assertEqual(result, expected_result)

    def test_get_result_compress_positive(self):
        expected_result = 'Compress: 33.47%'
        result = get_result_compress(self.path_compress_positive,
                                     self.path_decompress_positive)
        self.assertEqual(result, expected_result)

    def test_print_help(self):
        expected_result = "Программа HuffmanCompress позволяет архивировать "
        "и разархивировать текстовые файлы с помощью алгоритма "
        "Хаффмана.\n"
        "Использование:\n"
        "\thuffmancoding = HuffmanCompress(path/to/file)\n"
        "\tСжатие файла: huffmancoding.compress()"
        "(Можно использовать ключ '-c' в командной строке, "
        "чтобы файл только архивировался)\n"
        "\tРазархивирование файла: huffmancoding.decompress"
        "('path/to/compressed/file.bin')"
        "(Можно использовать ключ '-dc' в командной строке,"
        " чтобы файл только архивировался)\n"
        "\tПри использовании ключа '-d' все действия будут"
        " логироваться и сохраняться"
        " в соответствующий файл (loging.log)"
        result = self.hc.return_help()
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    main()

import unittest
from huffman_compress import HuffmanCompress, check_hash_logging, check_password_logging, get_result_compress


class TestHuffmanCoding(unittest.TestCase):

    def setUp(self):
        self.path_compress = 'test_input.txt'
        self.path_decompress = 'test_input_compressed.bin'
        self.hdc = HuffmanCompress(self.path_decompress)
        self.hc = HuffmanCompress(self.path_compress)

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
        with open(self.path_compress, 'r') as expected_path, open(self.hdc.decompress(test_key=True), 'r') as path:
            expected_result = expected_path.read().split()
            result = path.read().split()
        self.assertEqual(result, expected_result)

    def test_make_file_codes(self):
        expected_result = 'code_0.txt'
        self.hc.compress(test_key=True)
        self.hc.make_file_codes()
        result = f'code_{self.hc.count}.txt'
        self.assertEqual(result, expected_result)

    def test_check_hash_logging(self):
        expected_result = 'Hashes matched'
        result = check_hash_logging(self.hc.compress(test_key=True),
                                    self.hdc.decompress(test_key=True),
                                    test_key=True)
        self.assertEqual(result, expected_result)

    def test_check_password_logging(self):
        expected_result = 'Password correct'
        result = check_password_logging(self.hc.compress(test_key=True),
                                        test_key=True)
        self.assertEqual(result, expected_result)

    def test_get_result_compress(self):
        express_result = 'Compress: -18.82%'
        result = get_result_compress(self.path_compress, self.path_decompress)
        self.assertEqual(result, express_result)

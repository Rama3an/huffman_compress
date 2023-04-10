import unittest
from huffman_compress import HuffmanCompress


class TestHuffmanCoding(unittest.TestCase):

    def setUp(self):
        self.path = 'test_input.txt'
        self.hc = HuffmanCompress(self.path)

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
        expected_result = 'test_input_compressed.bin'
        result = self.hc.compress()
        self.assertEqual(result, expected_result)

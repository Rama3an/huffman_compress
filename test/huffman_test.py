from unittest import main, TestCase
from huffman_compress.huffman_compress import HuffmanCompress


class TestHuffmanCoding(TestCase):

    def setUp(self):
        self.path = "test_file/test_input.txt"
        self.path_compress = "test_file/test_input_compressed.bin"
        self.huffman_compress = HuffmanCompress(self.path)
        self.huffman_decompress = HuffmanCompress(self.path_compress)
        self.path_positive = "test_file/test_input_positive.txt"
        self.path_compress_positive = "test_file/test_input_positive_compressed.bin"

    def test_make_frequency_dict(self):
        text = "abbc"
        expected_result = {"a": 1, "b": 2, "c": 1}
        result = self.huffman_compress.make_frequency_dict(text)
        self.assertEqual(result, expected_result)

    def test_merge_nodes(self):
        frequency = {"a": 1, "b": 2, "c": 1}
        self.huffman_compress.make_heap(frequency)
        expected_result = self.huffman_compress.heap_node(None, 4)
        expected_result.left = self.huffman_compress.heap_node("b", 2)
        expected_result.right = self.huffman_compress.heap_node(None, 2)
        expected_result.right.left = self.huffman_compress.heap_node("a", 1)
        expected_result.right.right = self.huffman_compress.heap_node("c", 1)
        self.huffman_compress.merge_nodes()
        result = self.huffman_compress.heap[0]
        self.assertEqual(result.freq, expected_result.freq)
        self.assertEqual(result.left.char, expected_result.left.char)
        self.assertEqual(result.right.char, expected_result.right.char)

    def test_make_codes_helper(self):
        frequency = {"a": 1, "b": 2, "c": 1}
        self.huffman_compress.make_heap(frequency)
        self.huffman_compress.merge_nodes()
        expected_result = {"a": "10", "c": "11", "b": "0"}
        root = self.huffman_compress.heap[0]
        current_code = ""
        self.huffman_compress.make_codes_helper(root, current_code)
        result = self.huffman_compress.codes
        self.assertEqual(result, expected_result)

    def test_get_encoded_text(self):
        text = "abbc"
        expected_result = "100011"
        frequency = self.huffman_compress.make_frequency_dict(text)
        self.huffman_compress.make_heap(frequency)
        self.huffman_compress.merge_nodes()
        self.huffman_compress.make_codes()
        result = self.huffman_compress.get_encoded_text(text)
        self.assertEqual(result, expected_result)

    def test_pad_encoded_text(self):
        encoded_text = "01110"
        expected_result = "0000001101110000"
        result = self.huffman_compress.pad_encoded_text(encoded_text)
        self.assertEqual(result, expected_result)

    def test_get_byte_array(self):
        padded_encoded_text = "0000001101110000"
        expected_result = bytearray(b"\x03p")
        result = self.huffman_compress.get_byte_array(padded_encoded_text)
        self.assertEqual(result, expected_result)

    def test_compress(self):
        with (open(self.path_compress, "rb") as expected_path,
              open(self.huffman_compress.compress(test_key=True, directory_key_codes="test_file/"), "rb") as path):
            expected_result = expected_path.read().split()
            result = path.read().split()
        self.assertEqual(result, expected_result)

    def test_decompress(self):
        with open(self.path, "r") as expected_path, \
                open(self.huffman_decompress.decompress(test_key=True), "r") as path:
            expected_result = expected_path.read().split()
            result = path.read().split()
        self.assertEqual(result, expected_result)

    def test_make_file_codes(self):
        expected_result = "test_file/code_0.txt"
        self.huffman_compress.compress(test_key=True, directory_key_codes="test_file/")
        self.huffman_compress.make_file_codes(directory_key="test_file/")
        result = f"test_file/code_{self.huffman_compress.count}.txt"
        self.assertEqual(result, expected_result)

    def test_print_help(self):
        expected_result = "Программа HuffmanCompress позволяет архивировать "
        "и разархивировать текстовые файлы с помощью алгоритма "
        "Хаффмана.\n"
        "Использование:\n"
        "\thuffmancoding = HuffmanCompress(path/to/file)\n"
        "\tСжатие файла: huffmancoding.huffman_compress()"
        "(Можно использовать ключ '-c' в командной строке, "
        "чтобы файл только архивировался)\n"
        "\tРазархивирование файла: huffmancoding.decompress"
        "('path/to/compressed/file.bin')"
        "(Можно использовать ключ '-dc' в командной строке,"
        " чтобы файл только архивировался)\n"
        "\tПри использовании ключа '-d' все действия будут"
        " логироваться и сохраняться"
        " в соответствующий файл (loging.log)"
        result = self.huffman_compress.return_help()
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    main()

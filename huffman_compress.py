import heapq
import os
import json
from hashlib import sha256
from loguru import logger


class HuffmanCompress:
    count = 0
    f = True

    def __init__(self, path):
        self.path = path  # путь к исходному файлу
        self.heap = []  # куча, хранящая узлы дерева Хаффмана
        self.codes = {}  # словарь, который хранит коды Хаффмана для каждого символа
        self.reverse_mapping = {}  # перевёрнутый codes

    class HeapNode:  # класс, описывающий узлы дерева
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    @staticmethod
    def make_frequency_dict(text):  # создание словаря частот
        frequency = {}
        for char in text:
            if char not in frequency:
                frequency[char] = 0
            frequency[char] += 1
        return frequency

    def make_heap(self, frequency):  # создание кучи узлов дерева
        for key in frequency:
            node = self.HeapNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):  # этот метод объединяет узлы, так, как описано в алгоритме Хаффмана
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)

            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2

            heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):  # этот метод рекурсивно пробегает по дереву и составляет на его
        # основе коды Хаффмана
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_file_codes(self):
        while True:
            try:
                with open(f'test/code_{HuffmanCompress.count}.txt', 'x'):
                    pass
            except FileExistsError:
                HuffmanCompress.count += 1
                continue
            else:
                break
        with open(f'test/code_{HuffmanCompress.count}.txt', 'w') as path:
            json.dump(self.reverse_mapping, path)

    def make_codes(self):

        root = heapq.heappop(self.heap)
        current_code = ""
        self.make_codes_helper(root, current_code)

    def get_encoded_text(self, text):  # получение закодированного текста

        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    @staticmethod
    def pad_encoded_text(encoded_text):  # делает длину текста кратной 8

        padding_required = 8 - (len(encoded_text) % 8)
        for i in range(padding_required):
            encoded_text += "0"

        padded_info = "{0:08b}".format(padding_required)
        encoded_text = padded_info + encoded_text
        return encoded_text

    @staticmethod
    def get_byte_array(padded_encoded_text):  # перевод закодированного текста в байты

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i + 8]
            b.append(int(byte, 2))
        return b

    def compress(self):  # сжатие

        filename, file_extension = os.path.splitext(self.path)
        output_path = filename + "_compressed.bin"

        with open(self.path, "r+") as file, open(output_path, "wb") as output:
            text = file.read()
            text = text.rstrip()

            frequency = self.make_frequency_dict(text)
            self.make_heap(frequency)
            self.merge_nodes()
            self.make_codes()

            encoded_text = self.get_encoded_text(text)
            padded_encoded_text = self.pad_encoded_text(encoded_text)

            self.make_file_codes()
            b = self.get_byte_array(padded_encoded_text)
            output.writelines([f'test/code_{HuffmanCompress.count}.txt'.encode(),
                               '\n'.encode(),
                               sha256(text.encode()).hexdigest().encode(),
                               '\n'.encode(),
                               bytes(b)])

        logger.debug("Compressed")
        return output_path

    @staticmethod
    def remove_padding(padded_encoded_text):  # удаление добавочных нулей

        padded_info = padded_encoded_text[:8]
        padding_required = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1 * padding_required]

        return encoded_text

    def decode_text(self, encoded_text):  # декодирование

        current_code = ""
        decoded_text = ""
        with open(f'{self.path}', 'rb') as file_compress:
            path = file_compress.readline().decode()[:-1]
            with open(path) as revers_mapping_file:
                reverse_mapping = json.load(revers_mapping_file)

        for bit in encoded_text:
            current_code += bit
            if current_code in reverse_mapping:
                char = reverse_mapping[current_code]
                decoded_text += char
                current_code = ""

        return decoded_text

    def decompress(self):  # разархивация

        filename, file_extension = os.path.splitext(self.path)
        if file_extension != '.bin':
            raise Exception
        output_path = f'{filename}_decompressed.txt'

        with open(self.path, "rb") as file, open(output_path, "w") as output:
            for _ in range(2):
                file.readline()
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

            encoded_text = self.remove_padding(bit_string)
            decompressed_text = self.decode_text(encoded_text)

            output.write(decompressed_text)

        logger.debug("Decompressed")
        return output_path

    @staticmethod
    def print_help():
        print("Программа HuffmanCompress позволяет архивировать и разархивировать "
              "текстовые файлы с помощью алгоритма "
              "Хаффмана.")
        print("Использование:")
        print("\thuffmancoding = HuffmanCompress(path/to/file)")
        print("\tСжатие файла: huffmancoding.compress()"
              "(Можно использовать ключ '-c' в командной строке, чтобы файл только архивировался)")
        print("\tРазархивирование файла: huffmancoding.decompress('path/to/compressed/file.bin')"
              "(Можно использовать ключ '-dc' в командной строке, чтобы файл только архивировался)")
        print("\tПри использовании ключа '-d' все действия будут логироваться и сохраняться"
              " в соответствующий файл (loging.log)")

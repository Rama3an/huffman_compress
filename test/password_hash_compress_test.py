from huffman_compress.password_hash_compress_check import check_password_logging, check_hash_logging, get_result_compress
import pytest


class TestPasswordHashCompress:
    path = "test_file/test_input.txt"
    path_compress = "test_file/test_input_compressed.bin"
    path_decompress = "test_file/test_input_compressed_decompressed.txt"
    path_positive = "test_file/test_input_positive.txt"
    path_compress_positive = "test_file/test_input_positive_compressed.bin"

    @pytest.mark.parametrize("expected_result, compress_path, decompress_path",
                             [
                                 ("Hashes matched", path_compress, path_decompress),
                                 ("Hashes did not match", path_compress, path_positive)
                             ])
    def test_check_hash_logging_matched(self, expected_result, compress_path, decompress_path):
        result = check_hash_logging(compress_path,
                                    decompress_path,
                                    test_key=True)
        assert result == expected_result

    @pytest.mark.parametrize("expected_result, password",
                             [
                                 ("Password correct", "test password"),
                                 ("Password incorrect", "False")
                             ])
    def test_check_password_logging_correct(self, expected_result, password):
        result = check_password_logging(self.path_compress,
                                        test_key=True, password=password)
        assert result == expected_result

    @pytest.mark.parametrize("expected_result, file, file_compress",
                             [
                                 ("Compress: -14.74%", path, path_compress),
                                 ("Compress: 33.57%", path_positive, path_compress_positive)
                             ])
    def test_get_result_compress(self, expected_result, file, file_compress):
        result = get_result_compress(file, file_compress)
        assert result == expected_result

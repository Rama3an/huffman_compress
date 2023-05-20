from loguru import logger
from hashlib import sha256
import getpass
import os


def check_hash_logging(path_comp, path_dec, test_key=False):
    with open(path_comp, "rb") as file_comp, open(path_dec, "r") as file_dec:
        hash_file_comp = file_comp.readlines()[2][:-1].hex()
        hash_file_dec = sha256(file_dec.read().encode()).hexdigest()
    if test_key:
        if hash_file_dec == hash_file_comp:
            return "Hashes matched"
        else:
            return "Hashes did not match"
    else:
        if hash_file_dec == hash_file_comp:
            logger.debug("Hashes matched")
        else:
            logger.error("Hashes did not match")


def check_password_logging(path_comp, test_key=False,
                           password="test password"):
    if not test_key:
        password = getpass.getpass()

    password_hash = sha256(password.encode()).hexdigest()
    with open(path_comp, "rb") as file_comp:
        password_file_hash = file_comp.readlines()[1][:-1].hex()
    if test_key:
        if password_hash == password_file_hash:
            return "Password correct"
        else:
            return "Password incorrect"
    else:
        if password_hash == password_file_hash:
            logger.debug("Password correct")
        else:
            logger.error("Password incorrect")
            quit()


def get_result_compress(path, path_comp):
    percent = 100
    point = 2
    size_path = os.path.getsize(f'{path}')
    size_path_comp = os.path.getsize(f'{path_comp}')
    if size_path < size_path_comp:
        percent_compress = \
            f"Compress: {-round(size_path / size_path_comp * percent, point)}%"
    else:
        percent_compress = \
            f"Compress: {round(size_path_comp / size_path * percent, point)}%"
    return percent_compress

import unittest
import os
from hash_function import generate_digest, _DIGEST_SIZE

class TestSecureHasher(unittest.TestCase):
    def test_output_characteristics(self):
        """Проверка свойств вывода хэша"""
        samples = [b"", b"test", b"long data"*100, os.urandom(512)]  # Тестовые данные
        for data in samples:
            with self.subTest(data=data):  # Проводим тест для каждого примера данных
                digest = generate_digest(data)  # Генерация хэша
                self.assertEqual(len(digest), _DIGEST_SIZE)  # Проверка длины хэша
                self.assertIsInstance(digest, bytes)  # Проверка типа хэша (должен быть bytes)
    
    def test_deterministic_behavior(self):
        """Одинаковые входные данные должны давать одинаковый хэш"""
        data = b"Consistent output test"
        self.assertEqual(generate_digest(data), generate_digest(data))  # Проверка детерминированности

    def test_avalanche_effect(self):
        """Небольшие изменения во входных данных должны сильно менять хэш (лавинный эффект)"""
        digest1 = generate_digest(b"data version 1")
        digest2 = generate_digest(b"data version 2")
        self.assertNotEqual(digest1, digest2)  # Хэши для разных данных не должны быть одинаковыми
        
        # Подсчёт различий в битах
        diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(digest1, digest2))
        self.assertGreater(diff_bits, _DIGEST_SIZE * 2)  # Проверка, что более 50% битов изменилось
    
    def test_input_validation(self):
        """Неверный ввод (не байты) должен вызывать исключение TypeError"""
        invalid_inputs = ["string", 12345, None, [b"list"]]  # Некорректные данные
        for data in invalid_inputs:
            with self.subTest(data=data), self.assertRaises(TypeError):  # Проверка исключения для неверных данных
                generate_digest(data)
    
    def test_edge_cases(self):
        """Тестирование граничных случаев"""
        # Пустые данные
        empty_digest = generate_digest(b"")
        self.assertEqual(len(empty_digest), _DIGEST_SIZE)  # Проверка хэша для пустых данных
        
        # Один байт
        self.assertNotEqual(generate_digest(b"\x00"), generate_digest(b"\x01"))  # Проверка, что разные байты дают разные хэши
        
        # Большие данные
        large_data = os.urandom(10 * 1024 * 1024)  # 10МБ данных
        digest = generate_digest(large_data)  # Генерация хэша для больших данных
        self.assertEqual(len(digest), _DIGEST_SIZE)  # Проверка длины хэша для больших данных

if __name__ == "__main__":
    unittest.main()  # Запуск тестов

import unittest
import os
from hash_util import byte_hash, HASH_SIZE

class TestByteHash(unittest.TestCase):
    def setUp(self):
        self.test_vectors = [
            (b"", "a3d9c4e1b8f6d2c5a7e9b1d3f5c7e9a1b3d5f7c9e1b3d5f7a9c1e3b5d7f9"),
            (b"hello", "c2e4f6a8b1d3c5e7f9a2b4d6c8e1a3b5d7f9c1e3b5d7"),
            (b"password", "e1a3c5e7b9d2f4a6c8e1b3d5f7a9c2e4f6b8d1a3c5")
        ]
    
    def test_hash_length(self):
        """Проверка длины хеша"""
        for data, _ in self.test_vectors:
            h = byte_hash(data)
            self.assertEqual(len(h), HASH_SIZE)
    
    def test_empty_input(self):
        """Проверка пустого ввода"""
        h = byte_hash(b"")
        self.assertEqual(len(h), HASH_SIZE)
    
    def test_determinism(self):
        """Проверка детерминированности"""
        data = b"test data"
        h1 = byte_hash(data)
        h2 = byte_hash(data)
        self.assertEqual(h1, h2)
    
    def test_avalanche_effect(self):
        """Проверка лавинного эффекта"""
        h1 = byte_hash(b"data1")
        h2 = byte_hash(b"data2")
        diff = sum(b1 != b2 for b1, b2 in zip(h1, h2))
        self.assertGreater(diff, HASH_SIZE//2)
    
    def test_large_input(self):
        """Проверка большого ввода"""
        data = os.urandom(1024*1024)  # 1MB данных
        h = byte_hash(data)
        self.assertEqual(len(h), HASH_SIZE)
    
    def test_type_check(self):
        """Проверка обработки неверных типов"""
        with self.assertRaises(TypeError):
            byte_hash("string")
        with self.assertRaises(TypeError):
            byte_hash(123)
    
    def test_known_vectors(self):
        """Проверка известных значений"""
        for data, expected in self.test_vectors:
            h = byte_hash(data).hex()
            self.assertEqual(h[:len(expected)], expected)

if __name__ == "__main__":
    unittest.main()
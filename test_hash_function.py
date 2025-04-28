import unittest
import os
from hash_function import generate_digest, _DIGEST_SIZE

class TestSecureHasher(unittest.TestCase):
    def test_output_characteristics(self):
        """Verify digest output properties"""
        samples = [b"", b"test", b"long data"*100, os.urandom(512)]
        for data in samples:
            with self.subTest(data=data):
                digest = generate_digest(data)
                self.assertEqual(len(digest), _DIGEST_SIZE)
                self.assertIsInstance(digest, bytes)
    
    def test_deterministic_behavior(self):
        """Same input should produce same digest"""
        data = b"Consistent output test"
        self.assertEqual(generate_digest(data), generate_digest(data))
    
    def test_avalanche_effect(self):
        """Small changes should drastically change digest"""
        digest1 = generate_digest(b"data version 1")
        digest2 = generate_digest(b"data version 2")
        self.assertNotEqual(digest1, digest2)
        
        # Count differing bits
        diff_bits = sum(bin(b1 ^ b2).count('1') for b1, b2 in zip(digest1, digest2))
        self.assertGreater(diff_bits, _DIGEST_SIZE * 2)  # At least 50% bits changed
    
    def test_input_validation(self):
        """Non-bytes input should raise TypeError"""
        invalid_inputs = ["string", 12345, None, [b"list"]]
        for data in invalid_inputs:
            with self.subTest(data=data), self.assertRaises(TypeError):
                generate_digest(data)
    
    def test_edge_cases(self):
        """Test special boundary conditions"""
        # Empty input
        empty_digest = generate_digest(b"")
        self.assertEqual(len(empty_digest), _DIGEST_SIZE)
        
        # Single byte
        self.assertNotEqual(generate_digest(b"\x00"), generate_digest(b"\x01"))
        
        # Large input
        large_data = os.urandom(10 * 1024 * 1024)  # 10MB
        digest = generate_digest(large_data)
        self.assertEqual(len(digest), _DIGEST_SIZE)

if __name__ == "__main__":
    unittest.main()
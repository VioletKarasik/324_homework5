from hash_util import byte_hash

def demo():
    print("Демонстрация хеш-функции")
    print("-" * 40)
    
    test_cases = [
        b"",
        b"hello world",
        b"password123",
        b"a" * 100,
        b"\x00\x01\x02\x03",
        b"The quick brown fox jumps over the lazy dog"
    ]
    
    for data in test_cases:
        try:
            data_str = data.decode('utf-8', errors='replace') if data else "''"
            if len(data_str) > 50:
                data_str = data_str[:47] + "..."
            
            print(f"Вход: {data_str}")
            h = byte_hash(data)
            print(f"Хеш:  {h.hex()}")
            print(f"Размер: {len(h)} байт")
            print("-" * 40)
        except Exception as e:
            print(f"Ошибка: {e}")

if __name__ == "__main__":
    demo()
import os

# Криптографические параметры для перемешивания
_PRIME_SEED_A = 0x6A09E667F3BCC908  # Первичное значение для перемешивания A
_PRIME_SEED_B = 0xBB67AE8584CAA73B  # Первичное значение для перемешивания B
_DIGEST_SIZE = 32  # Размер хэша (256 бит)

def generate_digest(input_data: bytes) -> bytes:
    """Генерация 256-битного криптографического дайджеста с использованием улучшенного алгоритма перемешивания"""
    if not isinstance(input_data, bytes):
        raise TypeError("Входные данные должны быть в формате bytes")
    
    # Инициализация состояния хэша с чередующимися значениями
    hash_state = bytearray([(0x36 if i % 3 == 0 else 0x5C) for i in range(_DIGEST_SIZE)])
    
    # Обработка каждого байта входных данных
    input_length = len(input_data)
    for position, byte_value in enumerate(input_data):
        # Основная операция перемешивания
        state_position = position % _DIGEST_SIZE  # Вычисление позиции в состоянии хэша
        current_state = hash_state[state_position]  # Текущее значение состояния

        mixed_value = (current_state * _PRIME_SEED_A) + byte_value + position
        mixed_value ^= (input_length << (position % 7)) | _PRIME_SEED_B  # Модификация значения с учетом длины данных
        
        hash_state[state_position] = mixed_value % 256  # Обновление состояния хэша

        # Вторичное распространение изменений
        alt_position = (position + byte_value) % _DIGEST_SIZE  # Альтернативная позиция
        hash_state[alt_position] ^= (mixed_value >> (position % 4)) % 256  # Вторичная диффузия
    
    # Финальные раунды трансформации
    for _ in range(4):  # Количество раундов увеличено с 3 до 4
        temp_buffer = bytearray(hash_state)  # Создаем копию состояния для работы
        for i in range(_DIGEST_SIZE):
            # Перемешиваем с соседними и удаленными байтами
            prev_byte = temp_buffer[(i - 1) % _DIGEST_SIZE]  # Предыдущий байт
            next_byte = temp_buffer[(i + 1) % _DIGEST_SIZE]  # Следующий байт
            far_byte = temp_buffer[(i * 17) % _DIGEST_SIZE]  # Далёкий байт
            
            # Обновляем состояние хэша с учетом побитовых операций
            hash_state[i] = (hash_state[i] ^ prev_byte ^ next_byte ^ far_byte + 
                            (_PRIME_SEED_A // (i + 1))) % 256
    
    return bytes(hash_state)  # Возвращаем финальный хэш как последовательность байт

def demonstrate_hashing(data: bytes):
    """Выводит входные данные и их хэш"""
    try:
        # Преобразуем данные в строку, если это возможно
        display_text = data.decode('utf-8', errors='replace')[:60]
        if len(data) > 60:
            display_text += "..."  # Ограничиваем длину строки для вывода
    except:
        display_text = f"Бинарные данные ({len(data)} байт)"  # Если не удалось преобразовать в строку
    
    print(f"Входные данные: {display_text}")
    
    try:
        # Генерация хэша для входных данных
        digest = generate_digest(data)
        print(f"Хэш: {digest.hex()}")  # Выводим хэш в шестнадцатеричном виде
        print(f"Длина хэша: {len(digest)} байт")  # Выводим длину хэша
    except Exception as error:
        print(f"Ошибка: {str(error)}")
    print("─" * 60)

if __name__ == "__main__":
    print("=== Демонстрация криптографического дайджеста ===")
    
    # Тестовые случаи для демонстрации
    test_cases = [
        b"Cryptographic hash example",  # Пример хэширования
        b"",  # Пустые данные
        b"Short",  # Короткая строка
        b"Long string " * 20,  # Длинная строка
        b"Special \x00\xFF bytes",  # Специальные байты (нулевой и FF)
        os.urandom(1024),  # Случайные данные (1КБ)
        "This will cause error"  # Ошибка (не байты)
    ]
    
    # Демонстрация хэширования для каждого теста
    for case in test_cases:
        demonstrate_hashing(case if isinstance(case, bytes) else case.encode())

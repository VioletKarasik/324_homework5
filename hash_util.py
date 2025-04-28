# Константы для хеширования (первые 32 цифры числа π и e)
HASH_CONST_1 = 31415926535897932384626433832795
HASH_CONST_2 = 27182818284590452353602874713527
HASH_SIZE = 32  # Размер хеша в байтах

def byte_hash(data: bytes) -> bytes:
    """Хеш-функция, возвращающая 32-байтовый хеш для входных данных"""
    if not isinstance(data, bytes):
        raise TypeError("Входные данные должны быть в формате bytes")
    
    # Инициализация состояния (32 байта)
    state = bytearray([(i * HASH_CONST_1 + HASH_CONST_2) % 256 for i in range(HASH_SIZE)])
    
    # Обработка входных данных
    length = len(data)
    for i, byte in enumerate(data):
        # Основное смешивание
        pos = i % HASH_SIZE
        state[pos] = (state[pos] * HASH_CONST_1 + byte + i) % 256
        
        # Дополнительное смешивание
        other_pos = (i + byte) % HASH_SIZE
        state[other_pos] ^= (state[pos] + length) % 256
    
    # Финальное перемешивание
    for _ in range(4):
        new_state = bytearray(HASH_SIZE)
        for i in range(HASH_SIZE):
            # Смешиваем с соседями
            new_state[i] = (state[i] + state[(i-1)%HASH_SIZE] + state[(i+1)%HASH_SIZE]) % 256
        state = new_state
    
    return bytes(state)
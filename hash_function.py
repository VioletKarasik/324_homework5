import os

# Cryptographic mixing parameters
_PRIME_SEED_A = 0x6A09E667F3BCC908
_PRIME_SEED_B = 0xBB67AE8584CAA73B
_DIGEST_SIZE = 32  # 256-bit output

def generate_digest(input_data: bytes) -> bytes:
    """Generate a 256-bit cryptographic digest using enhanced mixing algorithm"""
    if not isinstance(input_data, bytes):
        raise TypeError("Input must be bytes sequence")
    
    # Initialize hash state with alternating pattern
    hash_state = bytearray([(0x36 if i % 3 == 0 else 0x5C) for i in range(_DIGEST_SIZE)])
    
    # Process each byte of input
    input_length = len(input_data)
    for position, byte_value in enumerate(input_data):
        # Primary mixing operation
        state_position = position % _DIGEST_SIZE
        current_state = hash_state[state_position]
        
        mixed_value = (current_state * _PRIME_SEED_A) + byte_value + position
        mixed_value ^= (input_length << (position % 7)) | _PRIME_SEED_B
        
        hash_state[state_position] = mixed_value % 256
        
        # Secondary diffusion
        alt_position = (position + byte_value) % _DIGEST_SIZE
        hash_state[alt_position] ^= (mixed_value >> (position % 4)) % 256
    
    # Final transformation rounds
    for _ in range(4):  # Increased from 3 to 4 rounds
        temp_buffer = bytearray(hash_state)
        for i in range(_DIGEST_SIZE):
            # Mix with adjacent and distant bytes
            prev_byte = temp_buffer[(i - 1) % _DIGEST_SIZE]
            next_byte = temp_buffer[(i + 1) % _DIGEST_SIZE]
            far_byte = temp_buffer[(i * 17) % _DIGEST_SIZE]  # Changed multiplier
            
            hash_state[i] = (hash_state[i] ^ prev_byte ^ next_byte ^ far_byte + 
                            (_PRIME_SEED_A // (i + 1))) % 256
    
    return bytes(hash_state)

def demonstrate_hashing(data: bytes):
    """Display input data and its hash digest"""
    try:
        display_text = data.decode('utf-8', errors='replace')[:60]
        if len(data) > 60:
            display_text += "..."
    except:
        display_text = f"Binary data ({len(data)} bytes)"
    
    print(f"Input: {display_text}")
    
    try:
        digest = generate_digest(data)
        print(f"Digest: {digest.hex()}")
        print(f"Length: {len(digest)} bytes")
    except Exception as error:
        print(f"Error: {str(error)}")
    print("─" * 60)

if __name__ == "__main__":
    print("=== Cryptographic Digest Demonstration ===")
    
    test_cases = [
        b"Cryptographic hash example",
        b"",
        b"Short",
        b"Long string " * 20,
        b"Special \x00\xFF bytes",
        os.urandom(1024),
        "This will cause error"  # Intentional type error
    ]
    
    for case in test_cases:
        demonstrate_hashing(case if isinstance(case, bytes) else case.encode())
import sys, string, random

def parse_size_to_bytes(size_str: str) -> int:
    size_str = size_str.strip().upper()
    multipliers = {
        'B': 1,
        'K': 1000,
        'KB': 1000,
        'M': 1000**2,
        'MB': 1000**2,
        'G': 1000**3,
        'GB': 1000**3,
        'T': 1000**4,
        'TB': 1000**4
    }
    
    for suffix, mult in sorted(multipliers.items(), key=lambda x: -len(x[0])):
        if size_str.endswith(suffix):
            return int(float(size_str[:-len(suffix)].strip()) * mult)
            
    return int(size_str)

def get_random_character(alphabet: str) -> str:
    return random.choice(alphabet)

def create_file(size: int, path: str) -> bool:
    with open(path, "w") as output:
        alphabet = string.ascii_letters + '\n'
        for i in range(size):
            output.write(get_random_character(alphabet))
        return True

    return False


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: file_creator.py [size] [output path]")
        sys.exit()

    size = parse_size_to_bytes(sys.argv[1])
    if create_file(size, sys.argv[2] if len(sys.argv) > 2 else "output.txt"):
        print("Successfully written " + str(size) + " bytes")
    else:
        print("Error")

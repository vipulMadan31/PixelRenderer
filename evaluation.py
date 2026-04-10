import numpy as np
import struct
import re

# =========================
# 1. Parse memory file
# =========================
def parse_memory(file_path):
    floats = []
    pattern = re.compile(r'0x([0-9A-Fa-f]+)')
    
    with open(file_path, 'r') as f:
        for line in f:
            match = pattern.search(line)
            if match:
                hex_val = int(match.group(1), 16)
                fval = struct.unpack('!f', struct.pack('!I', hex_val))[0]
                floats.append(fval)
    
    return np.array(floats, dtype=np.float32)

# =========================
# 2. Expected image (gradient)
# =========================
def generate_expected(w, h):
    img = np.zeros((h, w, 4), dtype=np.float32)
    
    for y in range(h):
        for x in range(w):
            u = x / w
            v = y / h
            img[y, x] = [u, v, 0.0, 1.0]
    
    return img.reshape(-1)

# =========================
# 3. Downsample
# =========================
def downsample(img, w, h):
    H, W, C = img.shape
    img = img[:h*(H//h), :w*(W//w)]  # trim
    
    img = img.reshape(h, H//h, w, W//w, C)
    return img.mean(axis=(1,3))

# =========================
# 4. Correlation
# =========================
def correlation(a, b):
    if np.std(a) < 1e-6 or np.std(b) < 1e-6:
        return 0
    return np.corrcoef(a, b)[0,1]

# =========================
# 5. Sliding window search
# =========================
def find_best_match(memory, expected, window_size, stride=1024):
    best_corr = -1
    best_idx = -1
    
    for i in range(0, len(memory) - window_size, stride):
        window = memory[i:i+window_size]
        
        # filter garbage values
        window = np.clip(window, -2, 2)
        
        corr = correlation(window, expected)
        
        if corr > best_corr:
            best_corr = corr
            best_idx = i
    
    return best_idx, best_corr

# =========================
# MAIN
# =========================
if __name__ == "__main__":
    
    memory = parse_memory("memory_snapshot_15s.txt")
    
    # expected small image
    W, H = 64, 128
    expected_img = generate_expected(W, H)
    
    window_size = W * H * 4
    
    idx, corr = find_best_match(memory, expected_img, window_size)
    
    print("Best match index:", idx)
    print("Correlation:", corr)
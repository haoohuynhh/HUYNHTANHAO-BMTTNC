from flask import Flask, request, jsonify

app = Flask(__name__)

# Định nghĩa lớp TranspositionCipher
class TranspositionCipher:
    def __init__(self):
        pass

    def encrypt(self, text, key):
        if not isinstance(text, str):
            raise ValueError("Văn bản phải là một chuỗi ký tự")
        if not isinstance(key, int) or key <= 0:
            raise ValueError("Khóa phải là một số nguyên dương")
        encrypted_text = ''
        for col in range(key):
            pointer = col
            while pointer < len(text):
                encrypted_text += text[pointer]
                pointer += key
        return encrypted_text

    def decrypt(self, text, key):
        if not isinstance(text, str):
            raise ValueError("Văn bản phải là một chuỗi ký tự")
        if not isinstance(key, int) or key <= 0:
            raise ValueError("Khóa phải là một số nguyên dương")
        
        # Tính số hàng và số ký tự bổ sung (nếu có)
        num_rows = (len(text) + key - 1) // key  # Làm tròn lên
        decrypted_text = [''] * len(text)
        
        # Điền các ký tự vào vị trí gốc
        pos = 0
        for col in range(key):
            for row in range(num_rows):
                index = row * key + col
                if index < len(text):
                    decrypted_text[index] = text[pos]
                    pos += 1
        
        return ''.join(decrypted_text)

# Khởi tạo đối tượng cipher
transposition_cipher = TranspositionCipher()
TRANSPOSITION_CIPHER_ALGORITHM = "TranspositionCipher"

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Không có dữ liệu JSON được gửi'}), 400
    
    plain_text = data.get('plain_text')
    key = data.get('key')

    if plain_text is None or key is None:
        return jsonify({'error': 'Thiếu trường plain_text hoặc key'}), 400

    try:
        key = int(key)
        if key <= 0:
            return jsonify({'error': 'Khóa phải là một số nguyên dương'}), 400
        encrypted_text = transposition_cipher.encrypt(plain_text, key)
        return jsonify({'encrypted_text': encrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/transposition/decrypt', methods=['POST'])
def transposition_decrypt():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Không có dữ liệu JSON được gửi'}), 400
    
    cipher_text = data.get('cipher_text')
    key = data.get('key')

    if cipher_text is None or key is None:
        return jsonify({'error': 'Thiếu trường cipher_text hoặc key'}), 400

    try:
        key = int(key)
        if key <= 0:
            return jsonify({'error': 'Khóa phải là một số nguyên dương'}), 400
        decrypted_text = transposition_cipher.decrypt(cipher_text, key)
        return jsonify({'decrypted_text': decrypted_text})
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
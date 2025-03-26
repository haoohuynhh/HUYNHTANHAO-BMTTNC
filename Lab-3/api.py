from flask import Flask, request, jsonify
import rsa
import os

app = Flask(__name__)

KEY_FOLDER = "keys"
PUBLIC_KEY_PATH = os.path.join(KEY_FOLDER, "publicKey.pem")
PRIVATE_KEY_PATH = os.path.join(KEY_FOLDER, "privateKey.pem")

def generate_and_save_keys():
    if not os.path.exists(KEY_FOLDER):
        os.makedirs(KEY_FOLDER)

    if not os.path.exists(PUBLIC_KEY_PATH) or not os.path.exists(PRIVATE_KEY_PATH):
        public_key, private_key = rsa.newkeys(512)

        with open(PUBLIC_KEY_PATH, "wb") as pub_file:
            pub_file.write(public_key.save_pkcs1())

        with open(PRIVATE_KEY_PATH, "wb") as priv_file:
            priv_file.write(private_key.save_pkcs1())

        return public_key, private_key
    else:
        with open(PUBLIC_KEY_PATH, "rb") as pub_file:
            public_key = rsa.PublicKey.load_pkcs1(pub_file.read())

        with open(PRIVATE_KEY_PATH, "rb") as priv_file:
            private_key = rsa.PrivateKey.load_pkcs1(priv_file.read())

        return public_key, private_key

# Load hoặc tạo khóa
public_key, private_key = generate_and_save_keys()

@app.route("/api/rsa/generate_keys", methods=["GET"])
def generate_keys():
    """ API tạo khóa RSA """
    return jsonify({
        "message": "Keys generated successfully"
    })

@app.route("/api/rsa/encrypt", methods=["POST"])
def encrypt():
    """ API mã hóa chuỗi bằng khóa công khai """
    data = request.json
    message = data.get("message", "").encode()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    encrypted_msg = rsa.encrypt(message, public_key)
    return jsonify({"encrypted_message": encrypted_msg.hex()})

@app.route("/api/rsa/decrypt", methods=["POST"])
def decrypt():
    """ API giải mã chuỗi bằng khóa riêng """
    data = request.json
    if not data or "cipher_text" not in data:
        return jsonify({"error": "Encrypted message is required"}), 400

    try:
        encrypted_bytes = bytes.fromhex(data["cipher_text"])
        decrypted_msg = rsa.decrypt(encrypted_bytes, private_key).decode()
        return jsonify({"decrypted_message": decrypted_msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/rsa/sign", methods=["POST"])
def sign():
    """ API ký số một thông điệp """
    data = request.json
    message = data.get("message", "").encode()

    if not message:
        return jsonify({"error": "Message is required"}), 400

    signature = rsa.sign(message, private_key, 'SHA-256')
    return jsonify({"signature": signature.hex()})

@app.route("/api/rsa/verify", methods=["POST"])
def verify():
    """ API xác minh chữ ký của thông điệp """
    data = request.json
    message = data.get("message", "").encode()
    signature = data.get("signature", "")

    if not message or not signature:
        return jsonify({"error": "Message and signature are required"}), 400

    try:
        rsa.verify(message, bytes.fromhex(signature), public_key)
        return jsonify({"verified": True})
    except rsa.VerificationError:
        return jsonify({"verified": False}), 400

if __name__ == "__main__":
    app.run(debug=True)
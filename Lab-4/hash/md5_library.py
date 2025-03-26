import hashlib

def calculate_md5(input_string):
    md5_hash = hashlib.md5(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

input_string = input("Nhập chuỗi cần băm: ")
md5_hash = calculate_md5(input_string)

print("Mã băm MD5 của chuỗi '{0}' là: {1}".format(input_string, md5_hash))
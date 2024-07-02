# Generate an RSA private key, of size 248
# Приватный ключ для кодировки jwt
openssl genrsa -out jwt-private.pem 2048

# Extract the public key from the key pair, which can be used in a certificate
# Публичный ключ на основе приватного для раскодировки созданного нами jwt
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem
import time
import jwt


private_key = """-----BEGIN PRIVATE KEY-----
MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAMvHDDB4qU7MZwFP
ti9qgYOeqiQiYs44Kr8Bxskigh0+Bsaa8u/Gei78XlIENe6h+wVQ4rTIh4ZKHbVD
lnELJo8g/+VLdvHUjwwlcw9PTGteUDAyKevq7Pctg2vkGMtSkpM+UrtoafNYAgLn
i2UWw+ZPJY+wER02NOgYgI0cQTjXAgMBAAECgYBteVnLEIeklZsg0ToG7yj1FOBC
2VZLg1EznDi3BZrxKslpGQU6W154r4vcc/alZM/+Yx3oEXL9agPbxZukz2C+vVF+
mop9Y6XUXwZ3R7WasEynZtvEVLKrP9Qh+oWjnkmX3wKyBBrIiDjljcVcabljOd+W
nkcblyzC6yj/q7ybQQJBAPxkxVGvWn9fKUlVD/g9N1IFCv0RhqOC21q/iKQIDQ9v
xz6AVo5bBMG3N0Gu9s4TlKcoOdcRtFS4c9oKEp/yeYsCQQDOsHG7PY68ww12TS85
4aPOHbfESIk5SWsWxM4lE/S82EvZeFdsbw0Lqn+/YDmW/+pw//MI4xFoYGbOwChR
LG9lAkEAwGCK6h0vbIB7NrMIbh0y6mh/nK9cIYufaMcu/mBInCiGBMTLtMv5jzH4
gy86XY8dMl/93klXW3AQlfQxiArIywJAHFYycYJCBH0VZme0ltHpnEOUwzNSpOj8
5pU60fiHcDCTTZBjI/mhpzzL4Nf3bU1OvglJL6m55D57OdM8c8yMxQJBANScXKUh
96GIRACTNKA8fOvOGe1bqVXlrT185MkkGHH6iH94zVvLCYfkYawU4uk2aRobusL1
/Z8KSns5Oll63pY=
-----END PRIVATE KEY-----"""

public_key = """-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDLxwwweKlOzGcBT7YvaoGDnqok
ImLOOCq/AcbJIoIdPgbGmvLvxnou/F5SBDXuofsFUOK0yIeGSh21Q5ZxCyaPIP/l
S3bx1I8MJXMPT0xrXlAwMinr6uz3LYNr5BjLUpKTPlK7aGnzWAIC54tlFsPmTyWP
sBEdNjToGICNHEE41wIDAQAB
-----END PUBLIC KEY-----"""


def jwt_encode(data):
    return jwt.encode(data, private_key, algorithm='RS256')


def jwt_decode(data):
    return jwt.decode(data, public_key, algorithms='RS256')


if __name__ == "__main__":
    a = jwt.encode({'some': 'passyload'}, private_key, algorithm='RS256')
    print(jwt.decode(a, public_key, algorithms='RS256'))

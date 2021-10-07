import rsa

# generater
class generater():
    def __init__(self):
        pass
    def generater_key(self):
        (pubkey, privkey) = rsa.newkeys(1024)
        pub = pubkey.save_pkcs1()
        pubfile = open('../key/public.pem', 'wb')
        pubfile.write(pub)
        pubfile.close()

        pri = privkey.save_pkcs1()
        prifile = open('../key/private.pem', 'wb')
        prifile.write(pri)
        prifile.close()
    def get_key(self):
        # key
        with open('./key/public.pem', "rb") as publickfile:
            with open('./key/private.pem', "rb") as privatefile:
                pub = publickfile.read()
                pubkey = rsa.PublicKey.load_pkcs1(pub)
                pri = privatefile.read()
                privkey = rsa.PrivateKey.load_pkcs1(pri)
                return pubkey, privkey
import hashlib


# class represents a user of the application, providing functionality for password hashing
class User:

    # this static method salts and hashes the user password
    @staticmethod
    def hash_pw(password):
        # combine password and salt to encode to bytes
        salted_password = (password + 'monty').encode()

        # create instance of SHA256 hash algorithm from hashlib library
        sha256 = hashlib.sha256()

        # pass the salted password through the hashing algorithm
        sha256.update(salted_password)

        # get the hexadecimal representation of the sha256 hash
        pw_hash = sha256.hexdigest()

        # return the hash
        return pw_hash

#!/usr/bin/env python
# -*- coding: utf8 -*-

""" 
 generate.py
 CSR Generator for csrgenerator.com

 Copyright (c) 2013 David Wittman <david@wittman.com>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation, either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.

"""

import OpenSSL.crypto as crypt

class CsrGenerator:
    def __init__(self, key_bit_length, form_values):
        self.csr_info = self._validate(form_values)
        self.keypair = self.generate_rsa_keypair(crypt.TYPE_RSA, key_bit_length)

    def _validate(self, form_values):
        valid = {}
        fields = ('C', 'ST', 'L', 'O', 'OU', 'CN')
        optional = ('OU',)

        for field in fields:
            try:
                valid[field] = form_values[field]
            except KeyError:
                if field not in optional:
                    raise

        return valid

    def generate_rsa_keypair(self, key_type, key_bit_length):
        "Generates a public/private key pair of the type key_type and size key_bit_length"
        key = crypt.PKey()
        key.generate_key(key_type, key_bit_length)
        return key

    @property
    def private_key(self):
        return crypt.dump_privatekey(crypt.FILETYPE_PEM, self.keypair)

    @property
    def csr(self):
        digest = "md5"
        request = crypt.X509Req()
        subject = request.get_subject()

        for (k,v) in self.csr_info.items():
            setattr(subject, k, v)

        request.set_pubkey(self.keypair)
        request.sign(self.keypair, digest)
        return crypt.dump_certificate_request(crypt.FILETYPE_PEM, request)

def cgi_field_storage_to_dict(field_storage):
    "Transforms a FieldStorage object into a dictionary"
    return dict((key, field_storage[key].value) for key in field_storage.keys())

def main():
    pass

if __name__ == '__main__':
    main()

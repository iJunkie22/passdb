import hashlib
import sqlite3
import pickle

__author__ = 'ethan'


class HashMangler(object):
    def __init__(self, seed):
        assert isinstance(seed, unicode) or isinstance(seed, str)
        hash_str = hashlib.sha256(seed).hexdigest()
        self._hash_chars = [int(''.join(('0x', hash_str[x - 1], hash_str[x])), 16) for x in range(1, len(hash_str), 2)]
        self._hash_len = len(self._hash_chars)

    def talk(self, res_len):
        assert isinstance(res_len, int)
        return [self._hash_chars[x % self._hash_len] for x in range(0, res_len)]

    def mangle(self, input_str):
        assert isinstance(input_str, unicode) or isinstance(input_str, str)
        offsets = self.talk(len(input_str))
        input_ords = map(ord, input_str)
        return u''.join([unichr(y + z) for y, z in zip(input_ords, offsets)])

    def demangle(self, mangled_str):
        assert isinstance(mangled_str, unicode) or isinstance(mangled_str, str)
        offsets = self.talk(len(mangled_str))
        mangled_ords = map(ord, mangled_str)
        return u''.join([unichr(y - z) for y, z in zip(mangled_ords, offsets)])


def writedb(passkey, db_conn, url, uname_str, pass_str):
    assert isinstance(db_conn, sqlite3.Connection)
    cur = db_conn.cursor()
    mangler = HashMangler(passkey)
    try:
        cur.execute('''CREATE TABLE IF NOT EXISTS wallet (location TEXT, uname TEXT, password TEXT);''')
        db_conn.commit()
        cur.execute('''INSERT INTO wallet (location, uname, password) VALUES (?, ?, ?);''',
                    (url, mangler.mangle(uname_str), mangler.mangle(pass_str)))
        db_conn.commit()
    finally:
        pass


def read_db(passkey, db_conn):
    mangler = HashMangler(passkey)
    assert isinstance(db_conn, sqlite3.Connection)
    cur = db_conn.cursor()
    cur.row_factory = sqlite3.Row

    try:
        cur.execute('SELECT * FROM wallet;')
        for row in cur:
            print "=" * 20
            print row[0]
            print mangler.demangle(row[1])
            print mangler.demangle(row[2])
    finally:
        pass


def save_seed(new_seed_str):
    pickle.dump(new_seed_str, open('seed.p', 'wb'))


def main():
    # TODO: run save_seed with a passkey if you like

    seed_str = pickle.load(open('seed.p', 'rb'))

    conn = sqlite3.connect('passes.db')
    c = conn.cursor()
    c.row_factory = sqlite3.Row

    test1 = HashMangler(seed_str)

    s1a = test1.mangle('banana')
    s2a = test1.mangle('The quick brown fox jumped.')
    s1b = test1.demangle(s1a)
    s2b = test1.demangle(s2a)

    print s1a
    print s1b

    print s2a
    print s2b

    read_db(seed_str, conn)

if __name__ == '__main__':
    main()

import passdb
import plistlib
import binascii
import uuid
import os.path
import pickle


class PassPlist(object):
    def __init__(self):
        self.mangler = None
        self.root = {}
        self.seed_str = None

    @property
    def has_mangler(self):
        return self.mangler is not None

    def load_plist(self, fp):
        self.root = plistlib.readPlist(fp)

    def init_mangler(self, seed_str):
        self.mangler = passdb.HashMangler(seed_str)

    def demangle_entry(self, m_k1, m_v1):
        assert self.has_mangler, "You need to call init_mangler first!"

        dm_k2 = self.mangler.demangle(pickle.loads(binascii.unhexlify(m_k1)))
        dm_v2 = self.mangler.demangle(pickle.loads(binascii.unhexlify(m_v1)))
        return dm_k2, dm_v2

    def add_as_mangled(self, k_in, v_in):
        k, v = self.mangle_entry(k_in, v_in)
        self.root[k] = v

    def get_as_demangled(self, k_in):
        return self.demangled_root.get(k_in)

    def mangle_entry(self, r_k1, r_v1):
        assert self.has_mangler, "You need to call init_mangler first!"
        m_k2 = binascii.hexlify(pickle.dumps(self.mangler.mangle(r_k1)))
        m_v2 = binascii.hexlify(pickle.dumps(self.mangler.mangle(r_v1)))
        return m_k2, m_v2

    @property
    def demangled_root(self):
        return dict([self.demangle_entry(k, v) for k, v in self.root.iteritems()])


def load_from_standard_path():
    ppl = PassPlist()
    ppl.init_mangler(uuid.UUID(int=uuid.getnode()).hex[-12:])
    if os.path.exists(os.path.expanduser('~/.pypassplist.plist')):
        ppl.load_plist(os.path.expanduser('~/.pypassplist.plist'))
    return ppl


def write_to_standard_path(pass_pl1):
    plistlib.writePlist(pass_pl1.root, os.path.expanduser('~/.pypassplist.plist'))


def run_sample():
    ppl1 = load_from_standard_path()
    ppl1.add_as_mangled('foo', 'bar')
    write_to_standard_path(ppl1)
    print ppl1.demangled_root

if __name__ == '__main__':
    run_sample()

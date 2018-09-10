import _io

def preprocess(file: _io.TextIOWrapper):
    txt = map(lambda x: x.strip(), file.readlines())
    return ''.join(txt)

if __name__ == '__main__':
    import sys
    with open(sys.argv[1], newline=None) as f:
        print(preprocess(f))

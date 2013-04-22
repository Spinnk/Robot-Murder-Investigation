import os

if __name__=='__main__':
    CWD = os.path.split(os.path.abspath(__file__))[0]
    f = open(os.path.join(CWD, 'map.csv'), 'r')
    data = f.read()
    f.close()
    while '\n' in data:
        data = data.replace('\n', ',')
    while '\r' in data:
        data = data.replace('\r', ',')
    data = data.split(',')
    while '' in data:
        data.remove('')
    data = [chr(int(x)) for x in data]
    f = open(os.path.join(CWD, "map.txt"), 'wb')
    f.write(''.join(data))
    f.close()

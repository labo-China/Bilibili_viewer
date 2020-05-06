class tool:
    def __init__(self):
        # av2bv bv2av
        self.alphabet = 'fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'

    def bv2av(self,x):
        r = 0
        for i, v in enumerate([11, 10, 3, 8, 4, 6]):
            r += self.alphabet.find(x[v]) * 58 ** i
        return (r - 0x2_0840_07c0) ^ 0x0a93_b324

    def av2bv(self,x):
        x = (x ^ 0x0a93_b324) + 0x2_0840_07c0
        r = list('BV1**4*1*7**')
        for v in [11, 10, 3, 8, 4, 6]:
            x, d = divmod(x, 58)
            r[v] = self.alphabet[d]
        return ''.join(r)
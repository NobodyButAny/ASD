def z_func(s: str) -> list[int]:
    z = [0 for i in s]
    n = len(s)
    l = 0
    r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            r = i + z[i] - 1
            l = i
    return z


def prefix_func(s: str) -> list[int]:
    p = [0 for i in s]
    n = len(s)
    for i in range(1, n):
        cur = p[i - 1]
        while s[i] != s[cur] and cur > 0:
            cur = p[cur - 1]
        if s[i] == s[cur]:
            p[i] = cur + 1
    return p


def knuth_morris_pratt(s: str, substr: str) -> list[int]:
    z_out = z_func(substr + '#' + s)
    res = []
    n = len(substr)
    for i, val in enumerate(z_out):
        if val == n:
            res.append(i - n - 1)
    return res


if __name__ == '__main__':
    test = 'abacabadava'
    print(*z_func(test), sep='')
    print(*prefix_func(test), sep='')

    phrase = 'вкусные булочки с маком смаковали видные мужи, светя макушками.'
    keyword = 'мак'
    res = knuth_morris_pratt(phrase, keyword)
    print(res)
    for i, char in enumerate(phrase):
        if i in res:
            print(char.upper(), end='')
        else:
            print(char, end='')
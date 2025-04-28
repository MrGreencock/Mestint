import random

def ea(a,b,d=0):
    d = a
    while b!=0:
        d = b
        b = a % b
        a = d

    return d


def getPublicExponent(phi_n):
    while True:
        e = random.randint(1, phi_n)
        gcd = ea(e, phi_n)
        if gcd == 1:
            break

    return e


def eea(a,b,d=0,x=0,y=0):
    x0 = 1
    x1 = 0
    y0 = 0
    y1 = 1
    s = 1
    while b != 0:
        r = a % b
        q = a // b
        a, b = b, r
        x, y = x1, y1
        x1 = q * x1 + x0
        y1 = q * y1 + y0
        x0 = x
        y0 = y
        s = -s

    x = s * x0
    y = -s*y0
    d,x,y = a,x,y
    return d, x, y

def getSecretExponent(e, phi_n):
    d, x, _ = eea(e, phi_n)
    if d != 1:
        raise ValueError("Nincs inverz")
    return x % phi_n

def fe(base, exp, mod):
    base = base % mod
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    elif exp % 2 == 0:
        return fe(base * (base%mod), exp//2, mod)

    return base * fe(base, exp - 1, mod)


def powerMod(b, e, m):
    x = 1
    while e > 0:
        if e % 2 == 1:
            x = (b * x) % m

        b = (b * b) % m
        e = e // 2
    return x


def mrprime(n, a):
    for i in a:
        d = n - 1
        s = 0
        while d % 2 == 0:
            d = d // 2
            s += 1
        t = powerMod(i, d, n)
        if t == 1:
            return True
        while s > 0:
            if t == n - 1:
                return True
            t = (t * t) % n
            s = s - 1

    return False

def crt(c,d,p,q):
    c1 = pow(c, d%(p-1)) % p
    c2 = pow(c, d%(q-1)) % q
    M = p * q
    m1 = M // p
    m2 = M // q
    gcd, y1, y2 = eea(m1, m2)
    m = c1 * m1 * y1 + c2 * m2 * y2
    if m < 0:
        m = m + M
    return m

def generatePrime(n, a):
    while True:
        n = random.randint(2, n)
        if mrprime(n,a):
            break

    return n

def encryption_rsa(m, e, n):
    return fe(m, e, n)

def decryption_rsa(c, d, p, q):
    return crt(c,d,p,q) % (p*q)


def signature(m, d, p, q):
    return crt(m,d,p,q) % (p*q)

def verification(c,e,n):
    return fe(c,e,n) % n


def main():
    while True:
        p = generatePrime(1000, [2, 3])
        q = generatePrime(1000, [2, 3])
        if p != q and p > 10 and q > 10:
            break

    
    n = p * q
    phi_n = (p-1) * (q-1)
    e = getPublicExponent(phi_n)
    d = getSecretExponent(e, phi_n)
    pk = (n, e)
    sk = (n, d)
    print(f"{pk}, {sk}")
    m = 23
    c = encryption_rsa(m,e,n)
    s = signature(m,d,p,q)
    print(f"Encrypted message: {c}")
    print(f"Original message: {decryption_rsa(c,d,p,q)}")
    print(f"Signatured message: {s}")
    print(f"Verified message: {verification(s,e,n)}")



if __name__ == "__main__":
    main()

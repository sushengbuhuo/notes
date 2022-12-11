# RSA加密算法拉胯解说版
# Pyhton3.8.5
"""
RSA 加密解密核心算法
1、n = p * q
1.1、p和q是什么，当然是质数。质数就是除了1和本身不被任何数整除的数。N是两个质数的乘积
2、&#248;(n) = (p - 1) * (q - 1)
2.1、&#248;(n)是什么，当然是n的欧拉函数。是小于n并且与n互质的正整数的个数。
2.2、比如说&#248;(10) 那么与10互质的有1,3,7,9即&#248;(10)=4。
2.3、质数n的欧拉数是n-1。已知n为两个质数的乘积。所以用公式
3、取一个随机数e，随机选择一个整数e，条件是1< e < φ(n)，且e与φ(n) 互质
4、计算出d来。ed ≡ 1 mod &#248;(n)
4.1、上面的ed是乘积算作整体，ed 除&#248;(n)的余数等于1，即：e * d % &#248;(n) ==1
4.2 e * d % &#248;(n) ==1，也是 ( e * d -1 ) % &#248;(n) ==0，
5、加密用：c = m**e mod n
6、解密用：m = c**d mod n
私钥：nd
公钥：ne
"""
 
 
def gcd(x, y):  # 辗转相除法
    return y if (x == 0) else gcd(y % x, x)
 
 
def get_prime_number(a, b):  # 指定范围质数
    temp = []
    for v in range(a, a + b):
        x = 0
        for j in range(2, int(v ** 0.5) + 1):  # 结束点是i的平方根取整+1
            if gcd(x=v, y=j) != 1:
                x = 1
                break
        if x == 0:
            temp.append(v)
    return temp
 
 
def findModReverse(a, g):
    if gcd(a, g) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, g
    while v3 != 0:
        h = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - h * v1), (u2 - h * v2), (u3 - h * v3), v1, v2, v3
    return u1 % g
 
 
def get_e():
    # 随机选择一个整数e，条件是1< e < φ(n)，且e与φ(n) 互质。
    # 所以从1开始，从N-1结束
    for i in range(2, N):
        # 调用辗转相除，结果为1就是互质关系
        if gcd(x=N, y=i) == 1:
            if i >= 19:  # 当e大于或等于19就结束了
                return i
 
 
primeNumber = get_prime_number(a=200, b=100)  # 获取指定范围内的质数
 
 
# 1、获取两个质数，从质数列表里面取。并且两个质数不能相同
p = primeNumber[0]
q = primeNumber[-1]
if p == q:
    print('质数pq相同，需要调整范围')
 
# 2、计算n
n = p * q
 
# 3、计算&#248;(n)，用N表示，知道pq很简单。不知道pq你就慢慢猜去
N = (p - 1) * (q - 1)
 
# 4、随机选择一个整数e，条件是1< e < φ(n)，且e与φ(n) 互质。
e = get_e()  # 用函数
 
# 5、ed ≡ 1 mod &#248;(n)等价于e * d % &#248;(n) ==1
d = findModReverse(a=e, g=N)  # 用函数，网上扣得。不然就只能用枚举法。当n越大速度越慢
 
# 6、加密 c = m**e mod n
m = 10086  # 需要加密的数字。这里的m不能大于 n-2，会溢出
c = m ** e % n  # 密文用c
 
# 7、解密 m = c**d mod n
M = c ** d % n  # 解密用M是为了和小m区分
print(f'质数列表：\t{primeNumber}')
print(f"质数：\t\tp={p}")
print(f"质数：\t\tq={q}")
print(f"质数pq乘积：\tn={n}")
print(f"n的欧拉数：\tφ(n)={N}")
print(f"与n的欧拉数互质的数：e={e}")
print(f"ed除N余1的数：\td={d}")
print(f'需要加密的数：m={m}')
print(f'已经加密的数：c={c}')
print(f'经过解密的数：M={M}')
print('公钥(n,e)', (n, e))
print('私钥(n,d)', (n, d))
input('暂停一下')
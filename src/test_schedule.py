class MyProut:
    string = None


def whatiszeid(prout):
    print(id(prout))

aProut = MyProut()
aProut.string = 'prout'
print(id(aProut))

whatiszeid(aProut)
whatiszeid(prout=aProut)



noget = type('none', (), {})
disget = type('display', (), {})
intget = type('intvar', (), {})
strget = type('strvar', (), {})
doubleget = type('doublevar', (), {})
singleget = type('singleline', (), {})
multiget = type('multiline', (), {})
treeget = type('tree', (), {})


#class novar(base):SUITE

if __name__ == '__main__':
	x = intget
	print(type(x))
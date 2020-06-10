import random

def calc():
    width = 10
    scaling = 1 * 10
    newWidth = (width + scaling) - (scaling/2)
    return newWidth

def main():
    for i in range(20):
        print(calc())

main()

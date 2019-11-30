import sys
print("HELLO,USER")
def getKeyWord(string,key):
    key=list(key)
    if len(string)==len(key):
        return(''.join(key))
    else:
        for i in range(len(string) -
                       len(key)):
            key.append(key[i % len(key)])
        return("".join(key))
def cipher(string,key):
    ciphertext=[]
    for i in range(len(string)):
        if str.islower(string[i]):
            c=(((ord(string[i])-97)+ord(key[i]))%26)+97
        else:
            if str.isupper(string[i]):
                c=(((ord(string[i])-65)+ord(key[i]))%26)+65
            else:
                if (int(string[i])>=0 and int(string[i])<=9):
                    c=(((int(string[i])-0)+ord(key[i])%26))%10+0
                    c=str(c)
                else:
                    c=ord(string[i])
        try:
            ciphertext.append(chr(c))
        except:
            ciphertext.append(c)
    return(''.join(ciphertext))
def plain(string,key):
    plaintext=[]
    for i in range(len(string)):
        if str.islower(string[i]):
            p=(((ord(string[i])-97)-ord(key[i]))%26)+97

        else:
            if str.isupper(string[i]):
                p=(((ord(string[i])-65)-ord(key[i]))%26)+65
            else:
                if (int(string[i])>=0 and int(string[i])<=9):
                    p=(((int(string[i])-0)-ord(key[i])%26))%10+0
                    p=str(p)
                else:
                    p=ord(string[i])
        try:
            plaintext.append(chr(p))
        except:
            plaintext.append(p)
    return(''.join(plaintext))
if __name__ == "__main__":
    q=True
    while(q==True):
        choose=int(input("for ciphertext press:1 \nfor plaintext press:2\nyour choice: "))
        if(choose==1):
            plaintext=input('enter the plain text:')
            keyword=input('enter the keyword:')
            key=getKeyWord(plaintext,keyword)
            ciphertext=cipher(plaintext,key)
            print('ciphertext: '+ciphertext)
        elif(choose==2):
            ciphertext=input('enter the cipher text:')
            keyword=input('enter the keyword:')
            key=getKeyWord(ciphertext,keyword)
            plaintext=plain(ciphertext,key)
            print('plaintext: '+plaintext)
        else:
            print('wrong choice')

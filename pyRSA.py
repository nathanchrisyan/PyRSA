//Implementation of the RSA encryption algorithm

import random
import os
import string
import time
import threading

def ReadByWord(line){
    results1 = ""
    results2 = []
    for i in line{
        if i != " " and i != ""{
            results1 += i
        }
        else{
            if results1 == ""{
                pass
            }
            else{
                results2.append(results1.rstrip(''))
            }
            results1 = ""
        }
    }
    return results2
}

def MessageToInt(message){
    result = ""
    for i in message{
        result += str(format(ord(i), "x"))
    }
    return result
}

def IntToMessage(intMessage){
    resultLetter = ""
    result = ""
    
    for i in range(1, len(intMessage) + 1){
        resultLetter += intMessage[i - 1]
        
        if i % 2 == 0 and i != 0{
            print resultLetter
            result += resultLetter.decode('hex')    //Convert the hex to a character and add it to the result
            resultLetter = ""           
        }

        
    }
    
    return result
}

def SplitMessage(message){
    messages = []
    result = ""
    for i in range (len(message)){
        result += message[i]
        if i % 5 == 0 and i != 0{
            if (i + 5) > len(message){
                result += message[i + 1:]
            }
            messages.append(result)
            result = ""
        }
    }
    
    return messages    
}

//print SplitMessage("hello dank memes I am the best dankus in the world")

def egcd(a, b){
    if a == 0{
        return (b, 0, 1)
    }
    else{
        g, y, x = egcd(b % a, a)
        return (g, x - (b / a) * y, y)
    }
}

def ModularMultiplicativeInverse(n, mod){
    g, x,  y = egcd(n, mod)
    if g != 1{
        raise Exception("modular inverse does not exist")
    }
    else{
        return x % mod
    }
}

def EulerTotientFunc(n, p, q){      //Calculates the Euler totient function that will be used for the public key
    return n - (p + q - 1) 
}

def FindCoPrime(m){
    fp1 = open("primes1.txt")
    lines = fp1.readlines()
    
    line_num = random.randint(100, 1000)
    current_line = lines[line_num]
    running = True
    
    while True{
        for i in ReadByWord(current_line){
            if m % int(i) != 0{
                return int(i)    
            
            }
        }
        line_num += 1
        current_line = lines[line_num]
        
    }
}
 
def FindP(){
    primeFiles = [17, 32, 34, 37, 41, 46, 47]       //A list of all of the prime files that I have on hand
    
    file_to_open = primeFiles[random.randint(0, len(primeFiles) - 1)]
    fp = open("primes" + str(file_to_open) + ".txt").readlines()
    
    linenum = random.randint(5, 2000)    //~20,000 lines per file_to_open
    word = random.randint(0, 7)
    
    return int(ReadByWord(fp[linenum])[word])    
}

def FindQ(){
    primeFiles = [17, 32, 34, 37, 41, 46, 47]       //A list of all of the prime files that I have on hand
    
    file_to_open = primeFiles[random.randint(0, len(primeFiles) - 1)]
    fp = open("primes" + str(file_to_open) + ".txt").readlines()
    
    linenum = random.randint(5, 2000)    //~20,000 lines per file_to_open
    word = random.randint(0, 7)
    
    return int(ReadByWord(fp[linenum])[word])    
}
    
def GeneratePublicKey(p, q, totientFunc){
    Key = [0, 0]
    
    Key[0] = p * q
    Key[1] = FindCoPrime(totientFunc) 
    
    return Key
}

def GeneratePrivateKey(p, q, publicKey, totientFunc){
    Key = ModularMultiplicativeInverse(publicKey[1], totientFunc)
    
    return Key
} 

def Encrypt(message, publicKey){
    encryped = pow(message, publicKey[1], publicKey[0])
    return encryped
    
}

def Decrypt(encrypedMessage, privateKey, publicKey){
    decrypted = pow(encrypedMessage, privateKey, publicKey[0])
    return decrypted
}

def ScanForDrives(){     //Returns the next letter that will exist
    alphabet = list(string.ascii_lowercase)[2:]
    for alpha in range(len(alphabet)){
        if os.system(alphabet[alpha] + ": 2>NUL") == 1{
            return alphabet[alpha]
        }
        else{
            continue
        }
    }
}


def IsUSBPlugged(driveLetter){
    
    if os.system(driveLetter + ": 2>NUL") == 1{
        return False
    }
    else{
        return True
    }    
}

def ScanForOtherDrives(driveLetter){
    alphabet = list(string.ascii_lowercase)[2:]    
    
    availableDrives = []
    
    for alpha in range(alphabet.index(driveLetter) - 1, len(alphabet)){
        if os.system(alphabet[alpha] + ": 2>NUL") == 1{
            pass
        }
        else{
            availableDrives.append(alphabet[alpha])
        }        
    }
}

def PrintAvailableDrives(driveSelected, availableDrives){
    if driveSelected == 0{
    availableDrives = ScanForOtherDrives()
    print "Available USBs:"
        
    counter = 0
    for i in availableDrives{
    print str(counter) + " : " + i
 
    }
    }
    
}

//def power()

print "                                      Welcome to PyRSA!"
print "            Please remove all USB/Removable Drives from the computer and press 'enter'"
raw_input("")

defaultAvailableDrives = ScanForOtherDrives()

INPUT = 0
while INPUT != "4"{
    print "0 : Write public/private key onto different USB ( more secure )" 
    print "1 : Write public/private key onto same USB ( less secure )"
    print "2 : Encrypt a message"
    print "3 : Decrypt a message"
    print "4 : Quit application"
    
    INPUT = raw_input("")
    
    if INPUT == "0"{
        print "Please insert a USB and press 'enter'"
        raw_input("")
    
        print "Detecting USB..."
        availableDrives = ScanForOtherDrives() //Detects what letter the entered drive should be
        //os.system("cls")
    
        while defaultAvailableDrives == availableDrives{
            //os.system("cls")
            print "Detecting USB..."
            time.sleep(0.5)
        }
        
        PrintAvailableDrives()
        driveSelected = 0
        
        
        driveSelected = raw_input("")
        
        
        
        print "Finding P..."
        p = FindP()
        print "Found P..."
        print "-----------------------------------"

        print "Finding Q..."
        q = FindQ()
        print "Found Q..."
        print "-----------------------------------"

        print "Generating product"
        n = p * q 
        print "Generated product"
        print "-----------------------------------"

        print "Generating totient function"
        totient = int(EulerTotientFunc(n, p, q))
        print "Generated totient function"
        print "-----------------------------------"

        print "Finding coprime"
        coPrime = FindCoPrime (totient)
        print "Found coprime"
        print "-----------------------------------"
    
        print "Generating private key"
        PrivateKey = ModularMultiplicativeInverse(coPrime, totient)
        print "Generated private key"
        print "-----------------------------------"
    
        print "Writing to USB"
        f = open(driveLetter + ":/PRIVATEKEY.RSA", "w")
        f.write(str(PrivateKey) + "\n")
        f.write(str(p * q))         //This is for the decryption, when using the private key, this section of the public key is required
        print "Wrote to USB"
        f.close()
        os.system("cls")
        
        print "Please insert a USB"
        print "If a USB is already in the computer, please remove it and press enter"
        raw_input("")
    
        print "Detecting USB..."
        driveLetter = ScanForDrives() //Detects what letter the entered drive should be
        os.system("cls")
    
        while IsUSBPlugged(driveLetter) == False{
            os.system("cls")
            print "Detecting USB..."
            time.sleep(1)
               
        }
        print "USB Detected!"
        
        print "Generating public key"
        PublicKey = GeneratePublicKey(p, q, totient)
        print "Generated public key"
        print "-----------------------------------"
        
        print "Writing to USB"
        f = open(driveLetter + ":/PUBLICKEY.RSA", "w")
        f.write(str(PublicKey[0]) + "\n")
        f.write(str(PublicKey[1]))
        f.close()
        print "Wrote to USB"
                
        print "FINISHED"
    
    }
    elif INPUT == "1"{
        print "Please insert a USB"
        print "If you already have a USB in the computer, please remove it and press enter"
        raw_input("")
    
        print "Detecting USB..."
        driveLetter = ScanForDrives() //Detects what letter the entered drive should be
        os.system("cls")
    
        while IsUSBPlugged(driveLetter) == False{
            os.system("cls")
            print "Detecting USB..."
            time.sleep(1)
               
        }
        print "USB Detected!"
    
        print "Finding P..."
        p = FindP()
        print "Found P..."
        print "-----------------------------------"

        print "Finding Q..."
        q = FindQ()
        print p * q
        print "Found Q..."
        print "-----------------------------------"

        print "Generating product"
        n = p * q 
        print "Generated product"
        print "-----------------------------------"

        print "Generating totient function"
        totient = int(EulerTotientFunc(n, p, q))
        print "Generated totient function"
        print "-----------------------------------"

        print "Finding coprime"
        coPrime = FindCoPrime (totient)
        print "Found coprime"
        print "-----------------------------------"
    
        print "Generating private key"
        PrivateKey = ModularMultiplicativeInverse(coPrime, totient)
        print "Generated private key"
        print "-----------------------------------"
    
        print "Writing to USB"
        f = open(driveLetter + ":/PRIVATEKEY.RSA", "w")
        f.write(str(PrivateKey) + "\n")
        f.write(str(p * q) + "\n")
        print "Wrote to USB"
        f.close()
        os.system("cls")
        
        print "Generating public key"
        PublicKey = GeneratePublicKey(p, q, totient)
        print "Generated public key"
        print "-----------------------------------"
        
        print "Writing to USB"
        f = open(driveLetter + ":/PUBLICKEY.RSA", "w")
        f.write(str(PublicKey[0]) + "\n")
        f.write(str(PublicKey[1]))
        f.close()
        print "Wrote to USB"
                
        print "FINISHED"
            
    
    }
    elif INPUT == "2"{
        foundPUBLICKEYRSA = False
        while foundPUBLICKEYRSA == False{
            print "Please insert a USB with a PUBLICKEY.RSA file"
            print "If you already have a USB in the computer, please remove it and press enter"
            raw_input("")
    
            print "Detecting USB..."
            driveLetter = ScanForDrives() //Detects what letter the entered drive should be
            os.system("cls")
    
            while IsUSBPlugged(driveLetter) == False{
                os.system("cls")
                print "Detecting USB..."
                time.sleep(1)
               
            }
            
            for i in os.listdir(driveLetter + ":/"){
                if i == "PUBLICKEY.RSA"{ 
                    foundPUBLICKEYRSA = True
                }
                else{
                    pass
                }
            }
            if foundPUBLICKEYRSA == False{
                print "Could not locate PUBLICKEY.RSA"
                print "Please insert a USB with the PUBLICKEY.RSA file" 
            }
            elif foundPUBLICKEYRSA == True{
                print "Located PUBLICKEY.RSA!"
            }
        }
        
        message = raw_input("Message to be encryped: ")
        name = raw_input("Name of the file to store encrypted message ( if no name is given, ENCRYPEDMESSAGE will be the default): ")
        
        print "Initializing public key\n"
        f = open(driveLetter + ":/PUBLICKEY.RSA", "r")
        if name == ""{
            fw = open(driveLetter + ":/ENCRYPEDMESSAGE.ENCRYPTED", "w")
        }
        else{
            fw = open(driveLetter + ":/" + name + ".ENCRYPTED", "w")
        }
        f_lines = f.readlines()
        
        PublicKey = [None, None]
        PublicKey[0] = int(f_lines[0])
        PublicKey[1] = int(f_lines[1])
        print "Public key initialized"
        print "-----------------------------------"
        
        print "Splitting message into approximately " + str(len(message) / 5) + " sections"
        message = SplitMessage(message)
        print "Split message"
        print "-----------------------------------"

        print "Converting messages to hex"

        new_message = []
        for j in message{
            new_message.append(int(MessageToInt(j), 16))
    
        }       
        print "Converted messages to hex"
        message = new_message

        print "( messages = ",
        for i in message{
            print i,
        } 
        print ")\n"

        print "Encrypting message"

        encrypedMessages = []
        for i in message{
            encrypedMessages. append(Encrypt(i, PublicKey))

        }

        print "Finished encryption"
        print "-----------------------------------"
        
        print "Writing message to file"
        for i in encrypedMessages{
            //print str(i)
            fw.write(str(i) + "\n")
        }
        fw.close()
        f.close()
        print "Finished writing message to directory: " + driveLetter + ":/\n"

    }
    elif INPUT == "3"{
        foundPRIVATEKEYRSA = False
        while foundPRIVATEKEYRSA == False{
            print "Please insert a USB with a PRIVATEKEY.RSA file"
            print "If you already have a USB in the computer, please remove it and press enter"
            raw_input("")
    
            print "Detecting USB..."
            driveLetter = ScanForDrives() //Detects what letter the entered drive should be
            os.system("cls")
    
            while IsUSBPlugged(driveLetter) == False{
                os.system("cls")
                print "Detecting USB..."
                time.sleep(1)
               
            }
            
            for i in os.listdir(driveLetter + ":/"){
                if i == "PRIVATEKEY.RSA"{ 
                    foundPRIVATEKEYRSA = True
                }
                else{
                    pass
                }
            }
            if foundPRIVATEKEYRSA == False{
                print "Could not locate PRIVATEKEY.RSA"
                print "Please insert a USB with the PRIVATEKEY.RSA file" 
            }
            elif foundPRIVATEKEYRSA == True{
                print "Located PRIVATEKEY.RSA!"
            }
        
        }
        print "Here are some of the possible messages to decrypt"
        print "Which one would you like to decrypt? ( Type in a number )"
        possibleEncryptedMessagesToDecrypt = []
        counter = 0 
        for i in os.listdir(driveLetter + ":/"){
            //print i.rpartition(".")[2]
            if i.rpartition(".")[2] == "ENCRYPTED"{ 
                possibleEncryptedMessagesToDecrypt.append(i)
                print str(counter) + " : " + i
                counter += 1
            }
            else{
                pass
            }
        
        }
        
        f = open(driveLetter + ":/PRIVATEKEY.RSA", "r")
        f_lines = f.readlines()
        
        toDecrypt = int(raw_input("\n")) 
        PrivateKey = [None, None]
        
        print "Initializing the private key"
        PrivateKey[0] = f_lines[0]
        PrivateKey[1] = f_lines[1]
        
        encryptedMessages = []
        decryptedMessages = []
        
        fr = open(driveLetter + ":/" + possibleEncryptedMessagesToDecrypt[toDecrypt], "r")
        print driveLetter + ":/" + possibleEncryptedMessagesToDecrypt[toDecrypt]
        
        f_lines = fr.readlines()
        encryptedMessages = f_lines
        
        print encryptedMessages
        for i in encryptedMessages{
            //print int(i.strip("\n"))
            print hex(Decrypt(int(i.strip("\n")), int(PrivateKey[0]), [int(PrivateKey[1]), int(PrivateKey[0])]))[2:].strip("L")
            //decryptedMessages.append(IntToMessage(hex(Decrypt(int(i.strip("\n")), int(PrivateKey[0]), [int(PrivateKey[1]), int(PrivateKey[0])]))[2:].strip("L"))) 
            decryptedMessages.append(str(Decrypt(int(i.strip("\n")), int(PrivateKey[0]), [int(PrivateKey[1]), int(PrivateKey[0])])))
            print decryptedMessages
        }
        for i in decryptedMessages{
            print hex(int(i))
            print IntToMessage(hex(int(i))[2:].rpartition("L")[0])
        }
        fr.close()
        f.close()
    }    

}
        


"""   
print "Finding P..."
p = FindP()
print "Found P..."
print "-----------------------------------"

print "Finding Q..."
q = FindQ()
print "Found Q..."
print "-----------------------------------"

print "Generating product"
n = p * q 
print "Generated product"
print "-----------------------------------"

print "Generating totient function"
totient = int(EulerTotientFunc(n, p, q))
print "Generated totient function"
print "-----------------------------------"

print "Generating public key"
PublicKey = GeneratePublicKey(p, q, totient)
print "Generated public key"
print "-----------------------------------"

print "Generating private key"
PrivateKey = GeneratePrivateKey(p, q, PublicKey, totient)
print "Generated private key"
print "-----------------------------------"

message = raw_input("What message would you like to encrypt? ")
print "Splitting message into approximately " + str(len(message) / 5) + " sections"
message = SplitMessage(message)
print "Split message"
print "-----------------------------------"

print "Converting messages to hex"

new_message = []
for j in message{
    new_message.append(int(MessageToInt(j), 16))
    
}
print "Converted messages to hex"
message = new_message

print "--- ( messages = ",
for i in message{
    print i,
} 
print ") ---\n"

print "Encrypting message"

encrypedMessages = []
for i in message{
    encrypedMessages. append(Encrypt(i, PublicKey))

}

print "Finished encryption"
print "-----------------------------------"
print "Here is your encrypted message"
print encrypedMessages
print "Here is the decrypted message"

decryptedMessages = []

for i in encrypedMessages{
    decryptedMessages.append(Decrypt(i, PrivateKey, PublicKey))    
}

print str(decryptedMessages)[2:]
print hex(i)
for i in decryptedMessages{
    print IntToMessage(hex(i)[2:])
}
"""





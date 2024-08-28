import base64

class EncryptDecrypt:

    def encryptMessage(self, message):

        messageEncode = message.encode('utf-8')

        encodedMessage = base64.b16encode(messageEncode)  

        return encodedMessage.decode('utf-8')  

    def decryptMessage(self, encodedMessage):

        decodedMessage = base64.b16decode(encodedMessage)  

        return decodedMessage.decode('utf-8') 
    

test = EncryptDecrypt()

mensage = 'Pepito Perez'

print(mensage)

encryptedMessage = test.encryptMessage(mensage)

print(encryptedMessage)

decryptedMessage = test.decryptMessage(encryptedMessage)

print(decryptedMessage)

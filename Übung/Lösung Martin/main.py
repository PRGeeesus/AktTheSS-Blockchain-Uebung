import hashlib
import os
import numpy as np

ex_1_chain_path = "C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex1\\"
ex_2_base_path = "C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\"

class Block():
    def __init__(self,blocknumber,previous_hash,data):
        self.blocknumber = blocknumber
        self.previous_hash = previous_hash
        self.data = data
        self.nonce = 0


    def hashing(self):
        key = hashlib.sha256()
        # key.update( ("block=" + str(self.blocknumber) + "\n").encode('utf-8') )

        temp = b"".join([ b"\xef\xbb\xbf", (("block=" + str(self.blocknumber)+ "\n") +
                                          ("previous_hash=" + str(self.previous_hash)+"\n") +
                                          ("data=" + str(self.data)+"\n") ).encode() ])
        key.update(temp)
        return key.hexdigest()

    def hashingWithNonce(self):
        key = hashlib.sha256()
        # key.update( ("block=" + str(self.blocknumber) + "\n").encode('utf-8') )

        temp = b"".join([ b"\xef\xbb\xbf", (("block=" + str(self.blocknumber)+ "\n") +
                                          ("previous_hash=" + str(self.previous_hash)+"\n") +
                                          ("data=" + str(self.data)+"\n")+
                                          ("nonce=" + str(self.nonce)+"\n") ).encode() ])
        key.update(temp)
        return key.hexdigest()


class BlockChain():
    def __init__(self):
        self.chain = []

    def parseBlock(self,inputstring):
        tempBlock = Block(99,"","");
        counter = 0;
        output = inputstring.split("\n")
        tempBlock.blocknumber = output[0].split("block=")[1]
        tempBlock.previous_hash = output[1].split("previous_hash=")[1]
        tempsplice = output[2].split("data=")
        outputstring = ""
        if(len(tempsplice) >2):
            for i in range(0,len(tempsplice)-2):
                outputstring = outputstring + "data="
        tempBlock.data = outputstring + tempsplice[len(tempsplice)-1]
        return tempBlock

    def saveBlock(self,block,path):
        if int(block.blocknumber) < 10:
            name = "0" + str(block.blocknumber)
        else:
            name = str(block.blocknumber)
        file2write=open(path+name,'w')
        temp = (("block=" + str(block.blocknumber)+ "\n") +
                ("previous_hash=" + str(block.previous_hash)+"\n") +
                ("data=" + str(block.data)+"\n") )
        file2write.write(temp)
        file2write.close()

    def saveBlock_Nonce(self,block,path):
        if int(block.blocknumber) < 10:
            name = "0" + str(block.blocknumber)
        else:
            name = str(block.blocknumber)
        file2write=open(path+name,'w')
        temp = (("block=" + str(block.blocknumber)+ "\n") +
                ("previous_hash=" + str(block.previous_hash)+"\n") +
                ("data=" + str(block.data)+"\n")+
                ("nonce=" + str(block.nonce)+"\n") )
        file2write.write(temp)
        file2write.close()

    def generateAddSaveBlock(self,data,path):
        lastblock = self.chain[len(self.chain)-1]
        temp = Block(str(int(lastblock.blocknumber)+1),lastblock.hashing(),data)
        self.chain.append(temp)
        if(self.checkEntireChain()):
            self.saveBlock(temp,path)
            print("Appended and Saved New Block")


    def generateAddSaveBlock_Nonce(self,data,path,limit):
        counter = 0
        lastblock = self.chain[len(self.chain)-1]
        lastblock.nounce = counter;
        print("LIMIT:")
        print(str(limit))
        print("GUESSESING :")

        while(int(lastblock.hashingWithNonce(),16) > limit):
            #print(int(lastblock.hashingWithNonce(),16))
            counter = counter + 1;
            lastblock.nonce = counter
        print("nounce found: ")
        print(str(int(lastblock.hashingWithNonce(),16)) + " < ")
        print(str(limit))

        temp = Block(str(int(lastblock.blocknumber)+1),lastblock.hashingWithNonce(),data)
        temp.nonce = counter
        self.chain.append(temp)
        if(self.checkEntireChain()):
            self.saveBlock_Nonce(temp,path)
            print("Appended and Saved New Block")



    def checkEntireChain(self):
        if self.chain[0].previous_hash != "null" :
            print("Genesis block wrong")
            return -1

        for i in range(1,len(self.chain)):
            print("Checking Block " + str(i-1) + " hash vs. block " + str(i) + " saved" )
            if str(self.chain[i-1].hashing()) != str(self.chain[i].previous_hash) :
                print("Error: Consecutive hash Values do not match!")
                print("block " + str(self.chain[i-1].blocknumber) + " is hashed as:   " + str(self.chain[i-1].hashing()))
                print("block " + str(self.chain[i].blocknumber) + " is saved as :   " + str(self.chain[i].previous_hash))
                return -(i)
        print("Blockchain Correct:")
        print(" -" + str(len(self.chain)) + " Blocks Found")
        return 1


    def loadAppendBlocks(self,dir):
        for file in os.listdir(dir):
            file = open(dir+file,"r",encoding='utf-8')
            data = file.read()
            self.chain.append(self.parseBlock(data))
            file.close()
        print("Blockchain from " + dir + " loaded")

    def loadAppendBlock(self,path):

        file = open(path,"r",encoding='utf-8')
        data = file.read()
        self.chain.append(self.parseBlock(data))
        file.close()
        print("Block from " + path + " loaded")


    def printChain(self):
        for link in self.chain:
            print(str(link.blocknumber) +": "+ str(link.previous_hash))
            print(link.data)
            print("\n")





def main():
    # #Exercise 1
    # myBC = BlockChain();
    # myBC.loadAppendBlocks(ex_1_chain_path)
    # myBC.checkEntireChain()
    # myBC.printChain()

    #Exercise 2
    # 1)
    # for i in range(1,6):
    #     print("Blockchain: "+str(i))
    #     #print(ex_2_base_path + "blockchain_0" + str(i))
    #     myBC = BlockChain();
    #     path = ex_2_base_path + "blockchain_0" + str(i) + "\\"
    #     myBC.loadAppendBlocks(path)
    #     code = myBC.checkEntireChain()
    #     if(code == 1):
    #         #myBC.generateAddSaveBlock("Blockchain richtig.",path)
    #         print("Blockchain richtig.")
    #     else:
    #         #myBC.generateAddSaveBlock("Block " + str(code) + "wrong",path)
    #         print("Block " + str(code) + "wrong")

    ## 2)
    ## checking which block is the correct one BC 5
    # myBC = BlockChain();
    # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\00")
    ## corrected version
    # # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\01-corrected_version")
    ## inital version is the correct version
    # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\01-initial_version")
    # myBC.loadAppendBlock("C:\\Users\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\02")
    # myBC.printChain()
    # myBC.checkEntireChain()

    ## checking which block is the correct one BC 5
    # myBC = BlockChain();
    # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\00")
    ## corrected version
    # # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\01-corrected_version")
    ## inital version is the correct version
    # myBC.loadAppendBlock("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\01-initial_version")
    # myBC.loadAppendBlock("C:\\Users\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex2_all\\blockchain_05\\02")
    # myBC.printChain()
    # myBC.checkEntireChain()

    ## BC 4 - the Hashing of Block 1 and the saved hash of 1 in Block 2 do not match.
    ## Assumingly Block 1 was edited Afterwards

    ## BC 1 - the hashing of Block 1 and the saved hash of 1 in Block 2 do not match.
    ## Assumingly Block 1 was edited Afterwards

    ## 3.)
    # Um eine veränderung in der Blockchain Unkenntlich zu machen müsste man Block n änderen und
    # dann Block n+1 mit dem neuen Hash des n-ten Blocks versehen. Danach müsste Block n+1 mit deinem neuen
    # previous_hash und seinen alten Daten gehasht werden und in Block n+2 gespeichert werden.
    # diese schritte müssten für alle Blöcke von n bis BC-länge wiederholt werden


    ## Exercise 3
    # 1)
    # Vorteil:  - Überprüfun von Korrekten Blöcken ist einfacher als Hinzufügen
    # Nachteil: - Hinzufügen von Blöcken ist aufwendiger
    #           - Hoher Energieverbrauch
    #           - Certainty of correct branch becomes certain only with time
    #           -
    #2)
    # myBC = BlockChain()
    # myBC.loadAppendBlocks("C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex3\\")
    # myBC.printChain()
    # myBC.checkEntireChain()
    # limit = int("0x000000ffffffffffffffffffffffffffffffffffffffffffffffffffffffffff", 16)
    # print("Linit is: " + str(hex(limit)))
    # myBC.generateAddSaveBlock_Nonce("But Block 1 seems Wrong","C:\\Users\\isa_2\\OneDrive\\RAS - Master\\Aktuelle Themen SSE\\Übung\\blockchain_ex3\\",limit)




main()

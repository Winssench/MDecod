sigFox1 = "5AFC0142850A142850A14285"
sigFox2 = "850A142850A142850A142850"

binMessage1 = "{0:08b}".format(int(sigFox1, 16))
binMessage2 = "{0:08b}".format(int(sigFox1, 16))

print("1",binMessage1)
print("2", binMessage2)

idbit1 = int(binMessage1[0:1], 2)
idbit2 = int(binMessage2[0:1], 2)
temperature = int(binMessage1[1:7], 2) - 20
humidity = int(binMessage1[7:13], 2)
pressure = int(binMessage1[13:20], 2) + 936


print("id1", idbit1)
print("id2", idbit2)



hourVisits1 = [binMessage1[x:x+7] for x in range(20,len(binMessage1) - 6, 7)]

secondMessageReceived = False

hourVisits2 = [binMessage2[x:x+7] for x in range(2,len(binMessage2) - 3, 7)]

partLeft = binMessage1[len(binMessage1) - 6: len(binMessage1)] + binMessage2[1:2]


'''
dealing with second message

'''
print("pMessage2")
for x in hourVisits2:
    print("item" , x)
if(secondMessageReceived):
    print("")
    partLeft.append()


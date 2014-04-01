# Splitter - used for dividing logs strings/text on needed length per line

def splitLine(text, symbPerLine):
    text=text.split('\n')
    splitedText=[]
    
    # Thx stackoverflow for this method of spliting!
    for lin in text:
        tempArr = [ lin[i:i+symbPerLine] for i in range(0,len(lin),symbPerLine) ]
        for elem in tempArr:
            splitedText.append(elem)
    
    return splitedText

def convertToPsCommand(commandString):
    pre = 'powershell -Command "'
    end = '"'
    convString = ''
    
    for ch in commandString:
        if ch == '"':
            convString = convString + '\\"'
        else:
            convString = convString + ch
            
    return pre + convString + end
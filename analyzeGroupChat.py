import sys
import json
import copy

def main():
    #Check if the user has provided a file to analyze
    if len(sys.argv) != 2:
        print("Chat file missing. Please add path to filename as an argument.")
        sys.exit()
    
    #Load the json file
    with open(sys.argv[1]) as f:
        chat = json.load(f)
    
    #Create an array containing the participants
    participants = []
    for name in chat['participants']:
        participants.append(name['name'])
    
    #This tracks how many messages each participant has sent
    messagesSent = dict.fromkeys(participants, 0)
    #This tracks how many images each participant has sent
    imagesSent = dict.fromkeys(participants, 0)
    #This tracks how many reactions each participant made
    reactionsMade = dict.fromkeys(participants, 0)
    #This tracks how many reactions each participant received
    reactionsReceived = dict.fromkeys(participants, 0)
    #This tracks the most reacted message. The string is the message or image URL
    #The integer is the total number of reactions
    mostReactedMessage = ['',0]

    calcMessagesSent(chat, messagesSent)
    calcImagesSent(chat, imagesSent)
    calcReactions(chat, reactionsMade, reactionsReceived, mostReactedMessage)

    #Print the results
    print('Messages sent:\n', messagesSent, '\n')
    print('Images sent:\n', imagesSent, '\n')
    print('Reactions:\n', reactionsMade, '\n')
    print('Reactions received:\n', reactionsReceived, '\n')
    print('Most reacted message:\n', messageToString(mostReactedMessage[0]), '\n')

#Counts the total number of messages sent by each participant
def calcMessagesSent(chat, messagesSent):
    #For every message
    for message in chat['messages']:
        #Update the message count for the sender
        messagesSent[message['sender_name']] = messagesSent[message['sender_name']] + 1

#Counts the total number of images sent by each participant
def calcImagesSent(chat, imagesSent):
    #For every message
    for message in chat['messages']:
        #If there is an image in the message
        if 'photos' in message:
            #Count the number of photos sent
            numImagesSent = len(message['photos'])
            #Update the image count for the sender
            imagesSent[message['sender_name']] = imagesSent[message['sender_name']] + numImagesSent   

#Counts the total number of reactions each participant made
def calcReactions(chat, reactionsMade, reactionsReceived, mostReactedMessage):
    #For every message
    for message in chat['messages']:
        #If a message has a reaction
        if 'reactions' in message:
            #Create a list of unique reactions (the dataset can contain duplicates)
            reactions = []
            for reaction in message['reactions']: 
                if reaction not in reactions:
                    reactions.append(reaction)
            #If the number of reactions is greater than the most reacted message
            if len(reactions) > mostReactedMessage[1]:
                #Update the most reacted message with this message
                mostReactedMessage[0] = message
                mostReactedMessage[1] = len(reactions)
            #Update the reactionsMade values for each person who reacted
            for reaction in reactions:
                reactionsMade[reaction['actor']] = reactionsMade[reaction['actor']] + 1
            #Update the reactionsReceived values for the message sender
            reactionsReceived[message['sender_name']] = reactionsReceived[message['sender_name']] + len(reactions)

#Returns a message in string format with sender, message and image urls (if any)
def messageToString(message):
    messageString = 'Author: ' + message['sender_name'] + '\n'
    if 'content' in message:
        messageString = messageString + 'Message: ' + message['content'] + '\n'
    if 'photos' in message:
        for image in message['photos']:
            messageString = messageString + 'Image: ' + image['uri'] + '\n'
    return messageString

if __name__ == "__main__":
    main()

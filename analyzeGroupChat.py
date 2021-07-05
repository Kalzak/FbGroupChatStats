import sys
import json

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
    
    #This tracks how many reactions each participant made
    reactionsMade = dict.fromkeys(participants, 0)
    #This tracks how many reactions each participant received
    reactionsReceived = dict.fromkeys(participants, 0)

    calcReactions(chat, reactionsMade, reactionsReceived)
    print(reactionsMade)
    print(reactionsReceived)

#Counts the total number of reactions each participant made
def calcReactions(chat, reactionsMade, reactionsReceived):
    #For every message
    for message in chat['messages']:
        #If a message has a reaction
        if 'reactions' in message:
            #Create a list of unique reactions (the dataset can contain duplicates)
            reactions = []
            for reaction in message['reactions']: 
                if reaction not in reactions:
                    reactions.append(reaction)
            #Update the reactionsMade values for each person who reacted
            for reaction in reactions:
                reactionsMade[reaction['actor']] = reactionsMade[reaction['actor']] + 1
            #Update the reactionsReceived values for the message sender
            reactionsReceived[message['sender_name']] = reactionsReceived[message['sender_name']] + len(reactions)

if __name__ == "__main__":
    main()

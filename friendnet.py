
def read_file():
    friend_file = open('friends.txt', 'r')
    lines = friend_file.readlines()
    friends_dict = {}
    for line in lines:
        line = line[:-1] # remove new line character
        words = line.split(' ')
        person = words[0]
        if person in friends_dict:
            relationships = friends_dict[person]
            relationships.append((words[1], words[2]))
            friends_dict[person] = relationships
        else:
            # add to dictionary: words[1] = person, words[2] = number
            friends_dict[person] = [(words[1], words[2])] 
    return friends_dict



def main():
    friends_dict = read_file()
    print(friends_dict)

if __name__ == "__main__":
    main()
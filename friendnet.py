'''
    Friend Net
    Katrina Baber and Lucy Tibbetts

    Best Friend Chain idea
    1. Convert graph to DAG
    2. Negate all weights
    3. Run shortest path algorithm (probably Dijkstra's)

    Killer feature ideas:
    1. Best mutual friend: given two users, user A and user B, find the "best" mutual friend
    
    Algorithm:
    First, we will calculate all mutual friends, i.e. users who are in the friend lists for both users.
    Second, we will calculate a friendliness sum for each mutual friend (user C). The friendliness sum will be
    comprised of how much user A likes user C, how much user B likes user C, how much user C likes user A, and
    how much user C likes user B

    2. Distance from everyone, i.e. print out a list of a user's 1st, 2nd, 3rd, etc. connections, where 1st means
    they are direct friends, 2nd means they have a mutual friend, 3rd means they are two friends removed, and so on
    * This feature would require us to traverse the whole graph
    
    Algorithm:
    Find the shortest path between the given user and each other user. We will likely use Dijkstra's shortest path
    algorithm for these calculations. Then, output the connections by level, e.g. 1st, 2nd, 3rd, where 1st indicates
    a path length of 1, 2nd indicates a path length of 2, etc. 

'''

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
            relationships[words[1]] = words[2]
            friends_dict[person] = relationships
        else:
            # add to dictionary: words[1] = person, words[2] = number
            friends_dict[person] = {words[1] : words[2]}
    return friends_dict

def look_up_user(friends_dict):
    print("What user would you like to look up?")
    user = input()
    if user in friends_dict:
        print(user + " exists!")
    else:
        print(user + " does not exist :(")

def look_up_relationship(friends_dict):
    print("Please enter the first user's name: ")
    user_1 = input()
    print("Please enter the second user's name: ")
    user_2 = input()
    if user_1 in friends_dict:
        user_1_friends = friends_dict[user_1]
        if user_2 in user_1_friends:
            weight = user_1_friends[user_2]
            print("The relationship from " + user_1 + " to " + user_2 + " is " + weight)
        else:
            print(user_1 + " is not friends with " + user_2) 
    else:
        print(user_1 + " does not exist")

def main():
    friends_dict = read_file()
    print("Welcome to Friend Net")
    print("What would you like to do? (Enter a number 1-2)")
    print("1. Look up a user")
    print("2. Look up the relationship between two users")
    choice = 0
    while choice < 1 or choice > 2:
        try:
            choice = int(input())
            if choice == 1:
                look_up_user(friends_dict)
            elif choice == 2:
                look_up_relationship(friends_dict)
            else:
                print("Please enter a number 1-2")
        except ValueError:
            print("Please enter a number 1-2")

if __name__ == "__main__":
    main()
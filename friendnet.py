import sys

'''
    Friend Net
    Katrina Baber and Lucy Tibbetts

    Killer features:
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

def best_friend_chain(friends_dict):
    print("Please enter the first user's name: ")
    user_1 = input()
    print("Please enter the second user's name: ")
    user_2 = input()

    if user_1 in friends_dict and user_2 in friends_dict:
        # implement dijkstra's
        # resource: https://medium.com/basecs/finding-the-shortest-path-with-a-little-help-from-dijkstra-613149fbdc8e
        visited = [] 
        unvisited = []
        distance_vals = {} # store distances as we build potential paths

        # transform weights in friends_dict
        for user in friends_dict:
            distance_vals[user] = [sys.maxsize, None]
            unvisited.append(user)
            friends = friends_dict[user] # set distance to infinity
            for friend in friends:
                weight = friends[friend]
                friends[friend] = 10 - int(weight)
        
        # set user_1 distance to 0
        distance_vals[user_1] = [0, user_1]
    
        while user_2 not in visited:
            # select node with minimum distance from distance_vals
            min_dist_node = min(filter(lambda val: val in unvisited, distance_vals), 
            key=lambda val: distance_vals[val][0])
            # calculate distance for adjacent nodes
            adjacent_nodes = friends_dict[min_dist_node]
            for node in adjacent_nodes:
                if node in unvisited:
                    dist = distance_vals[min_dist_node][0] + adjacent_nodes[node]
                    current_best_dist = distance_vals[node][0]
                    if dist < current_best_dist:
                        distance_vals[node] = [dist, min_dist_node] # update with new distance and previous node
            # move node from unvisited to visited
            visited.append(min_dist_node)
            unvisited.remove(min_dist_node)

        # based on data stored in distance_vals, construct 'best friend chain'
        path = [user_2]
        current_user = user_2
        while current_user != user_1:
            current_user = distance_vals[current_user][1]
            path.append(current_user)
        print("Best friend chain: " + str(path))
    elif user_1 not in friends_dict:
        print(user_1 + " is not a valid user")
    elif user_2 not in friends_dict:
        print(user_2 + " is not a valid user")

def best_mutual_friend(friends_dict):
    print("Please enter the first user's name: ")
    user_1 = input()
    print("Please enter the second user's name: ")
    user_2 = input()
    if user_1 in friends_dict and user_2 in friends_dict:
        # find all mutual friends
        mutual_friends = {}
        for user in friends_dict:
            if user in friends_dict[user_1] and user in friends_dict[user_2]:
                # found a mutual friend
                # calculate "friendliness sum": comprised of how much user A likes user C, 
                # how much user B likes user C, how much user C likes user A, and
                # how much user C likes user B
                friendliness = int(friends_dict[user_1][user]) + int(friends_dict[user_2][user]) 
                if user_1 in friends_dict[user]:
                    friendliness += int(friends_dict[user][user_1])
                if user_2 in friends_dict[user]:    
                    friendliness += int(friends_dict[user][user_2])
                mutual_friends[user] = friendliness
        if len(mutual_friends) == 0:
            # no mutual friends
            print(user_1 + " and " + user_2 + " have no mutual friends :(")
        else:
            # find user with the highest "friendliness sum"
            print(mutual_friends)
            best_mutual_friend = max(mutual_friends, key=mutual_friends.get)
            print("The best mutual friend is: " + best_mutual_friend)

    elif user_1 not in friends_dict:
        print(user_1 + " is not a valid user")
    elif user_2 not in friends_dict:
        print(user_2 + " is not a valid user")
    
def user_connections(friends_dict):
    print("Please enter a user's name: ")
    user = input()
    if user in friends_dict:
        print(user + " has the following connections:")
        # use djikstra's to find shortest path to every other user
        user_paths = {}
        for other_user in friends_dict:
            visited = [] 
            unvisited = []
            distance_vals = {} # store distances as we build potential paths

            for person in friends_dict:
                distance_vals[person] = [sys.maxsize, None] # set distance to infinity
                unvisited.append(person)

            # set user distance to 0
            distance_vals[user] = [0, user]
            while other_user not in visited:
                # select node with minimum distance from distance_vals
                min_dist_node = min(filter(lambda val: val in unvisited, distance_vals), 
                key=lambda val: distance_vals[val][0])
                # calculate distance for adjacent nodes
                adjacent_nodes = friends_dict[min_dist_node]
                for node in adjacent_nodes:
                    if node in unvisited:
                        dist = distance_vals[min_dist_node][0] + int(adjacent_nodes[node])
                        current_best_dist = distance_vals[node][0]
                        if dist < current_best_dist:
                            distance_vals[node] = [dist, min_dist_node] # update with new distance and previous node
                # move node from unvisited to visited
                visited.append(min_dist_node)
                unvisited.remove(min_dist_node)

            # based on data stored in distance_vals, construct the shortest path
            path = [other_user]
            current_user = other_user
            while current_user != user:
                current_user = distance_vals[current_user][1]
                path.append(current_user)
            user_paths[other_user] = path

        path_lengths = {}
        # determine path lengths, e.g. 1st, 2nd, and 3rd connections
        for user in user_paths:
            path = user_paths[user]
            if len(path) > 1:
                # path to another user
                path_lengths[user] = len(path) - 1

        # group by path length 
        grouped_users = {}
        for user in path_lengths:
            path_length = path_lengths[user]
            if path_length in grouped_users:
                users = grouped_users[path_length]
                users.append(user)
                grouped_users[path_length] = users
            else:
                grouped_users[path_length] = [user]

        # print out grouped "connections"
        for group in sorted(grouped_users):
            print("Level " + str(group) + " connections: " + str(grouped_users[group]))

    else:
        print(user + " is not a valid user")

def main():
    friends_dict = read_file()
    print("Welcome to Friend Net")
    print("What would you like to do? (Enter a number 1-5)")
    print("1. Look up a user")
    print("2. Look up the relationship between two users")
    print("3. Look up the best friend chain between two users")
    print("4. Find the 'best mutual friend' between two users")
    print("5. View a user's 'connections'")
    choice = 0
    while choice < 1 or choice > 5:
        try:
            choice = int(input())
            if choice == 1:
                look_up_user(friends_dict)
            elif choice == 2:
                look_up_relationship(friends_dict)
            elif choice == 3:
                best_friend_chain(friends_dict)
            elif choice == 4:
                best_mutual_friend(friends_dict)
            elif choice == 5:
                user_connections(friends_dict)
            else:
                print("Please enter a number 1-2")
        except ValueError:
            print("Please enter a number 1-2")

if __name__ == "__main__":
    main()
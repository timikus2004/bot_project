def print_list(list):
    string_of_users = ''
    for user in range(len(list)):
        string_of_users += list[user] + ' '
    print(string_of_users)
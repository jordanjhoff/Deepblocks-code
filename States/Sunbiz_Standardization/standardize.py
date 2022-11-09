'''This set of functions takes the output from one of the currently existing sunbiz equivalent bots and re-formats it into a standardized output'''

# Input: dictionary, Output: dictionary
# deletes all empty keys and changes all empty values that doesnt have a empty key to "No Data Found"
# removes all '\n's that are present at any level in the nested dictionaries and replaces them with spaces
def check_format(dict):
    del_list = []
    for key, val in dict.items():
        sub_del_list = []
        if key == '' or key == ' ':
            del_list.append(key)
        if not val:
            dict[key]['No'] = 'Data Found'
        for k, v in val.items():
            if k == '' or k == ' ':
                sub_del_list.append(k)
            if v == '' or v == ' ':
                dict[key][k] = 'No Data Found'
            if isinstance(v, list):
                temp = v
                for i in range(len(temp)):
                    temp[i] = temp[i].replace('\n', ' ')
                dict[key][k] = temp
            else:
                dict[key][k] = dict[key][k].replace('\n', ' ')
        if sub_del_list:
            for k in sub_del_list:
                del val[k]
    if del_list:
        for key in del_list:
            del dict[key]
    return dict


# input: dictionary, output: dictionary
# makes sure there is an information dictionary and if one doesn't exists then it creates one
def make_information(dict):
    delete = ''
    for key, val in dict.items():
        if key.lower() == 'profile':
            delete = key
        elif key.lower() == 'details':
            delete = key
        elif key.lower() == 'entity info':
            delete = key
        elif key.lower() == 'business information':
            delete = key
    if delete:
        dict['Information'] = dict.pop(delete)
    return dict


# Searches for an agent dictionary using the keyword 'agent', if there is one it changes its name to 'Agent Information' and transfers all of information to that new dictionary while deleting the old one. If there is no agent dictionary then it creates a dictionary with the key 'Agent Information' and it finds any information at any point within the output that says 'agent' in the key and moves it into that dictionary.
def make_agent(dict):
    agent = {}
    delete = ''
    for key, val in dict.items():
        pop_list = []
        if key == 'Agent Information':
            return dict
        if 'agent' in key.lower():
            delete = key
        for v in val:
            if 'agent' in v.lower() and not delete:
                agent[v] = val[v]
                pop_list.append(v)
        if pop_list:
            for i in range(len(pop_list)):
                del val[pop_list[i]]
    if delete:
        dict['Agent Information'] = dict.pop(delete)
        return dict
    if agent:
        dict['Agent Information'] = agent
    else:
        dict['Agent Information'] = {'No': 'Data Found'}
    return dict


# searches for an agent dictionary using the keyword 'officer', if there is one it changes its name to 'officer' and transfers all of information to that new dictionary while deleting the old one. If there is no officers dictionary then it creates a dictionary with the key 'Officers' and it finds any information at any point within the output that says 'officer' in the key and moves it into that dictionary.
def make_officer(dict):
    officer = {}
    delete = ''
    for key, val in dict.items():
        pop_list = []
        if key == 'Officers':
            return dict
        if 'director' in key.lower() or 'officer' in key.lower():
            delete = key
        for v in val:
            if 'officer' in v.lower() or 'director' in v.lower() and not delete:
                officer[v] = val[v]
                pop_list.append(v)
        if pop_list:
            for i in range(len(pop_list)):
                del val[pop_list[i]]
    if delete:
        dict['Officers'] = dict.pop(delete)
        return dict
    if officer:
        dict['Officers'] = officer
    else:
        dict['Officers'] = {'No': 'Data Found'}
    return dict


# takes all information from what used to be the information dictionary and stores it in a dictionary called 'General Information' within the information dictionary. Then, it goes throughout the rest of the output to look for any dictionary other than the information, agent, or officer dictionaries, and moves those dictionaries into the information dictionary, after the general information dictionary --> Ex. ({'Information' :{General Information : {...}, Stocks : {...}})
def adjust_information(dict):
    del_list = []
    avoid = ['information', 'agent', 'officer']
    for key, val in dict.items():
        if all(word not in key.lower() for word in avoid):
            del_list.append(key)
    information = {}
    general_info = dict.pop('Information')
    information['General Information'] = general_info
    for d in del_list:
        information[d] = dict.pop(d)
    dict['Information'] = information
    return (dict)


# Goes into the agent information dictionary and checks through the keys for the keywords 'name', 'email', and 'address' (if 'address' is found it checks for the keywords 'street' and 'mail' to determine what kind of address it is). If any are found, it changes the keys of the information to appropriate key names, and any extra information regarding the agent that doesnt have any matching keywords is stored in a dictionary inside agent information titled 'Extra Agent Info'.
def adjust_agents(dict):
    move_list = []
    email = []
    name = []
    addresses = []

    if 'No' in dict['Agent Information'].keys() and dict['Agent Information']['No'] == 'Data Found':
        return dict
    for key, val in dict['Agent Information'].items():
        if 'email' in key.lower():
            email = key
        elif 'name' in key.lower():
            name = key
        elif 'address' in key.lower():
            addresses.append(key)
        else:
            move_list.append(key)

    if name:
        dict['Agent Information']['Name'] = dict['Agent Information'].pop(name)
    else:
        dict['Agent Information']['Name'] = 'No Data Found'
    if email:
        dict['Agent Information']['Email'] = dict['Agent Information'].pop(email)
    else:
        dict['Agent Information']['Email'] = 'No Data Found'
    if addresses:
        for address in addresses:
            if 'mail' in address.lower():
                dict['Agent Information']['Mailing Addresses'] = dict['Agent Information'].pop(address)
            elif 'street' in address.lower():
                dict['Agent Information']['Street Addresses'] = dict['Agent Information'].pop(address)
            else:
                dict['Agent Information']['Addresses'] = dict['Agent Information'].pop(address)
    else:
        dict['Agent Information']['Address'] = 'No Data Found'

    if move_list:
        extra_info = {}
        for move in move_list:
            extra_info[move] = dict['Agent Information'].pop(move)
        dict['Agent Information']['Extra Agent Info'] = extra_info
    return (dict)


# Goes into the Officers dictionary and checks through the keys for the keywords 'name', 'title', and 'address' (if 'address' is found it checks for the keywords 'street' and 'mail' to determine what kind of address it is). If any are found, it changes the keys of the information to appropriate key names, and any extra information regarding the officrs (such as 'Effective From' : '2/15/08') that doesnt have any matching keywords is stored in a dictionary inside Officers titled 'Extra Officer Info'.
def adjust_officers(dict):
    move_list = []
    title = []
    name = []
    addresses = []
    if 'No' in dict['Officers'].keys() and dict['Officers']['No'] == 'Data Found':
        return dict
    for key, val in dict['Officers'].items():
        if 'title' in key.lower():
            title = key
        elif 'name' in key.lower():
            name = key
        elif 'address' in key.lower():
            addresses.append(key)
        else:
            move_list.append(key)

    if name:
        dict['Officers']['Names'] = dict['Officers'].pop(name)
    else:
        dict['Officers']['Name'] = 'No Data Found'
    if title:
        dict['Officers']['Titles'] = dict['Officers'].pop(title)
    else:
        dict['Officers']['Titles'] = 'No Data Found'
    if addresses:
        for address in addresses:
            if 'mail' in address.lower():
                dict['Officers']['Mailing Addresses'] = dict['Officers'].pop(address)
            elif 'street' in address.lower():
                dict['Officers']['Street Addresses'] = dict['Officers'].pop(address)
            else:
                dict['Officers']['Addresses'] = dict['Officers'].pop(address)
    else:
        dict['Officers']['Addresses'] = 'No Data Found'

    if move_list:
        extra_info = {}
        for move in move_list:
            extra_info[move] = dict['Officers'].pop(move)
        dict['Officers']['Extra Officer Info'] = extra_info
    return dict


# the main method, runs all of the functions above
# input: not standardized output from sunbiz equivalent bot
# output: standardized nested dictionaries
def standardize(dict):
    dict = check_format(dict) 
    dict = make_information(dict)
    dict = make_agent(dict)
    dict = make_officer(dict)
    dict = check_format(dict)
    dict = adjust_information(dict)
    dict = adjust_agents(dict)
    dict = adjust_officers(dict)

    return dict
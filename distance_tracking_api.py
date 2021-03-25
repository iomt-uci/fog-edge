import pickle
import sklearn
from sklearn.tree import DecisionTreeClassifier

three_feet_tree =  pickle.load(open('3FeetTree.sav', 'rb'))
six_feet_tree =  pickle.load(open('6FeetTree.sav', 'rb'))
nine_feet_tree =  pickle.load(open('9FeetTree.sav', 'rb'))
indoor_model = pickle.load(open('IndoorPosModel.sav', 'rb'))


def get_SD_Alarms(USR):
    '''
    return a list of int. each int is the distance prediction between
    this device and another device.
    '''
    result = []
    for u in USR.values():
        if int(u) == -90:
            result.append(0)
            continue
        alarm = 4
        if nine_feet_tree.predict([[int(u)]]):
            alarm = 3
            if six_feet_tree.predict([[int(u)]]):
                alarm = 2
                if three_feet_tree.predict([[int(u)]]):
                    alarm = 1
        result.append(alarm)
    return result


def get_current_position(AP):
    '''
    returns a list of two int, the x and y coordinate.
    '''
    data = list(AP.values())
    result = indoor_model.predict([data])[0]
    temp = []
    position = []
    if "ï¼Œ" in result:
        temp = result.split("ï¼Œ")
    else:
        temp = result.split(",")
    position.append(temp[0].lstrip("("))
    position.append(temp[1].rstrip(")"))
    return position

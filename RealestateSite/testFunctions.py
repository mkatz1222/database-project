from flask_login import current_user
from sqlalchemy import desc
from sqlalchemy.sql.expression import func

from RealestateSite import db
from RealestateSite.models import Houses, User, Agents, Buyers, Sellers

"""
This is just a file I was using to test processes that were implemented in other places.
"""
def showHouses():
    houses = Houses.query.all()
    for x in houses:
        print(x)
    print(houses)

def nextHighestHouseID():
    maxHouseID = db.session.query(func.max(Houses.houseID))
    maxID = maxHouseID[0]
    maxID = maxID[0]
    nextMaxID = maxID+1
    return nextMaxID

def nextHighestUserID():
    maxUserID = db.session.query(func.max(User.id))
    maxID = maxUserID[0]
    maxID = maxID[0]
    nextMaxID = maxID+10
    return nextMaxID


def getUserRole():
    role = current_user.userRole
    return role


def showAgents():
    agents = Agents.query.all()
    for x in agents:
        print(x)

#testViews
def clientViewOfAgents():
    agents = Agents.clientView(db.Model)
    for x in agents:
        print(x)

def adminViewOfAgents():
    agents = Agents.managerView(db.Model)
    for x in agents:
        print(x)

def getBuyers():
    buyers = Buyers.query.all()
    for x in buyers:
        print(x)

def getSellers():
    sellers = Sellers.query.first()
    user = User.query.filter(User.id == sellers.sellerID).all()
    print(user)

# clientViewOfAgents()
#adminViewOfAgents()
#showAgents()
# getBuyers()
# getSellers()




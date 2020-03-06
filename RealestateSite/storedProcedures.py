from sqlalchemy import text
from sqlalchemy.sql.expression import func
from RealestateSite import db
from RealestateSite.models import Houses, Agents, Branches


def nextHighestID():
    maxHouseID = db.session.query(func.max(Houses.houseID))
    maxID = maxHouseID[0]
    maxID = maxID[0]
    nextMaxID = maxID+1
    return nextMaxID


def selectAllUsers():
    value = text("SELECT * FROM agents")
    return value


def selectAllBranches():
    branches = db.session.query(Branches).all()
    for x in branches:
        print(x)

def compareBranchesFunction(branchOne, branchTwo):
    firstBranch = Branches.query.filter(Branches.branchID == branchOne).all()
    secondBranch = Branches.query.filter(Branches.branchID == branchTwo).all()
    x = firstBranch[0]
    y = secondBranch[0]
    if x.averageIncome > y.averageIncome:
        return [x,y]
    else:
        return [y,x]


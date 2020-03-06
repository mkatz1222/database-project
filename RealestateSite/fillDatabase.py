from RealestateSite import db, bcrypt
from RealestateSite.models import Houses, Agents, Branches, Roles, User, Managers, Buyers, Sellers
from random import randint
import random

firstNames = ['Rick', 'Ryan', 'Jonathan', 'Michael', 'Emma', 'William', 'Olivia', 'Ava', 'Mia', 'Alexander', 'Mila',
              'Daniel', 'Aiden', 'Aria', 'John', 'Owen', 'Chloe', 'Penelope', 'Riley', 'Dylan', 'Lily', 'Nora', 'Jayden',
              'Jack', 'Wyatt', 'Madison', 'Luna', 'Gabriel', 'Julian', 'Aubrey', 'Addison', 'Violet', 'Leo', 'Elias',
              'Robert',
              'Chris', 'Cora', 'Sarah', 'Jordan', 'Jason', 'Madeline', 'Hailey', 'Jordan', 'Cooper', 'Adam', 'Allison',
              'James',
              'Robert', 'William', 'David', 'Richard', 'Joseph', 'Thomas', 'Charles', 'Daniel', 'Christoper', 'Daniel',
              'Mathew',
              'Anthony', 'Donald', 'Mark', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth', 'Barbara', 'Susan',
              'Jessica',
              'Sarah', 'Karen', 'Nancy', 'Margaret', 'Lisa', 'Betty', 'Dorothy', 'Sandra']
lastNames = ['Smith', 'Johnson', 'Williams', 'Jones', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor',
             'Anderson', 'Hall',
             'Allen', 'Young', 'Hernandez', 'King', 'Wright', 'Lopez', 'Hill', 'Scott', 'Green', 'Adams', 'Stewart',
             'Sanchez',
             'Morris', 'Rogers', 'Reed', 'Cook', 'Morgan', 'Bell', 'Murphy', 'Bailey', 'Rivera', 'Price', 'Bennet',
             'Wood',
             'Barnes', 'Ross', 'Henderson', 'Coleman', 'Jenkins', 'Perry', 'Powell', 'Long', 'Thomas', 'Jackson',
             'White',
             'Harris', 'Martin', 'Thompson', 'Garcia', 'Martinez', 'Robinson', 'Clark', 'Rodriguez', 'Lewis', 'Lee',
             'Walker',
             'Barker', 'Gonzalez', 'Nelson', 'Carter', 'Mitchell', 'Perez', 'Roberts', 'Turner', 'Phillips', 'Campell',
             'Parker', 'Evands', 'Edwards', 'Collins', 'Cooper', 'Richardson', 'Cox', 'Howard', 'Ward', 'Torres',
             'Peterson',
             'Gray', 'Ramirez', 'James', 'Watson', 'Brooks', 'Kelly', 'Sanders', 'Patterson', 'Hughes', 'Flores',
             'Washington',
             'Butler', 'Simmons', 'Foster', 'Gonzales', 'Bryant', 'Alexander', 'Russel', 'Griffin', 'Diaz', 'Hayes']
streetNames = ['Random', '1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th', '11th', '12th', '13th',
               '14th', '15th',
               '16th', '17th', '18th', '19', '20th', 'Main', 'Oak', 'Pine', 'Maple', 'Cedar', 'Elm', 'View',
               'Washington', 'Lake',
               'Hill', 'Aspen', 'Park', 'Dogwood', 'Holly', 'Apache', 'Lehua']
streetSuffix = ['Avenue', 'Street', 'Road', 'Path', 'Way', 'Lane', 'Grove', 'Place', 'Gardens', 'Bypass', 'Square',
                'Hill',
                'Mews', 'Vale', 'Rise', 'Row']
cityNames = ['Washington', 'Springfield', 'Franklin', 'Lebanon', 'Clinton', 'Greenville', 'Bristol', 'Fairview',
             'Salem',
             'Madison', 'Georgetown', 'Arlington', 'Ashland', 'Dover', 'Oxford', 'Jackson', 'Burlington', 'Manchester',
             'Milton',
             'Newport']

booleanChoice = [True, False]
integerChoice = [1, 0]


def addRoles():

    user = Roles(roleID=1, roleName='User')
    buyer = Roles(roleID=2, roleName='Buyer')
    seller = Roles(roleID=3, roleName='Seller')
    agent = Roles(roleID=4, roleName='Agent')
    admin = Roles(roleID=5, roleName='Admin')
    db.session.add(buyer)
    db.session.add(seller)
    db.session.add(user)
    db.session.add(agent)
    db.session.add(admin)
    db.session.commit()


def addBranches():

    for x in range(20):
        branch = Branches(branchID=x + 1, city=cityNames[x], averageIncome=0)
        db.session.add(branch)
        # print(branch)
    db.session.commit()
    print("Added all Branches.")



def addHouses(x):

    ids = []
    for x in range(x+1):
        current = x
        ids.append(current)

    for y in range(x):
        house = Houses(houseID=ids[y], saleStatus=random.choice(booleanChoice), price=randint(1, 500000),
                       numberBedrooms=randint(1, 15), numberBathrooms=randint(1, 15),
                       sizeSqft=randint(1, 10000),
                       address=str(randint(1, 100)) + ' ' + random.choice(streetNames) + ' ' + random.choice(
                           streetSuffix),
                       city=random.choice(cityNames),
                       canTour=random.choice(booleanChoice), age=randint(1, 80),
                       fencedYard=random.choice(integerChoice), pool=random.choice(integerChoice))
        db.session.add(house)
        #print(house)
    db.session.commit()
    print("Added all houses.")

def addUsers(amount):

    print("Adding users.")
    hashed_password = bcrypt.generate_password_hash('admin').decode('utf-8')
    admin = User(id=amount, username='admin', email='admin'+'@gmail.com', password=hashed_password, userRole=5)
    manager = Managers(managerID=amount, userID=amount, managerName='admin', phoneNumber=randint(1000000000, 9999999999))

    db.session.add(admin)
    db.session.add(manager)
    #print(admin)

    for x in range(amount):
        endingInt = str(randint(1, 100))
        firstName = random.choice(firstNames)
        lastName = random.choice(lastNames)
        userName = str(random.choice(firstNames) + random.choice(lastNames))
        hashed_password = bcrypt.generate_password_hash(userName + endingInt).decode('utf-8')
        email = str(userName + endingInt)+'@gmail.com'

    # Users
        if x <= int(amount/5):
            user = User(id=x, username=userName, email=email, password=hashed_password, userRole=1)
            #print(user)
            db.session.add(user)

    # Agents
        elif x <= int((2*amount)/5):

            #print('This is an agent.')
            user = User(id=x, username=userName, email=email, password=hashed_password, userRole=4)
            #print(user)
            db.session.add(user)
            agent = Agents(agentID=x, userID=x, agentName=firstName + ' ' + lastName,
                           branchID=randint(1, 20), incomeLastYear=randint(0, 50000),
                           phoneNumber=randint(1000000000, 9999999999))
            db.session.add(agent)
            #print(agent)
            db.session.commit()

            lastAgent = db.session.query(Agents).order_by(Agents.agentID.desc()).first()
            agentsInBranch = db.session.query(Agents).filter(Agents.branchID == lastAgent.branchID)
            branchIncomeTotal = 0
            branchAgentTotal = 0
            for x in agentsInBranch:
                branchIncomeTotal += x.incomeLastYear
                branchAgentTotal += 1
            #print(branchIncomeTotal)
            selectedBranch = Branches.query.get(lastAgent.branchID)
            #print(selectedBranch)
            selectedBranch.averageIncome = branchIncomeTotal/branchAgentTotal
            #print(selectedBranch)




    # Buyers
        elif x <= int((3*amount)/5):
            user = User(id=x, username=userName, email=email, password=hashed_password, userRole=2)
            #print(user)
            db.session.add(user)
            buyer = Buyers(buyerID = x, userID=x, buyerName = firstName + ' ' + lastName, email = email, phoneNumber=randint(1000000000, 9999999999), budget= randint(1, 500000),
                           agentID = randint(int(amount/5), int((2*amount)/5)), lfSqft = randint(1, 10000),
                           lfBedrooms = randint(1, 15), lfBathrooms = randint(1, 15), lfCity = random.choice(cityNames))
            #print(buyer)
            db.session.add(buyer)
            db.session.commit()

    # Sellers
        elif x <= int((4*amount)/5):
            user = User(id=x, username=userName, email=email, password=hashed_password, userRole=3)
            #print(user)
            db.session.add(user)
            seller = Sellers(sellerID = x, userID=x, sellerName=firstName + ' ' + lastName, phoneNumber=randint(1000000000, 9999999999), houseID=x,
                             agentID = randint(int(amount/5), int((2*amount)/5)))
            #print(seller)
            db.session.add(seller)
            db.session.commit()

    # Managers
        elif x <= amount:
            user = User(id=x, username=userName, email=email, password=hashed_password, userRole=5)
            #print(user)
            db.session.add(user)
            manager = Managers(managerID = x, userID=x, managerName = firstName + ' ' + lastName, phoneNumber=randint(1000000000, 9999999999))
            #print(manager)
            db.session.add(manager)
            db.session.commit()

    print("Added all users.")


def createTables():
    db.create_all()
    print("Tables have been created.")

def empty():
    db.drop_all()

def addThings(amount):
    addRoles()
    addBranches()
    addHouses(amount)
    addUsers(amount)

def main():
    empty()
    createTables()
    addThings(200)


main()

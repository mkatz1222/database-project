from datetime import datetime
from RealestateSite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    userRole = db.Column(db.Integer, db.ForeignKey('roles.roleID'))
    userFavorites = db.relationship('Favorites', cascade="all,delete", backref='favorites', lazy=True)
    agentUser = db.relationship("Agents", backref="user")
    managerUser = db.relationship("Managers", backref="user")
    buyerUser = db.relationship("Buyers", backref="user")
    sellerUser = db.relationship("Sellers", backref="user")

    def __repr__(self):
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.userRole}')"

    def agentView(self):
        agentView = User.query.filter(username = User.username, email = User.email)
        return agentView

    def managerView(self):
        managerView = User.query.all()
        return managerView

class Agents(db.Model):
    __tablename__ = 'agents'
    agentID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    agentName = db.Column(db.String(30))
    branchID = db.Column(db.Integer, db.ForeignKey('branches.branchID'), nullable=False)
    incomeLastYear = db.Column(db.Integer)
    phoneNumber = db.Column(db.String(20))
    buyingClients = db.relationship("Buyers", cascade="all,delete", backref="agent")
    sellingClients = db.relationship("Sellers", cascade="all,delete", backref="agent")


    def __repr__(self):
        return f"Agents('{self.agentID}', '{self.agentName}', '{self.branchID}', '{self.incomeLastYear}', '{self.phoneNumber}')"

    def clientView(self):
        clientView = db.session.query(Agents.agentName, Agents.phoneNumber, Branches.city).join(
            Agents).filter(Branches.branchID == Agents.branchID)
        return clientView

    def agentView(self):
        agentView = db.session.query(Agents.agentName, Agents.phoneNumber, Branches.city).join(
            Agents).filter(Branches.branchID == Agents.branchID)
        return agentView

    def managerView(self):
        managerView = db.session.query(Agents.agentName, Agents.phoneNumber, Agents.agentID, Agents.branchID,
                                     Agents.incomeLastYear, Branches.city).join(
                                     Agents).filter(Branches.branchID == Agents.branchID)
        return managerView

class Managers(db.Model):
    managerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    managerName = db.Column(db.String(20))
    phoneNumber = db.Column(db.String(20))

    def __repr__(self):
        return f"Managers('{self.managerID}', '{self.managerName}', '{self.phoneNumber}')"

class Buyers(db.Model):
    buyerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    buyerName = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(20), nullable=False)
    phoneNumber = db.Column(db.String(20), nullable=True)
    budget = db.Column(db.Integer, nullable=True)
    agentID = db.Column(db.Integer, db.ForeignKey('agents.agentID'), nullable=False)
    lfSqft = db.Column(db.Integer, nullable=True)
    lfBedrooms = db.Column(db.Integer, nullable=True)
    lfBathrooms = db.Column(db.Integer,nullable=True)
    lfCity = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"Buyers('{self.buyerID}', '{self.buyerName}', '{self.email}', '{self.budget}', '{self.agentID}'" \
               f", '{self.lfSqft}', '{self.lfBedrooms}', '{self.lfBathrooms}', '{self.lfCity}')"


class Sellers(db.Model):
    sellerID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    sellerName = db.Column(db.String(20))
    phoneNumber = db.Column(db.String(20))
    houseID = db.Column(db.Integer, db.ForeignKey('houses.houseID'), nullable=False)
    agentID = db.Column(db.Integer, db.ForeignKey('agents.agentID'), nullable=False)

    def __repr__(self):
        return f"Sellers('{self.sellerID}', '{self.phoneNumber}', '{self.houseID}', '{self.agentID}')"


class Branches(db.Model):
    branchID = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String, nullable=False)
    averageIncome = db.Column(db.Integer, nullable=True)
    agents = db.relationship("Agents", cascade="all,delete", backref="AssignedBranch", lazy=True)


    def __repr__(self):
        return f"Branches('{self.city}', '{self.branchID}', '{self.averageIncome}')"


class Houses(db.Model):
    houseID = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    saleStatus = db.Column(db.Boolean, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    numberBedrooms = db.Column(db.Integer, nullable=False)
    numberBathrooms = db.Column(db.Integer, nullable=False)
    sizeSqft = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(50), unique=True, nullable=False)
    city = db.Column(db.String(25), nullable=False)
    canTour = db.Column(db.Boolean, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    fencedYard = db.Column(db.Integer, nullable=False)
    pool = db.Column(db.Integer, nullable=False)
    favorite = db.relationship('Favorites', cascade="all,delete", backref='houses')
    owner = db.relationship('Sellers', cascade="all,delete", backref='houses')


    def __repr__(self):
        return f"Houses('{self.houseID}', '{self.saleStatus}', '{self.price}', '{self.numberBedrooms}', '{self.numberBathrooms}', " \
               f"'{self.sizeSqft}', '{self.address}', '{self.city}', '{self.canTour}' , '{self.age}', " \
               f"'{self.fencedYard}', '{self.pool}')"


class Favorites(db.Model):
    favoriteID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    houseID = db.Column(db.Integer, db.ForeignKey('houses.houseID'), nullable=False)

    def __repr__(self):
        return f"Favorites('{self.userID}', '{self.houseID}')"


class Roles(db.Model):
    roleID = db.Column(db.Integer, primary_key=True)
    roleName = db.Column(db.String(20), unique=True)
    users = db.relationship('User', backref='roles')

    def __repr__(self):
        return f"Roles('{self.roleID}'. '{self.roleName}')"

from random import randint
from flask import render_template, url_for, flash, redirect, request, abort
from sqlalchemy import and_, desc, func
from RealestateSite import app, db, bcrypt
from RealestateSite.forms import RegistrationForm, LogInForm, SearchHousesForm, SearchAgentsForm, PostHouseForm, \
    editAccountForm, CompareBranchesForm
from RealestateSite.storedProcedures import nextHighestID, compareBranchesFunction
from RealestateSite.models import User, Houses, Agents, Branches, Buyers, Sellers, Favorites
from flask_login import login_user, current_user, logout_user, login_required
from RealestateSite.testFunctions import nextHighestUserID


@app.route("/")
@app.route("/home")
def home():
    houses = Houses.query.filter().order_by(desc(Houses.date_posted))
    return render_template('home.html', houses=houses)


@app.route("/about")
def about():
    return render_template('about.html', title = "about")


def highestandlowestagent():
    lowestID = db.session.query(func.min(Agents.agentID))
    lowest = lowestID[0]
    lowest = lowest[0]
    highestID = db.session.query(func.max(Agents.agentID))
    highest = highestID[0]
    highest = highest[0]

    list = [lowest, highest]
    return list

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        randomAgent = highestandlowestagent()
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        userID = nextHighestUserID()
        user = User(id = userID, username=form.username.data, email=form.email.data, password=hashed_password, userRole=2)
        buyer = Buyers(buyerID = userID, userID = userID, email = form.email.data, agentID = randint(randomAgent[0], randomAgent[1]))
        try:
            db.session.add(user)
            db.session.add(buyer)
            db.session.commit()
            flash('Your account has been created! You are now able to log in', 'success')
        except:
            db.session.rollback()
            flash('Your account has not been created.', 'fail')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LogInForm()
    agent = Agents.query.first()
    agent = User.query.filter_by(id=agent.userID).first()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form, agent=agent)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/searchHouses", methods=["GET", "POST"])
def searchHouses():
    form = SearchHousesForm()
    executableQuery = 'db.session.query(Houses).filter('
    queryCount = 0
    if request.method == 'POST':
        if form.address.data:
            house = Houses.query.filter(Houses.address == form.address.data)
            return render_template("showHouseSearch.html", houses=house)
        if form.price.data != 'any':
            executableQuery += 'Houses.price <= form.price.data'
            queryCount += 1
            print(executableQuery)
        if form.bedrooms.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.numberBedrooms <= form.bedrooms.data'
            queryCount += 1
            print(executableQuery)
        if form.bathrooms.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.numberBathrooms <= form.bathrooms.data'
            queryCount += 1
            print(executableQuery)
        if form.size.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.sizeSqft <= form.size.data'
            queryCount += 1
            print(executableQuery)
        if form.city.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.city == form.city.data'
            queryCount += 1
            print(executableQuery)
        if form.fence.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.fencedYard == form.fence.data'
            queryCount += 1
            print(executableQuery)
        if form.pool.data != 'any':
            if queryCount > 0:
                executableQuery += ', '
            executableQuery += 'Houses.pool == form.pool.data'
            queryCount += 1
            print(executableQuery)

        executableQuery += ').order_by(desc(Houses.price))'
        print(executableQuery)

        houses = eval(executableQuery)
        total = 0
        for x in houses:
            total += 1
        return render_template("showHouseSearch.html", houses=houses, total=total)
    return render_template('searchHouses.html', title='Search Houses', form=form)


@app.route("/searchAgents", methods=["GET", "POST"])
@login_required
def searchAgents():
    form = SearchAgentsForm()
    if request.method == 'POST':
        if form.agentBranch.data == 'any':
            if current_user.userRole != 5:
                agents = Agents.clientView(db.session).group_by(Agents.branchID)
            else:
                agents = Agents.managerView(db.session).group_by(Agents.branchID)
        else:
            if current_user.userRole != 5:
                agents = db.session.query(Agents.agentName, Agents.phoneNumber, Agents.agentID, Branches.city).join(
                        Agents).filter(and_(Branches.branchID == Agents.branchID, Branches.branchID == form.agentBranch.data))
            else:
                agents = db.session.query(Agents.agentName, Agents.phoneNumber, Agents.agentID, Agents.branchID,
                                     Agents.incomeLastYear, Branches.city).join(
                                    Agents).filter(and_(Branches.branchID == Agents.branchID, Branches.branchID == form.agentBranch.data))
        return render_template("showAgentsSearch.html", agents=agents)
    return render_template('searchAgents.html', title='Search Agents', form=form)


@app.route("/account")
@login_required
def account():
    if current_user.userRole == 1:
        user = User.query.get_or_404(current_user.id)

    elif current_user.userRole == 2:
        user = Buyers.query.get_or_404(current_user.id)
        agent = Agents.query.filter(Agents.agentID == user.agentID).all()
        agentSend = agent[0]
        return render_template('account.html', title='Account', user=user, agent=agentSend)

    elif current_user.userRole == 3:
        user = Sellers.query.get_or_404(current_user.id)
        sellerHouse = Houses.query.filter(Houses.houseID == user.houseID).all()
        agent = Agents.query.filter(Agents.agentID == user.agentID).all()
        agentSend = agent[0]
        houseSend = sellerHouse[0]
        return render_template('account.html', title='Account', user=user, house=houseSend, agent=agentSend)

    elif current_user.userRole == 4:
        user = Agents.query.get_or_404(current_user.id)

    else:
        flash("Error reaching account page.", "fail")
        return redirect(url_for('home'))
    return render_template('account.html', title='Account', user=user)


@app.route("/addfavorite/<int:houseID>", methods=['GET', 'POST'])
@login_required
def addFavorite(houseID):
    userID = current_user.id
    newFavorite = Favorites(favoriteID=None, userID = userID, houseID = houseID)
    db.session.add(newFavorite)
    try:
        db.session.commit()
        flash("Your house has been added to your favorites!", 'success')
    except:
        db.session.rollback()
        flash("Your house was unsuccessfully added to your favorites.", 'fail')
    return redirect(url_for('house', houseID=houseID))


@app.route("/favorites")
@login_required
def favorites():
    favorites = db.session.query(Houses.address, Houses.price, Houses.date_posted, Houses.numberBedrooms,
                                 Houses.numberBathrooms, Favorites.favoriteID).join(Houses).filter(and_(Favorites.houseID == Houses.houseID,
                                                                                  Favorites.userID == current_user.id))
    return render_template('favorites.html', title='Favorites', favorites=favorites)


@app.route("/house/new", methods=['GET', 'POST'])
@login_required
def newHouse():
    form = PostHouseForm()
    if request.method == 'POST':
        newID = nextHighestID()
        house = Houses(houseID = newID, saleStatus=True, price=form.price.data,
                       numberBedrooms=form.bedrooms.data, numberBathrooms=form.bathrooms.data,
                       sizeSqft=form.size.data, address=form.address.data, city=form.city.data,
                       canTour=True, age=form.age.data, fencedYard=form.fence.data,
                       pool=form.pool.data)
        db.session.add(house)
        try:
            db.session.commit()
            flash("Your house has been added!", 'success')
        except:
            db.session.rollback()
            flash("Your house was unsuccessfully added.", 'fail')
        return redirect(url_for('home'))
    return render_template('newHouse.html', title='Add House', form=form, legend='New House')


@app.route("/house/<int:houseID>")
def house(houseID):
    houseDet = Houses.query.get_or_404(houseID)
    return render_template('houseDetails.html', title=houseDet.address, house=houseDet)


@app.route("/house/<int:houseID>/update", methods=['GET', 'POST'])
@login_required
def updateHouse(houseID):
    selectedHouse = Houses.query.get_or_404(houseID)
    if current_user.userRole != 5:
        abort(403)
    form = PostHouseForm()
    if request.method == 'POST':
        selectedHouse.price = form.price.data
        selectedHouse.address = form.address.data
        selectedHouse.numberBedrooms = form.bedrooms.data
        selectedHouse.numberBathrooms = form.bathrooms.data
        selectedHouse.sizeSqft = form.size.data
        selectedHouse.city = form.city.data
        selectedHouse.age = form.age.data
        selectedHouse.fencedYard = form.fence.data
        selectedHouse.pool = form.pool.data
        try:
            db.session.commit()
            print(selectedHouse)
            flash('The selected house has been updated.', 'success')
            return redirect(url_for('house', houseID=houseID))
        except:
            db.session.rollback()
            flash('The selected house has been updated.', 'fail')

        return redirect(url_for('house', houseID=houseID))
    elif request.method == 'GET':
        form.price.data = selectedHouse.price
        form.address.data = selectedHouse.address
        form.bedrooms.data = selectedHouse.numberBedrooms
        form.bathrooms.data = selectedHouse.numberBathrooms
        form.size.data = selectedHouse.sizeSqft
        form.city.data = selectedHouse.city
        form.age.data = selectedHouse.age
        form.fence.data = selectedHouse.fencedYard
        form.pool.data = selectedHouse.pool

    return render_template('newHouse.html', title='Update House', form=form, legend='Update House')


@app.route("/account/<int:buyerID>/edit", methods=['GET', 'POST'])
@login_required
def editAccount(buyerID):
    selectedBuyer = Buyers.query.get_or_404(buyerID)

    form = editAccountForm()
    if request.method == 'POST':
        selectedBuyer.phoneNumber = form.phoneNumber.data
        selectedBuyer.buyerName = form.buyerName.data
        selectedBuyer.budget = form.budget.data
        selectedBuyer.lfSqft = form.lfSqft.data
        selectedBuyer.lfBedrooms = form.lfBedrooms.data
        selectedBuyer.lfBathrooms = form.lfBathrooms.data
        selectedBuyer.lfCity = form.lfCity.data
        try:
            db.session.commit()
            print(selectedBuyer)
            flash('Your account has been updated.', 'success')
            return redirect(url_for('account', buyer=selectedBuyer))
        except:
            db.session.rollback()
            flash('Your account failed to update', 'fail')

        return redirect(url_for('account', buyerID=buyerID))
    elif request.method == 'GET':
        form.phoneNumber.data =  selectedBuyer.phoneNumber
        form.buyerName.data = selectedBuyer.buyerName
        form.budget.data = selectedBuyer.budget
        form.lfSqft.data = selectedBuyer.lfSqft
        form.lfBedrooms.data = selectedBuyer.lfBedrooms
        form.lfBathrooms.data = selectedBuyer.lfBathrooms
        form.lfCity.data = selectedBuyer.lfCity


    return render_template('editAccount.html', title='Edit Account', form=form, legend='Edit Account')


@app.route("/house/<int:houseID>/delete", methods=['POST'])
@login_required
def deleteHouse(houseID):
    selectedHouse = Houses.query.get_or_404(houseID)
    print(houseID)
    if current_user.userRole != 5:
        abort(403)

    Houses.query.filter(Houses.houseID == houseID).delete()

    try:
        db.session.commit()
        flash('The selected house has been deleted.', 'success')
    except:
        flash('The selected house was unsuccessfully deleted.', 'fail')
        db.session.rollback()

    return redirect(url_for('home'))


@app.route("/showAgentsSearch/<int:agentID>/delete", methods=['POST'])
@login_required
def deleteAgent(agentID):
    selectedAgent = Agents.query.get_or_404(agentID)
    print(agentID)
    if current_user.userRole != 5:
        abort(403)

    Agents.query.filter(Agents.agentID == agentID).delete()

    try:
        db.session.commit()
        flash('The selected agent has been deleted.', 'success')
    except:
        flash('The selected agent was unsuccessfully deleted.', 'fail')
        db.session.rollback()

    return redirect(url_for('home'))


@app.route("/")
@app.route("/viewClients")
def viewClients():
    if current_user.userRole != 4:
        abort(403)

    # sellers = Sellers.query.filter(Sellers.agentID == current_user.id).all()
    sellers = db.session.query(Sellers.sellerName, Sellers.phoneNumber, Houses.address).join(
        Sellers).filter(and_(Houses.houseID == Sellers.houseID, Sellers.agentID == current_user.id))
    buyers = Buyers.query.filter(Buyers.agentID == current_user.id).all()
    return render_template('viewClients.html', sellers=sellers, buyers=buyers)



@app.route("/compareBranches",   methods=['GET', 'POST'])
def compareBranches():
    form = CompareBranchesForm()
    if request.method == 'POST':
        print(form.branchOne.data)
        print(form.branchTwo.data)
        results = compareBranchesFunction(form.branchOne.data, form.branchTwo.data)
        winner = results[0]

        loser = results[1]
        return render_template('compareBranchesResults.html', winner=winner, loser=loser)
    return render_template('compareBranches.html', form=form)




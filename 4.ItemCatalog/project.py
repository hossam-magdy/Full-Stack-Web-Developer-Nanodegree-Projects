# to enable import @ running via apache2
import os, sys
PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, PROJECT_ROOT)

from flask import (
    Flask,
    render_template,
    request,
    make_response,
    redirect,
    jsonify,
    url_for,
    flash,
    session as login_session
)
from functools import wraps # for "login_required" view decorator function

from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import random, string, httplib2, json, requests

from flask_sqlalchemy import SQLAlchemy # to avoid error: SQLite objects created in a thread can only be used in that same thread
from dbSetup import Category, Item, User

#from sqlalchemy import create_engine, asc
#from sqlalchemy.orm import sessionmaker
#from dbSetup import Base, Category, Item, User
#Connect to db and create db session (use full path not relative for apache2)
#engine = create_engine('sqlite:///{}'.format(os.path.join(PROJECT_ROOT, 'itemCatalog.db')))
#Base.metadata.bind = engine
#DBSession = sessionmaker(bind=engine)
#session = DBSession()

app = Flask(__name__)
app.secret_key = 'super_secret_key'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(PROJECT_ROOT, 'itemCatalog.db'))
db = SQLAlchemy(app)
session = db.session

################################################################################
################################################################# UserHelper fns
################################################################################

def loggedIn(in_session):
    if 'user_id' in in_session:
        return in_session['user_id']
    return None
# To be able to call it from a template
# http://www.radhakapoor.net/flask-calling-a-python-function-from-jinga-template/
app.jinja_env.globals.update(loggedIn=loggedIn)

#http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        #if g.user is None:
        if not loggedIn(login_session):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# User Helper Functions
def createUser(data):
    newUser = User(id_at_provider=data['id_at_provider'], name=data['name'], email=data['email'], picture=data['picture'])
    session.add(newUser)
    session.commit()
    #user = session.query(User).filter_by(email=login_session['email']).first()
    return newUser

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).first()
    return user

def getUserID(id_at_provider):
    try:
        user = session.query(User).filter_by(id_at_provider=id_at_provider).first()
        return user.id
    except:
        return None

################################################################################
################################################################# User LogInOut
################################################################################

@app.route('/connect', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if loggedIn(login_session):
            flash("You are already logged in.")
            return redirect("/")
        state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
        login_session['state'] = state
        return render_template('login.html', STATE=state)
    elif request.method == 'POST':
        state = request.form.get('state')
        provider = request.form.get('provider')
        access_token = request.form.get('access_token')

        if state != login_session['state']:
            response = make_response(json.dumps('Invalid state parameter.'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response

        try:
            login_session['provider'] = provider
            login_session['access_token'] = access_token
            if provider=="google":
                url = "https://www.googleapis.com/oauth2/v1/userinfo"
                params = {'access_token': access_token, 'alt': 'json'}
                answer = requests.get(url, params=params) #answer.raise_for_status()
                if answer.status_code != 200:
                    raise Exception(answer.get('status_code'))
                data = json.loads(answer.content) #answer.json() #(doesn't work with facebook)
                if not 'id' in data:
                    raise Exception("Could not define user @ provider")
                #return make_response(json.dumps(data), 500)
                login_session['id_at_provider'] = '{}:{}'.format(provider, data['id'])
                login_session['email'] = data.get('email', '')
                login_session['name'] = data.get('name', login_session['id_at_provider'])
                login_session['picture'] = data.get('picture', '')
            elif provider=="facebook":
                url = "https://graph.facebook.com/v2.9/me"
                params = {'access_token': access_token, 'fields': 'id, name, email, picture'}
                answer = requests.get(url, params=params) #answer.raise_for_status()
                if answer.status_code != 200:
                    raise Exception(answer.get('status_code'))
                data = json.loads(answer.content)
                if not 'id' in data:
                    raise Exception("Could not define user @ provider")
                #return make_response(json.dumps(data), 500)
                login_session['id_at_provider'] = '{}:{}'.format(provider, data['id'])
                login_session['email'] = data.get('email', '')
                login_session['name'] = data.get('name', '')
                if 'picture' in data and 'data' in data['picture'] and 'url' in data['picture']['data']:
                    login_session['picture'] = data['picture']['data']['url']
                else:
                    login_session['picture'] = ''
                #url = 'https://graph.facebook.com/v2.4/me/picture?access_token=%s&&redirect=0&height=200&width=200' % token
        except Exception as e:
            err = 'Connection with provider ({}) failed: {}'.format(provider, e)
            print err
            return make_response(json.dumps(err), 500)

        user_id = getUserID(login_session['id_at_provider'])
        if user_id:
            user = getUserInfo(user_id)
            user.name = login_session.get('name', '')
            user.email = login_session.get('email', '')
            user.picture = login_session.get('picture', '')
            session.commit()
        else:
            user = createUser(login_session)
            user_id = user.id

        login_session['user_id'] = user_id
        #print login_session

        flash("Welcome, {}".format(login_session['name']))
        return make_response(json.dumps('OAuth Connected: {}.'.format(login_session['provider'])), 200)
        #return redirect("/")

@app.route('/disconnect')
@app.route('/logout')
# Disconnect based on provider
def logout():
    if not loggedIn(login_session):
        flash("You were not logged in.")
    else:
        provider = login_session['provider']
        access_token = login_session['access_token']
        if provider=="google":
            url = "https://accounts.google.com/o/oauth2/revoke"
            params = {'token': access_token, 'alt': 'json'}
            answer = requests.get(url, params=params)
            data = json.loads(answer.content) #answer.json() #(doesn't work with facebook)
        elif provider=="facebook":
            url = "https://graph.facebook.com/{}/permissions".format(login_session['id_at_provider'])
            params = {'access_token': access_token, 'fields': 'name,email,picture,id'}
            answer = requests.delete(url, params=params)
            data = json.loads(answer.content)
        flash("You have successfully been logged out.")

    login_session.pop('user_id', None)
    login_session.pop('provider', None)
    login_session.pop('access_token', None)
    login_session.pop('id_at_provider', None)
    login_session.pop('email', None)
    login_session.pop('name', None)
    login_session.pop('picture', None)
    #print login_session

    #return make_response(json.dumps('OAuth Disonnected.'), 200)
    return redirect("/")

################################################################################
################################################################# Main
################################################################################

@app.route('/')
def main():
    Categories = session.query(Category).order_by(Category.name.asc())#.limit(10)
    LatestItems = session.query(Item).order_by(Item.id.desc()).limit(10)
    return render_template('main.html', Categories = Categories, LatestItems = LatestItems)

################################################################################
################################################################# CRUD: Category
################################################################################

@app.route('/catalog/<path:cat_name>')
def showCat(cat_name):
    cat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    if not cat:
        flash("Category not found", "error")
        return redirect(url_for('main'))
    items = session.query(Item).filter_by(cat_id = cat.id).order_by(Item.id.desc()).all()
    return render_template('catShow.html', cat = cat, items = items)

@app.route('/catalog/new', methods=['GET','POST'])
@login_required
def newCat():
    if request.method == 'POST':
        newCategory = Category(user_id = login_session['user_id'], name = request.form['name'])
        if not request.form['name']:
            flash("Category must have a name", "error")
            return render_template('catCreateUpdate.html')
        session.add(newCategory)
        session.commit()
        flash("Category ({}) Successfully Created".format(newCategory.name), "success")
        return redirect(url_for('showCat', cat_name=newCategory.name))
    else:
        return render_template('catCreateUpdate.html')

@app.route('/catalog/<path:cat_name>/edit', methods=['GET','POST'])
@login_required
def editCat(cat_name):
    editCat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    if not editCat:
        flash("Category not found", "error")
        return redirect(url_for('main'))
    if editCat.user_id != loggedIn(login_session):
        flash("You are not the owner of this category", "error")
        return redirect(url_for('main'))
    if request.method == 'POST':
        if not request.form['name']:
            flash("Category must have a name".format(newCategory.name), "error")
            return render_template('catCreateUpdate.html', editCat = editCat)
        editCat.name = request.form['name']
        session.commit()
        flash("Category ({}) Successfully Updated".format(editCat.name), "success")
        return redirect(url_for('main'))
    else:
        return render_template('catCreateUpdate.html', editCat = editCat)

@app.route('/catalog/<path:cat_name>/delete', methods=['GET','POST'])
@login_required
def deleteCat(cat_name):
    catToDelete = session.query(Category).filter_by(name = cat_name).limit(1).first()
    if not catToDelete:
        flash("Category not found", "error")
        return redirect(url_for('main'))
    if catToDelete.user_id != loggedIn(login_session):
        flash("You are not the owner of this category", "error")
        return redirect(url_for('showCat', cat_name=catToDelete.id))
    if request.method == 'POST':
        session.query(Item).filter_by(cat_id = catToDelete.id).delete()
        session.delete(catToDelete)
        session.commit()
        flash("Category ({}) Successfully Deleted".format(cat_name), "success")
        return redirect(url_for('main'))
    else:
        return render_template('catDelete.html', catToDelete = catToDelete)

################################################################################
################################################################# CRUD: Item
################################################################################

@app.route('/catalog/<path:cat_name>/<path:item_name>')
def showItem(cat_name, item_name):
    cat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    item = session.query(Item).filter_by(name = item_name).limit(1).first()
    #print cat.id
    #print item.cat_id
    if not item:
        flash("Item is not found", "error")
        return redirect(url_for('main'))
    if not cat or item.cat_id != cat.id:
        flash("Redirected, the URI was wrong")
        cat = session.query(Category).filter_by(id = item.cat_id).limit(1).first()
        return redirect(url_for('showItem', cat_name=cat.name, item_name=item.name))
    #item.description = item.description.replace("\n", "<br>\n")
    #print
    return render_template('itemShow.html', cat = cat, item = item)

@app.route('/catalog/<path:cat_name>/new', methods=['GET','POST'])
@login_required
def newItem(cat_name):
    cat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    if not cat:
        flash("Category not found", "error")
        return redirect(url_for('main'))
    if request.method == 'POST':
        if not request.form['name']:
            flash("Item must have a name", "error")
            return render_template('itemCreateUpdate.html')
        newItem = Item(user_id = login_session['user_id'], cat_id = cat.id, name = request.form['name'], description = request.form['description'])
        session.add(newItem)
        session.commit()
        flash("Item ({}) Successfully Created".format(newItem.name), "success")
        return redirect(url_for('showItem', cat_name=cat.name, item_name=newItem.name))
    else:
        return render_template('itemCreateUpdate.html')

@app.route('/catalog/<path:cat_name>/<path:item_name>/edit', methods=['GET','POST'])
@login_required
def editItem(cat_name, item_name):
    item = session.query(Item).filter_by(name = item_name).limit(1).first()
    cat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    #print item.user_id
    #print loggedIn(login_session)
    if not item:
        flash("Item not found", "error")
        return redirect(url_for('showCat', cat_name=cat.name))
    if not cat or item.cat_id != cat.id:
        flash("Redirected, the URI was wrong")
        cat = session.query(Category).filter_by(id = item.cat_id).limit(1).first()
        return redirect(url_for('editItem', cat_name=cat.name, item_name=item.name))
    if item.user_id != loggedIn(login_session):
        flash("You are not the owner of this item", "error")
        return redirect(url_for('showCat', cat_name=cat.name))
    if request.method == 'POST':
        if not request.form['name']:
            flash("Item must have a name", "error")
            return render_template('itemCreateUpdate.html', editItem = item)
        item.name = request.form['name']
        item.description = request.form['description']
        session.commit()
        flash("Item ({}) Successfully Updated".format(item.name), "success")
        return redirect(url_for('showItem', cat_name=item.cat.name, item_name=item.name))
    else:
        return render_template('itemCreateUpdate.html', editItem = item)

@app.route('/catalog/<path:cat_name>/<path:item_name>/delete', methods=['GET','POST'])
@login_required
def deleteItem(cat_name, item_name):
    item = session.query(Item).filter_by(name = item_name).limit(1).first()
    cat = session.query(Category).filter_by(name = cat_name).limit(1).first()
    if not item:
        flash("Item not found", "error")
        return redirect(url_for('showCat', cat_name=cat.name))
    if not cat or item.cat_id != cat.id:
        flash("Redirected, the URI was wrong")
        cat = session.query(Category).filter_by(id = editItem.cat_id).limit(1).first()
        return redirect(url_for('deleteItem', cat_name=cat.name, item_name=item.name))
    if item.user_id != loggedIn(login_session):
        flash("You are not the owner of this item", "error")
        return redirect(url_for('showCat', cat_name=cat.name))
    if request.method == 'POST':
        session.delete(item)
        session.commit()
        flash("Item ({}) Successfully Deleted".format(item_name))
        return redirect(url_for('showCat', cat_name = cat_name))
    else:
        return render_template('itemDelete.html', itemToDelete = item)

################################################################################
################################################################# JSON
################################################################################

@app.route('/catalog.json')
def JSON():
    cats = session.query(Category)
    ##return jsonify(Category=[i.serialize for i in cats])
    result = {"Category":[]}
    for i in cats:
        ##print prepareCat(i)
        ##x = i.serialize()
        result["Category"].append(prepareCat(i))
    ##items = session.query(Item).filter_by(category_id = category_id).all()
    return jsonify(result)

# Helper function to return dict of category with all its items
def prepareCat(cat):
    out = {
        'id'    : cat.id,
        'name'  : cat.name,
        'item'  : []
        }
    items = session.query(Item).filter_by(cat_id = cat.id).all()
    out['item'] = [i.serialize for i in items]
    return out

################################################################################
################################################################# Server
################################################################################

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 5000)


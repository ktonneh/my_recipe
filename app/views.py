from app import app
from flask import redirect, request, render_template, url_for, session, flash, render_template
from .forms import LoginForm, RegisterForm
from .models import User

database_users = {}
# {
# 'denno': {'passwword': '55', 'email': 'denno@yahoo.com'},
# 'tonny': {'passwword': '22', 'email': 'tonny@yahoo.com'},
# 'vee': {'passwword': '22', 'email': 'tonny@yahoo.com'}
# }
#
# database_users['vee']
# database_users['vee']['password']
# database_users['vee']['email']


recipe_list_items = []

recipe_categories = []


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', title='Register')

    if request.method == 'POST':
        id = len(database_users)+1;
        user = User(id,request.form.get('name'),request.form.get('username'),
                    request.form.get('email'), request.form.get('password'))
        # user.email = request.form.get('email')
        # user.username = request.form.get('username')
        # user.password = request.form.get('password')
        confirm_password = request.form.get('cpassword')
        print('Form submitted her')
        print(confirm_password)
    if user.password != confirm_password:
        return redirect('/register')

    print('User Object')
    print(user)

    database_users[user.username] = user.__dict__
    # session['username'] = username
    print('User Added$$')
    print(database_users)
    print(database_users[user.username]['email'])
    print('redirect to login!!')
    return redirect('/login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('index.html', form=form, title='Login')

    if request.method == 'POST':
        user = User(request.form.get('username'),request.form.get('password'))
        print('Entered from form##')
        print(user.username)
        print(user.password)

        print('Db Users##')
        print(database_users)

        try:
            print(database_users[user.username])
        except KeyError:
            print('No Users found')
            # flash('Invalid username, please try again!!')

        try:
            print(database_users[user.username]['password'])
        except KeyError:
            print('No Users Password found')
            # flash('Invalid password, Please try again!!')

        try:
            if database_users[user.username] and database_users[user.username]['password'] == user.password:
                session['username'] = user.username
                return redirect(url_for('recipecategorylist'))
            else:
                # flash('Invalid username or password, please try again!!')
                return redirect(url_for('login'))

        except (KeyError, ValueError):
            flash('Invalid username or password, please try again!!')
            return redirect(url_for('index'))


@app.route("/recipe_itemlist")
def recipe_itemlist():
    return render_template('recipe_itemlist.html')


@app.route('/add_recipeitem', methods=['GET', 'POST'])
def add_recipeitem():
    id = request.args.get('id')
    usern = session['username']
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        category = request.form.get('category')
        user = session['username']
        id = len(recipe_list_items) + 1
        category_item = {'id': id, "name": name, "description": description, "user": user, "category": category}
        recipe_list_items.append(category_item)
        print('Catgory##')
        print(category)
        category_index_to_view = int(category) - 1
        category_to_view = recipe_categories[category_index_to_view]
        recipeitems_to_view = []
        for item in recipe_list_items:
            if item['user'] == str(usern) and item['category'] == category:
                recipeitems_to_view.append(item)

        return render_template('recipe_itemlist.html', title='Item List',
                                       category_list_itemss=recipeitems_to_view, category=category_to_view)

    return render_template('add_recipeitem.html', title='add item', category=id)


@app.route('/add_recipecategory')
def addrecipecategory():
    return render_template('add_recipecategory.html')


@app.route('/save_category', methods=['POST'])
def savecategory():
    user = session['username']
    print(user)
    name = request.form.get('recipename')
    description = request.form.get('description')
    print(name)
    id = len(recipe_categories) + 1
    category = {"id": id, "name": name, "description": description, "user": user}
    recipe_categories.append(category)
    return redirect('/recipecategorylist')


@app.route('/recipecategorylist')
def recipecategorylist():
    uname = session['username']
    user_recipecategory = []
    for category in recipe_categories:
        if category['user'] == str(uname):
            user_recipecategory.append(category)
    else:
        return render_template('recipe_categorylist.html', title='Recipe Category List',
                               category_items=user_recipecategory)


@app.route('/viewitems')
def view_recipeitems():
    id = request.args.get('id')
    uname = session['username']
    if id == None:
        return redirect('/recipecategorylist')

    print('Item Values##')
    print(uname)
    print(id)

    category_index_to_view = int(id) - 1
    category_to_view = recipe_categories[category_index_to_view]
    print(category_to_view)
    recipeitems_to_view = []
    for item in recipe_list_items:
        if item['user'] == str(uname) and item['category'] == id:
            recipeitems_to_view.append(item)

    return render_template('recipe_itemlist.html', title=' Recipe Item List',
                                   category_list_itemss=recipeitems_to_view, category=category_to_view)


@app.route('/editcategory')
def edit_category():
    id = request.args.get('id')
    if id == None:
        return redirect('/recipecategorylist')
    index_to_edit = int(id) - 1
    category_to_edit = recipe_categories[index_to_edit]
    return render_template('edit_category.html', category=category_to_edit)


@app.route('/update_category', methods=['POST'])
def update_category():
    uname = session['username']
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        description = request.form.get('description')
        user = session['username']
        
        for item_to_update in recipe_categories:
            if item_to_update['id'] == int(id):
                item_to_update['name'] = name
                item_to_update['description'] = description
                break
        categories_to_view = []
        for item in recipe_categories:
            if item['user'] == str(uname):
                categories_to_view.append(item)
            else:
                return render_template('recipe_categorylist.html', title='Recipe List',
                                       category_items=categories_to_view)


@app.route('/logout')
def logout():
    session['username'] = ''
    return redirect('/login')

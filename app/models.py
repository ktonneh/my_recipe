class BucketListItem:
    def __init__(self,id,name,description,category,created_by,date):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.createdBy = created_by
        self.date = date


class Category:
    def __init__(self, id, name, description,user):
        self.id = id
        self.name = name
        self.description = description
        self.user = user


class User(object):

    def __init__(self, id, name, username, email, password):
        self.id = id
        self.name = name
        self.username = username
        self.email = email
        self.password = password


    def __init__(self,username,password):
        self.username = username
        self.password = password


### Creating user, fetching users

* Before adding user to the database, you have to hash the password.
* The model representation is done thanks to `__repr__` magic method.

```Python
In [2]: u = User(username='username', email='email@email', first_name='first', last_name='last')

In [3]: u.hash_password('password')

In [4]: db.session.add(u); db.session.commit()

In [5]: User.query.all()
Out[5]:
[1: 'dc' 'dc', 'dc@dc', admin: True,
 2: 'dc' 'dc', 'dc@dc', admin: True,
 3: '' '', '', admin: False,
 4: 'first' 'last', 'email@email', admin: False]
```



### Adding user to group

Through `Group` instance:

```Python
In [1]: g = Group.query.all()[0]

In [2]: g.users
Out[2]: [1: 'dc' 'dc', 'dc@dc', admin: True]

In [3]: g
Out[3]: 1: 'first group'

In [4]: g.users.append(User.query.all()[1])

In [5]: g.users
Out[5]: [1: 'dc' 'dc', 'dc@dc', admin: True, 2: 'dc' 'dc', 'dc@dc', admin: True]

In [6]: db.session.add(g); db.session.commit()
```

Through `User` instance:

```Python
In [2]: u = User.query.all()[3]

In [3]: u.groups
Out[3]: <sqlalchemy.orm.dynamic.AppenderBaseQuery at 0x7f989ef50fd0>

In [4]: u
Out[4]: 4: 'first' 'last', 'email@email', admin: False

In [6]: u.groups.all()
Out[6]: []

In [7]: u.groups.append(Group.query.all()[0])

In [8]: u.groups.all()
Out[8]: [1: 'first group']

In [9]: db.session.add(u); db.session.commit()

In [11]: User.query.all()[3].groups.all()
Out[11]: [1: 'first group']
```
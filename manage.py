import sys
import database


def print_usage():
    print('Incorrect number of arguments.')
    print('Script can be invoked like:')
    print('  ~:$ python3 manage.py adduser username:password')
    print('  ~:$ python3 manage.py userdel username:password')
    print('  ~:$ python3 manage.py getusers')
    print('  ~:$ python3 manage.py load_default')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'load_default':
        connection = database.connect()
        for table_name in 'users', 'tasks':
            database.drop_table(connection, table_name)
            database.create_table(connection, table_name)
            database.load_default(connection, table_name)
        connection.close()
    elif len(sys.argv) == 2 and sys.argv[1] == 'getusers':
        connection = database.connect()
        for user, password in database.get_user_credentials(connection):
            print('user:password -> {0}:{1}'.format(user, password))
        connection.close()
    elif len(sys.argv) == 3 and sys.argv[1] == 'adduser':
        connection = database.connect()
        database.insert_user(connection, sys.argv[2])
        connection.close()
    elif len(sys.argv) == 3 and sys.argv[1] == 'userdel':
        connection = database.connect()
        database.delete_user(connection, sys.argv[2])
        connection.close()
    else:
        print_usage()
        sys.exit(1)



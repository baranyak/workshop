import sqlite3
import config


def insert_user(connection, credentials):
    """
    Insert user in to the 'users' table. On error raise exceptions.
    :param connection: sqlite connection to the database
    :param credentials: user credentials in format username:password
    """
    if len(credentials.split(':')) == 2 and not credentials.startswith(':')\
            and not credentials.endswith(':'):
        username, password = credentials.split(':')
        if username in [cred[0] for cred in get_user_credentials(connection)]:
            raise Exception('Failed to add "{}" user. User already exists.'
                            .format(username))
        else:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users VALUES(?,?)',
                           (username, password))
            connection.commit()
            print('Successfully added "{}" user.'.format(username))
    else:
        raise Exception('Failed to add "{}" user.'.format(credentials))


def delete_user(connection, credentials):
    if len(credentials.split(':')) == 2 \
            and tuple(credentials.split(':')) in get_user_credentials(connection):
        username, password = credentials.split(':')
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE name=? and password=?',
                       (username, password))
        connection.commit()
        print('Successfully deleted "{}" user.'.format(username))
    else:
        raise Exception('Failed to delete "{}" user.'.format(credentials))


def get_user_credentials(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT name, password FROM users')
    connection.commit()
    return cursor.fetchall()


def connect():
    # Need to create database.db first
    return sqlite3.connect(config.CURRENT_DIR + "/database.db",
                           check_same_thread=False)


def drop_table(connection, table_name):
    cursor = connection.cursor()
    try:
        cursor.execute('DROP TABLE {}'.format(table_name))
        print('Successfully droped "{}" table.'.format(table_name))
    except Exception:
        print('Failed to drop "{}" table.'.format(table_name))
    connection.commit()


def create_table(connection, table_name):
    cursor = connection.cursor()
    if table_name == 'users':
        cursor.execute('CREATE TABLE users ('
                       'name text NOT NULL UNIQUE,'
                       'password text NOT NULL)')
        print('Successfully created "users" table.')
    elif table_name == 'tasks':
        cursor.execute('CREATE TABLE tasks ('
                       'id INTEGER PRIMARY KEY,'
                       'title text NOT NULL,'
                       'description text NOT NULL,'
                       'status text NOT NULL)')
        print('Successfully created "tasks" table.')
    else:
        print('Failed to create "{}" table.'.format(table_name))
    connection.commit()


def create_task(connection, task):
    if None not in (task.get('title'), task.get('description'),
                    task.get('status')):
        cursor = connection.cursor()
        cursor.execute(
            'INSERT INTO tasks (title, description, status) VALUES(?,?,?)',
            (task.get('title'), task.get('description'), task.get('status')))
        connection.commit()
        print('Successfully added "{}" task.'.format(task.get('title')))
    else:
        Exception('Failed to added "{}" task.'.format(task.get('title')))


def get_tasks(connection):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks')
    connection.commit()
    return [dict(zip(('id', 'title', 'description', 'status'), task))
            for task in cursor.fetchall()]


def get_task(connection, task_id):
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM tasks WHERE id=?', (task_id,))
    connection.commit()
    return [dict(zip(('id', 'title', 'description', 'status'), task))
            for task in cursor.fetchall()]


def update_task(connection, task):
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE tasks SET title=?, description=?, status=? WHERE id=?',
        (task['title'], task['description'], task['status'], task['id']))
    connection.commit()


def delete_task(connection, task_id):
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tasks WHERE id=?', (task_id,))
    connection.commit()


def load_default(connection, table_name):
    if table_name == 'users':
        for credential in config.credentials:
            insert_user(connection, credential)
    elif table_name == 'tasks':
        for task in config.tasks:
            create_task(connection, task)
    else:
        print('Failed to load "{}" table with default values.'
              .format(table_name))




if __name__ == '__main__':
    conn = connect()
    drop_table(conn, 'tasks')
    create_table(conn, 'tasks')
    load_default(conn, 'tasks')
    print(get_tasks(conn))


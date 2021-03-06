#!/usr/bin/env python
import sys, sqlite3, os, subprocess

import utils

# Open Connection
mydirs_directory = os.environ['CONTEXTUAL_ALIASES_DIR'] + '/db/'
conn = sqlite3.connect(mydirs_directory + 'contextual.sqlite')

# Creating cursor
c = conn.cursor()

def create_tables():
    # Create table
    c.execute('''
        CREATE TABLE IF NOT EXISTS ContextualActionsByKey (
            id_context INTEGER,
            path TEXT,
            aliases TEXT,
            contextual_action TEXT,
            PRIMARY KEY (id_context)
        )
    ''')

def show_command(args, extra_args):
    c.execute("SELECT contextual_action FROM ContextualActionsByKey WHERE path LIKE ? AND aliases LIKE ?", (os.getcwd(), sys.argv[2]))
    row = c.fetchone()
    if row is None:
        print 'No contextual action found!'
    else:
        env_str = 'source ' + os.environ['HOME']+'/.profile && '
        contextual_cmd = row[0]
        contextual_cmd = env_str + row[0]
        print(contextual_cmd)

def list_aliases(args, extra_args):
    exec_query = "SELECT aliases FROM ContextualActionsByKey WHERE path LIKE ?  ORDER BY aliases"
    exec_data = (os.getcwd(),)
    c.execute(exec_query, exec_data)
    for row in c:
        print(str(row[0]))

def save_alias(args, extra_args):
    # Get args
    current_path = os.getcwd()
    alias_string = args[0]
    contextual_action = args[1]

    save_data = (current_path, alias_string, contextual_action)

    exec_query = "SELECT contextual_action FROM ContextualActionsByKey WHERE path LIKE ? AND aliases LIKE ?"
    exec_data = (current_path, alias_string)
    c.execute(exec_query, exec_data)
    row = c.fetchone()
    if row is not None:
        print("There already a saved alias in current path")
        print("You should use -u option to update an alias")
        return

    save_query = "INSERT INTO ContextualActionsByKey (path, aliases, contextual_action) " + \
                "VALUES (:path, :aliases, :contextual_action)"
    
    c.execute(save_query, save_data)
    conn.commit()
    # TODO: Check if alias was really saved
    print('Alias Saved')

def exec_alias(args, extra_args):
    exec_query = "SELECT contextual_action FROM ContextualActionsByKey WHERE path LIKE ? AND aliases LIKE ?"
    exec_data = (os.getcwd(), args[0])
    c.execute(exec_query, exec_data)
    row = c.fetchone()
    if row is None:
        print 'No contextual action found!'
    else:
        env_str = 'source ' + os.environ['HOME']+'/.profile && '
        contextual_cmd = row[0]
        print("Contextual action: " + contextual_cmd + '\n')
        contextual_cmd = env_str + row[0]
        # cmd_output = subprocess.check_output(contextual_cmd, shell=True, executable='/bin/bash')
        # print cmd_output
        process = subprocess.Popen(contextual_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/bash')
        while True:
            out = process.stdout.read(1)
            if out == '' and process.poll() != None:
                break
            if out != '':
                sys.stdout.write(out)
                sys.stdout.flush()

def delete_alias(args, extra_args):
    alias_to_delete = args[0]
    path_alias_to_delete = os.getcwd()

    sql_query_delete = "DELETE FROM ContextualActionsByKey WHERE path LIKE ? AND aliases LIKE ?"
    delete_data = (path_alias_to_delete, alias_to_delete)
    c.execute(sql_query_delete, delete_data)
    conn.commit()

    print('Deleted alias!')

def update_aliases(args, extra_args):
    c.execute("SELECT DISTINCT aliases from ContextualActionsByKey ORDER BY aliases")
    for row in c:
        print(str(row[0]))


commands_parse = {
    '-u'       : update_aliases,
    '-l'       : list_aliases,
    '-s'       : save_alias,
    '-e'       : exec_alias,
    '-c'       : show_command,
    '-d'       : delete_alias,
    '--exec'   : exec_alias,
    '--save'   : save_alias,
    '--update' : update_aliases,
    '--command': show_command,
    '--delete' : delete_alias,
}

def parse_arguments():

    args = {}

    last_key = ''

    for i in xrange(1, len(sys.argv)):
        a = sys.argv[i]
        if a[0] == '-' and not utils.is_float(a):
            last_key = a
            args[a] = []
        elif last_key != '':
            arg_values = args[last_key]
            arg_values.append(a)
            args[last_key] = arg_values

    return args

def parse_commands(args):
    # print('DEBUG: Parsing args: ' + str(args))
    for a in args:
        if a in commands_parse:
            commands_parse[a](args[a], args)

create_tables()
args = parse_arguments()
parse_commands(args)

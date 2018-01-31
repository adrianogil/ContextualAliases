#!/usr/bin/env python
import sys, sqlite3, os, subprocess

list_args = '--save -s --open -o --remove -r --list -l -u --update -f --find -q --current'

# Open Connection
mydirs_directory = os.environ['CONTEXTUAL_ALIASES_DIR'] + '/db/'
conn = sqlite3.connect(mydirs_directory + 'contextual.sqlite');

# Creating cursor
c = conn.cursor()

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

if len(sys.argv) == 4:
    if (sys.argv[1] == '--save' or sys.argv[1] == '-s'):
        # Save current path
        #print "Saving Current Path " + os.getcwd() + " string " + sys.argv[2]
        # dict_path = {":path" : os.getcwd(), ":key": sys.argv[2]}
        #print dict_path
        c.execute("INSERT INTO ContextualActionsByKey (path, aliases, contextual_action) " +
                    "VALUES (:path, :aliases, :contextual_action)",
            (os.getcwd(), sys.argv[2], sys.argv[3]))
        conn.commit()
        print('Saved')
elif len(sys.argv) == 3:
    if (sys.argv[1] == '--exec' or sys.argv[1] == '-e'):
        c.execute("SELECT contextual_action FROM ContextualActionsByKey WHERE path LIKE ? AND aliases LIKE ?", (os.getcwd(), sys.argv[2]))
        row = c.fetchone()
        if row is None:
            print 'No contextual action found!'
        else:
            contextual_cmd = row[0]
            print("Contextual action: " + contextual_cmd + '\n')
            cmd_output = subprocess.check_output(contextual_cmd, shell=True)
            print cmd_output

elif len(sys.argv) == 2:
    if (sys.argv[1] == '--update' or sys.argv[1] == '-u'):
        c.execute("SELECT DISTINCT aliases from ContextualActionsByKey ORDER BY aliases")
        for row in c:
            print(str(row[0]))
            # contextual_aliases="alias "+ str(row[0]) + "='python $CONTEXTUAL_ALIASES_DIR/src/context_aliases.py -e " + str(row[0]) + "'"
            # print(contextual_aliases)
            # cmd_output = subprocess.check_output(contextual_aliases, shell=True)
            # print(cmd_output)

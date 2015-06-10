# Alex Monk, July 2014

import MySQLdb
from ConfigParser import ConfigParser

config = ConfigParser()
config.read('replica.my.cnf')
user = config.get('client', 'user')[1:-1] # Strip first and last characters - just apostrophes
password = config.get('client', 'password')[1:-1] # Strip first and last characters - just apostrophes

def checkDBs():
	cursors = {}
	metaDb = MySQLdb.connect(host = "s1.labsdb", user = user, passwd = password, db = "meta_p")
	metaCursor = metaDb.cursor()
	metaCursor.execute("select dbname, url, slice from wiki where not is_closed and url is not null;")
        cursors["s1.labsdb"] = metaCursor
	for row in metaCursor.fetchall():
	    dbname, url, slice = row
            if slice not in cursors.keys():
		db = MySQLdb.connect(host = dbname + '.labsdb', user = user, passwd = password, db = dbname + "_p")
	        cursor = db.cursor()
                cursors[slice] = cursor
	    else:
	        cursor = cursors[slice]
                cursor.execute("use {};".format(dbname + "_p"))

	    cursor.execute(""" \
		select
			rc_this_oldid
		from
			change_tag, recentchanges
		where
			ct_tag = 'visualeditor-needcheck' and
			ct_rev_id is not null and
			ct_rc_id = rc_id and
			rc_timestamp >= now() - interval 1 day
		;""")
	    for needcheckRow in cursor.fetchall():
	        revid, = needcheckRow
	        yield dbname, url, str(revid)

	for cursor in cursors.values():
		cursor.close()


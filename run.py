# Alex Monk, July 2014

from checkAllDBs import checkDBs
from ircecho import ircecho

msg = ""
for row in checkDBs():
	dbname, url, rev_id = row
	msg += "Corruption alert: visualeditor-needcheck on {}: {}\r\n".format(dbname, url.replace("http:", "https:") + "/?diff=" + rev_id)

if msg:
	ircecho("wm-ve-needcheck", "#mediawiki-visualeditor", msg)

#!/usr/bin/python

import livejournal
import os
import getpass

print 'This will irrevocably delete all entries.  Be very sure.'
lj = livejournal.LJ('evan', getpass.getpass())
itemids = os.listdir('out')
for itemid in itemids:
    if itemid != '1':
        print 'deleting', itemid
        try:
            lj.run('editevent', itemid=itemid, event='')
        except livejournal.ProtocolException, e:
            print e

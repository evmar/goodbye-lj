#!/usr/bin/python

import livejournal
import os
import getpass
import urllib

lj = livejournal.LJ('evan', getpass.getpass(), 'evan_tech')

def dump_entries(dirname, response):
    """Given a getevents response, dump all the entries into files
    named by itemid.
    Return the set of itemids received."""
    all_itemids = set()

    props = {}
    for i in range(1, int(response.get('prop_count', 0)) + 1):
        itemid = response['prop_%d_itemid' % i]
        name   = response['prop_%d_name' % i]
        value  = response['prop_%d_value' % i]
        if itemid not in props:
            props[itemid] = {}
        props[itemid][name] = value

    for i in range(1, int(response.get('events_count', 0)) + 1):
        itemid = response['events_%d_itemid' % i]
        all_itemids.add(itemid)
        with open('%s/%s' % (dirname, itemid), 'w') as outfile:
            fields = ('itemid',
                      'anum',
                      'eventtime',
                      'security',
                      'allowmask',
                      'poster',
                      'url',
                      'subject',)
            for field in fields:
                key = 'events_%d_%s' % (i, field)
                if key in response:
                    print >>outfile, field + ':', response[key]
            if itemid in props:
                for key, val in props[itemid].items():
                    print >>outfile, key + ':', val

            print >>outfile
            key = 'events_%d_event' % i
            print >>outfile, urllib.unquote(response[key])
    return all_itemids

def get_syncitems():
    """Run the loop to get all 'syncitems' entries.
    Returns a list of (syncitem, time) tuples."""
    syncitems = lj.run('syncitems')
    items = []
    total = int(syncitems['sync_total'])
    print '%d/%d syncitems' % (len(items), total)
    lastsync = None
    while len(items) < total:
        for i in range(1, int(syncitems['sync_count']) + 1):
            item = syncitems['sync_%d_item' % i]
            time = syncitems['sync_%d_time' % i]
            lastsync = max(lastsync, time)
            items.append((item, time))
        if len(items) < total:
            syncitems = lj.run('syncitems', lastsync=lastsync)
    return items

def subtract_second(time):
    """Subtract a second off an LJ date.  I didn't handle 00:00 because I
    am lazy.  This syncing system is way too complicated."""
    sec = int(time[-2:])
    if sec > 0:
        return time[:-2] + '%02d' % (sec - 1)
    min = int(time[-5:-3])
    if min > 0:
        return time[:-5] + '%02d:59' % (min - 1)
    raise RuntimeError, "Couldn't subtract second from " + time

output_dir = lj.usejournal or lj.user
try:
    os.mkdir(output_dir)
except OSError:
    pass  # Assume it exists already.

# Fetch syncitems; convert to a map of itemid => time.
items = get_syncitems()
remaining = {}
for item, time in items:
    if item[0] != 'L':
        continue
    remaining[item[2:]] = time

# Download items, crossing them off as we get them.
while len(remaining) > 0:
    lastsync = min(remaining.values())
    print '%d left, lastsync %s' % (len(remaining), lastsync)
    lastsync = subtract_second(lastsync)
    entries = lj.run('getevents',
                     selecttype='syncitems',
                     lastsync=lastsync,
                     lineendings='unix')
    done = dump_entries(output_dir, entries)
    for itemid in done:
        if itemid in remaining:
            del remaining[itemid]

#!/usr/bin/python

from pysphere import VIServer
import os, ssl, time

class Server:
        def __init__(self):
                self.server = VIServer()
                self.connect()

        def connect(self):
                try:
                        # monkey-patch SSL module (uncomment if unneeded)
                        #ssl._create_default_https_context = ssl._create_unverified_context
                        self.server.connect('vsphere-host', 'user', 'password')
                except Exception as e:
                        return str(e)
                return False

        def disconnect(self):
                self.server.disconnect()

if __name__=="__main__":
	# your vm to snap goes here
	vm_name = 'vm-name-here'

	# open vSphere connection
        con = Server()
        con.connect()

	# find the vm object and get the list of snaps
        vm = con.server.get_vm_by_name(vm_name)
        snapshot_list = vm.get_snapshots()

        snaps = [ { "name":s.get_name(),
                    "description":s.get_description(),
                    "created":s.get_create_time(),
                    "state":s.get_state(),
                    "path":s.get_path(),
                    "parent":s.get_parent(),
                    "children":s.get_children() } for s in snapshot_list ]

        for s in range(0, len(snaps)-3):
		# delete all but last snapshots
		print 'deleting snap: %s' % snaps[s]['name']
		task = vm.delete_named_snapshot(snaps[s]['name'], remove_children=False, sync_run=True)

	# kill zombi process prone apps
	apps = ['appname.py']
	for a in apps:
		cmd = 'killall -9 %s' % a
		print cmd
		os.system(cmd)
		# sleep to be sure proc is killed
		time.sleep(5)

	# create a memory snapshot so VM reverts to working state
	snapname = ('%s.snap-%s') % (vm_name, '_'.join(time.asctime(time.localtime(time.time())).split(' ')) )
	print 'creating new memory snap: %s' % snapname
	task = vm.create_snapshot(snapname,  memory=True, quiesce=False, sync_run=False)

	# close the vsphere connection
	con.disconnect()

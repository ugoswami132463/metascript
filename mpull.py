import subprocess 
import os 
import sys
import xml.etree.ElementTree as ET
import getpass

def mount_path(path = "none"):
	args = path.split('\\')
	os.chdir('/mnt')
	username = getpass.getuser()
	localpath = str(args[1]+'/'+ args[2])
	if not os.path.exists(localpath):
		os.system('sudo mkdir -p '+localpath)
		mount_cmd = "sudo mount -t cifs -o username="+username+" //crmhyd/nsid-hyd-06 /mnt/"+localpath
		os.system(mount_cmd)
	else:
		print "mount already exists..."
	location = '/mnt/'+localpath+'/'+args[3]
	return location

def pushd_cmd(args = "none"):
	os.chdir(args)	
	output = os.getcwd()	
	return output

def find_au():
	list_tok= []
	os.chdir('LINUX/android/release_notes')
	output = os.getcwd()
	print output
	au_tag= ''
	btd = open('build_tree_details.txt')
	Lines = btd.readlines()
	for lines in Lines:
		sline = str(lines)
		if sline[4:12] == 'AU Label':
			au_tag =sline[14:len(lines)]
			break
	return au_tag
	#we got the au_tag from release notes


if __name__ == '__main__': 
	path = str(sys.argv[1])
	main_dir = os.getcwd()
	mount = mount_path(path)
	ret = pushd_cmd(mount)
	if ret == str(sys.argv[1]):
		print "Moved to:",ret
	
	tree = ET.parse('contents.xml')
	root = tree.getroot()
	apps_string = ''
	lrp = root.findall("builds_flat/build/linux_root_path")
	i = 0
	for i in range(len(lrp)):
		attribute = lrp[i].attrib
		tag_con = attribute.values()
		content_str = str(tag_con).strip('[\' \']')
		if content_str == 'APPS_BUILDROOT':
			apps_string = lrp[i].text
			break

	ret = pushd_cmd(apps_string)
	print "Moved to:",ret
	au_tag = find_au()
	print au_tag
	#sync codebase command
	os.chdir(main_dir)
	
	cmd ='python ../lint_tools/src/sync_scripts/sync.py /local/mnt/workspace/ugoswami/mannar_sod -p ' + au_tag + '--target=qssi'
	print 'executing',cmd
	os.system(cmd)

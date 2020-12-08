import subprocess 
import os 
import sys
import xml.etree.ElementTree as ET
import getpass

def mount_path(path = "none"):
	args = path.split('\\')
	os.chdir('/mnt')
	win_path ='/'
	localpath = ''
	username = getpass.getuser()
	for path in args:
		win_path += path
		win_path +='/'
		localpath+=path
		localpath+='/'

	print "LOCALPATH",localpath
	print "WINDOWSPATH",win_path
	if not os.path.exists(localpath):
		print "mount needed, please grant permission. . ."
		os.system('sudo mkdir -p /mnt/'+localpath)
		mount_cmd = "sudo mount -t cifs -o username="+username+" "+win_path +" /mnt/"+localpath
		os.system(mount_cmd)
	else:
		print "mount already exists..."
	location = '/mnt'+localpath
	return location

def umount_path(path = "none"):
	args = path.split('\\')
	os.chdir('/mnt')
	localpath = args[1]
	os.system('sudo umount'+localpath)
	os.system('sudo rm -rf'+localpath)

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

def get_hotfixes():
	list_tok= []
	output = os.getcwd()
	print output
	hotfixes= ''
	btd = open('build_tree_details.txt')
	Lines = btd.readlines()
	for lines in Lines:
		sline = str(lines)
		if sline[4:16] == 'Change Refs:':
			hotfixes =sline[16:len(lines)]
			break
	return hotfixes
	#we got the au_tag from release notes


if __name__ == '__main__':
	py_exec = os.path.abspath(os.path.dirname(sys.argv[0]))
	print "Python Location:",py_exec
	path = str(sys.argv[1])
	kdev = False
	if len(sys.argv) > 2:
		kdev = True
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
	hotfixes = get_hotfixes()
	android_version=''
	if "LA.UM.9.12." in au_tag:
		android_version = 'KONA_R'
	elif "LA.UM.8.12." in au_tag or "LA.UM.8.13." in au_tag:
		android_version = 'KONA_Q'
	elif "LA.UM.9.14." in au_tag:
		android_version = 'LAHAINA_R'
	else :
		android_version = 'LEGACY'

	#sync codebase command
	os.chdir(main_dir)
	workspace = raw_input("Create workspace location: ")
	print "Your Workspace: ",workspace
	if not kdev:
		if android_version == 'LEGACY' or android_version =='KONA_Q':
			cmd = 'repo init -u git://git.quicinc.com/platform/manifest.git -b refs/tags/' +au_tag
			print 'executing',cmd
			os.system(cmd)
			os.system('repo sync')

		if android_version == 'LAHAINA_R' or android_version == 'KONA_R':
			cmd ='python ../lint_tools/src/sync_scripts/sync.py '+workspace+' -p ' + au_tag[0:44]+' --target=qssi'
			print 'executing',cmd
			os.system(cmd)

	else:
		if android_version == 'LEGACY':
			print "Kdev not recommended for ",android_version
		if android_version == 'KONA_Q':
			print android_version
			#makedir
			if not os.path.exists(workspace):
				os.system('mkdir ' + workspace)
			#init kdev
			os.chdir(workspace)
			os.system('git clone ssh://git-android.quicinc.com:29418/upstream/kdev.git kdev')
			os.chdir('kdev')
			#repo init
			cmd = 'repo init -u git://git.quicinc.com/platform/manifest --current-branch --no-tags --groups=cyborg -b refs/tags/'+au_tag[0:44]+' -m versioned.xml --repo-url=git://git.quicinc.com/tools/repo.git --repo-branch=qc/stable && repo sync -c -j8 --no-tags --no-clone-bundle --optimized-fetch'
			print 'Moving to Directory: ',os.getcwd()
			os.system(cmd)
			#repo sync

		if android_version == 'KONA_R':
			print android_version
			#makedir
			if not os.path.exists(workspace):
				os.system('mkdir ' + workspace)
			#init kdev
			os.chdir(workspace)
			os.system('git clone ssh://git-android.quicinc.com:29418/upstream/kdev.git kdev')
			os.chdir('kdev')
			#repo init
			cmd = 'repo init -u git://git.quicinc.com/la/vendor/manifest -b LA.UM.9.12 -g cyborg -b refs/tags/'+au_tag[0:44]+' --repo-url=ssh://git.quicinc.com:29418/tools/repo --repo-branch=qc/stable && repo sync -c -j16 --no-tags --no-clone-bundle --optimized-fetch'
			print 'Moving to Directory: ',os.getcwd()
			os.system(cmd)
			#repo sync

		if android_version == 'LAHAINA_R':
			print android_version
			#makedir
			if not os.path.exists(workspace):
				os.system('mkdir ' + workspace)
			#init kdev
			os.chdir(workspace)
			os.system('git clone ssh://git-android.quicinc.com:29418/upstream/kdev.git kdev')
			os.chdir('kdev')
			#repo init
			cmd = 'repo init -u git://git.quicinc.com/la/vendor/manifest -b LA.UM.9.14 -g cyborg -b refs/tags/'+au_tag[0:44]+' --repo-url=ssh://git.quicinc.com:29418/tools/repo --repo-branch=qc/stable && repo sync -c -j16 --no-tags --no-clone-bundle --optimized-fetch'
			print 'Moving to Directory: ',os.getcwd()
			os.system(cmd)
			#repo sync
	username = getpass.getuser()
	os.chdir(workspace)
	os.system(py_exec+'/kdev_gpull/./gpull cp '+hotfixes)


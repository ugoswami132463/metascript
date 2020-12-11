# metascript
This is a tool for code sync in a easy way just by providing the meta network path.

I'm introducing a script for doing code sync in a error free way. This is "metascript". This script will help us in performing code sync through any means, whether we do via lint tool or kdev or legacy target code sync, however LA targets only. Please give this script a try and let me know if you encounter any bugs during your run.
 
Note: The Initial startup configurations like installing python modules will be necessary. Those which are required for lint tool could be found on
go/aimfaq
 
Necessary tool which would be required are mentioned below:


	
CIFS ( Common Internet File System ) : We would perform mount operation of the windows network location so cifs-utils would be necessary. 

instructions:


sudo apt-get update
sudo apt-get install cifs-utils


With This we are ready for runnign the script. Good thing about this script is that you do not need to find the AU tag, just provide the network locations and it will find the AU tag along with hotfixes and start repo sync.
 
Instructions to run:

Syntax: python mpull.py "\\crmhyd location" <optional argument kdev>
Example:
(for kdev)
python mpull.py "\\crmhyd\nsid-hyd-06\SM8250_SDX55.LA_TN.2-0_2-0-00198-STD_LP5.INT-1" kdev
(for FBC)
python mpull.py "\\crmhyd\nsid-hyd-06\SM8250_SDX55.LA_TN.2-0_2-0-00198-STD_LP5.INT-1"
 
/ * * * You have to enter your password 2-3 times due to commands running with sudo, please bare with it, it's still a WIP * * */
You will have to enter your workspace location.
Create workspace location: /local/mnt/workspace/ugoswami/kona_R198/
And we are done. Code will sync automatically along with the hot-fixes.

Please find the location of the script here: \\lab6233\Dropbox\Udipto\script_alpha_test
copy the metascript folder to you harvester, in any mount where lint_tools is present.
 
Currently some of the commands hard coded.
python ../lint_tools/src/sync_scripts/sync.py

This would not work if lint_tools is not present in the same directory. again a WIP.

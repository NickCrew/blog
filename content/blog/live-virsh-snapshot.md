Title: Live External VM Snapshots for Libvirt
Tags: virtualization, libvirt, kvm
Date: 2018-08-08
Category: Tutorials
Author: Nick Ferguson
Summary: How to take live, external snaphots of a Qemu guest machine using libvirt and virsh.

---
# Synopsis
__*In this tutorial we are going to take an external snapshot of a running VM.*__

---

## External vs Internal Snapshots  

*QCOW2* disk images have the ability to store snapshots within the image itself. This can
have its uses, but an external snapshot is faster and allows us to safely store a copy
of the file system at that point. Red Hat also recommends external snapshots as the
preferred snapshotting method.  

## Live Block Commit

In simple terms, live block commit allows us to take a snapshot, operate a given period
of time with that snapshot as the primary disk image, and then 'merge' the virtual disks
with all changes since the snapshot saved.  

This is useful to us because we are going to:  
1. Take a snapshot  
2. Copy the original disk image to our backup location  
3. Use block commit to merge the snapshot back into the original disk image.

## Supported Qemu Versions

*Qemu* is the hardware emulator used with *KVM*, the Linux kernel module that enables virtualization  and *Libvirt*, the user-space virtual resource manager. You need to be using *Qemu* version __2.5__ or greater to create external snapshots. This is a problem if you're running CentOS 7, but it is easily remedied by installing the version of the qemu-kvm package from the oVirt/RHEV
repositories. If you are using Ubuntu then it will be included in the package available in the repos.

### Using oVirt Repo on CentOS 7  

	:::bash
	yum install centos-release-qemu-ev qemu-kvm-ev

--- 
### Qemu Guest Agent

> __Note:__ You should install the __qemu-guest-agent__ package on all of your guests. Having the agent installed
> allows you to perform operations on the guest machine without logging in such as freezing the
> file system, rebooting and shutdown safely. We will issue a flag with our snapshot command that
> freezes the file system during the time which it is taken to ensure there is no data loss.  

### How to set-up the qemu-guest-agent

On the guest machine install the `qemu-guest-agent` package using yum, dnf or apt depending on
your distro.  

__Create a virtual device in the guests definition__  

`virsh edit YOUR_DOMAIN` 


__Inside the tagsa__  

`<devices></devices>`

__Insert:__  

	<channel type='unix'>
		 <target type='virtio' name='org.qemu.guest_agent.0'/>
		 <address type='virtio-serial' controller='0' bus='0' port='1'/>
	</channel>
 
  

*__Note:__ If you already have a serial port on the guest, you may need to change __port='1'__ to a higher port number.  


Now you can use the *__--quiesce__* flag with *virsh* commands to freeze a guest machine's file machine.  

---

## The Snapshot Command

We will use the __virsh__ tool.  


The *domain* is the name your guest was defined as. To see a list of all guest domains on your system 
you can run:  

	virsh list --all

To see the virtual disks in use by a given domain:  

	virsh domblklist YOUR_DOMAIN

Here is example output for my Katello host:  

```bash
$ virsh domblklist katello
Target     Source
------------------------------------------------
vda        /vm_storage/foreman-katello.qcow2
```

To see a domain's current snapshots:  

	virsh snapshot-list YOUR_DOMAIN  

---
## Taking the snapshot

	:::bash
	virsh snapshot-create-as \
	--domain YOUR_DOMAIN guest-state-1 \
	--diskspec vda,file=/your/storage/pool/YOUR_DOMAIN-overlay-1.qcow2 \
	--disk-only --atomic --quiesce  


The `virsh domblklist` command should now show the overlay image as the virtual disk in use.  

You are now able to copy the original disk image to a backup location as it is not being 
actively written to. 

Once the copy is finished it's time to perform a live block commit:  

```bash
virsh blockcommit YOUR_DOMAIN vda --active --verbose --pivot
```

If successful you see the following output:  

```bash
Performing live block commit...
Block commit: [100 %]
Successfully pivoted
```

And that's it! A successful external snapshot with live block commit.  

#### Scripting It

I have written a shell script that performs a live snapshot and backup with the following usage:  
`./live-blockcommit-snap YOUR_DOMAIN /your/backup/location`  
  
```bash
#!/bin/bash
#
# Take an external snapshot with virsh using live block commit feature
#
# Usage: ./live-blockcommit-snap domain-name /backup/destination 
#
# Creates log collection directory in backup-destination
#
# You must have the qemu-guest-agent installed and enabled on the guest, otherwise
# the --quiesce argument must be removed from the snapshot-create command
# before the script will function. 
#
# Nicholas Ferguson 2018 MIT License https://gitlab.com/nickopotamus/


DOMAIN=$1

# check if guest is running
if [[ $(virsh list --all | grep "$DOMAIN" | awk '{print $3}' | awk 'NR==1{print $1}') == "running" ]]; then
  echo "Guest running...continuing..."
else
  echo "Guest is not running...stopping..."
  exit 1
fi

# check for correct arguments
if [ "$#" -ne 2 ]; then
  echo "Missing arguments! Provide domain and backup directory." >&2
  exit 1
fi

# does the backup destination exit
if ! [ -e "$2" ]; then
  echo "$2 not found!" >&2
  exit 1
fi

# is the backup destination a directory
if ! [ -d "$2" ]; then
  echo "$2 is not a directory!" >&2
  exit 1
fi 

# generate time stamp
TIME=`date "+%Y%m%d-%H%M%S"`

BACKUP_DEST="$2"/"$1"

# create backup dir if it does not exist
[ -d "$BACKUP_DEST" ] || mkdir -p "$BACKUP_DEST"

# label snapshot with timestamp
STATE="$1"_"$TIME"

# take care of logging
LOG_DIR="$2"/snapshot_logs
[ -d "$LOG_DIR" ] || mkdir -p "$LOG_DIR"

SNAP_LOG="$LOG_DIR"/"$DOMAIN"_latest.log
rm "$SNAP_LOG"
touch "$SNAP_LOG"

exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>"$SNAP_LOG" 2>&1


# name the overlay file
OVERLAY="$STATE"_overlay

# target is domain name, image is virtual disk file
TARGET=`virsh domblklist --details "$1" | grep ^file | awk '{print $3}'`
IMAGE=`virsh domblklist --details "$1" | grep ^file | awk '{print $4}'`
POOLDIR=`dirname "$IMAGE"`

# take the snapshot. will fail without a working qemu-guest-agent
virsh snapshot-create-as --domain "$1" "$STATE" \
--diskspec "$TARGET",file="$POOLDIR"/"$OVERLAY".qcow2 \
--disk-only \
--atomic \
--quiesce

# perform the backup
echo "Copying image to backup location..."
cp -a "$IMAGE" "$BACKUP_DEST"/"$STATE"

# live block commit
echo "Performing live block commit..."
virsh blockcommit "$1" "$TARGET" --active --verbose --pivot

# remove the overlay file
rm "$POOLDIR"/"$OVERLAY".qcow2

# remove the snapshot from domain
virsh snapshot-delete $1 --metadata "$STATE"

echo 'Current snapshots attached to this guest:'
virsh snapshot-list $1
echo '------------------------'

echo 'Most recent external snapshots:'
ls "$BACKUP_DEST"
echo '------------------------'

echo 'Current disk image in use:'
virsh domblklist $DOMAIN
```



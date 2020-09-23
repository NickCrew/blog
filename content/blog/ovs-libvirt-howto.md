Title: Libvirt and OpenVSwitch on RHEL 7
Date: 2018-07-22
Tags: OpenVSwitch, virtualization, kvm, libvirt, networking
Category: Tutorials
Author: Nick Ferguson
Summary: How to use OpenVSwitch with Libvirt/Qemu hypervisor on RHEL or CentOS 7

---

# Synopsis

__*Learn how to leverage OpenVSwitch to create a Libvirt network with portgroups for each of our VLANs.*__
  
--- 

### Prequisites 

1. We will assume that you have installed OVS and Libvirt 


2. If you desire VLAN support, you have a network interface connected to a trunk    
  

3. If you are using Ubuntu or Debian this will still work, but you will have to configure the `/etc/network/interfaces` file or netplan rather than the network-scripts used here. 

  
### Creating and Configuring the OVS Bridge
---

#### Create the OVS bridge  

	:::bash 
	ovs-vsctl add-br ovsbr0  
  
  
#### Add the interface (_eno1_ in this case) connected to the trunk

	:::bash
	ovs-vsctl add-port ovsbr0 eno1  
  

#### Check the configuration

	:::bash
	ovs-vsctl show
	Bridge "ovsbr0"
		Port "eno1"
			Interface "eno1"
		Port "ovsbr0"
			Interface "ovsbr0"
				type: internal
	  
---
> __NOTE:__ It is not necessary to set the `tag` or `trunk` parameters on the
> OVS Port or Bridge for this particular scenario to work


#### Assign an IP to the OVS Bridge:

##### Remove the IP from the physical NIC

	:::bash
	ip addr del 0.0.0.0 dev eno1

	
##### Run dhclient on the OVS bridge

	:::bash
	ip link set up ovsbr0
	dhclient ovsbr0 


__*Note: At this point it is ready but it will not persist across reboots without creating and modifying the network scripts*__  


### Configuring the network-scripts 


    :::bash
	# /etc/sysconfig/network-scripts/ifcfg-eno1
	TYPE="OVSPort"
	OVS_BRIDGE="ovsbr0"
	PROXY_METHOD="none"
	BROWSER_ONLY="no"
	BOOTPROTO="none"
	DEFROUTE="yes"
	IPV4_FAILURE_FATAL="no"
	NAME="eno1"
	DEVICE="eno1"
	ONBOOT="yes"  


#### For DHCP


	:::bash
	# /etc/sysconfig/network-scripts/ifcfg-ovsbr0
	BOOTPROTO="dhcp"
	DEVICE="ovsbr0"
	DEVICETYPE="ovs"
	HOTPLUG="no"
	NM_CONTROLLED="no"
	ONBOOT="yes"
	TYPE="OVSBridge"  


> __Note:__ You do not have to disable *NetworkManager*, however we do not want NetworkManager controlling any of the interfaces involved in our OVS set-up, including the physical NIC and any virtual ports.  
  

__*Reboot the system or restart networking to confirm everything is working correctly.*__  

---

## Define the Libvirt Network  

Here we are assuming two (2) VLANs with IDs __50__ and __60__, plus a virtual trunk: __vlan-all__.  

Each VLAN will be a Libvirt network *portgroup* that you may select using any of the Libvirt-client tools.  


### Create an XML file


	:::XML
	<!-- /tmp/ovs-network.xml -->
	<network>
	  <name>ovs-network</name>
	  <forward mode='bridge'/>
	  <bridge name='ovsbr0'/>
	  <virtualport type='openvswitch'/>
	  <portgroup name='vlan-01' default='yes'>
	  </portgroup>
	  <portgroup name='vlan-50'>
		<vlan>
		  <tag id='50'/>
		</vlan>
	  </portgroup>
	  <portgroup name='vlan-all'>
		<vlan trunk='yes'>
		  <tag id='50'/>
		  <tag id='60'/>
		</vlan>
	  </portgroup>
	</network>

  
  
### Define the network  

	:::bash
	virsh net-define /tmp/ovs-network.xml  
  

#### Start the network

	:::bash
	virsh net-start ovs-network

#### Have the network start on boot    

    virsh net-autostart ovs-network  

Now when you start a guest they will be on the subnet of the portgroup you select.  
If you select __vlan-all__ then that is a trunk interface (like the one coming into your physical NIC).  

---

This is far from the only way to use OVS with KVM/Libvirt guests but
I believe it by the simplest and easiest. One beneift of using OVS
is that guests on the same hypervisor, on the same subnet will communicate at virtio speed because they do not have to go back out over copper.


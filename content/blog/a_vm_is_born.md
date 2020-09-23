Title: Life and Death of a Virtual Machine
Date: 2018-07-06
Tags: lab, virtualization, applications
Category: Articles
Author: Nick Ferguson
Summary: Discussing my VM lifecycle management platform

---
# Synopsis
__Disscuss the key components to the automated virtual infrastructure of my lab environment.__  

---

## Introduction

I'm going to do a quick write-up on my host provisioning workflow now that all the pieces are in place and (mostly) functioning as intended. In any large production environment it will be a necessity to have automated processes to handle: Host creation, Life-cycle mangement and patching, provisioning and possibly identity management depending on the environment. We are not yet going to cover things such as logging and monitoring, just the things happening at the birth" of the machine. 

 

---
## Foreman

Foreman lets you define anything you'd normally be able to define with good old virt-install. Resources, storage location, disk type, network interfaces, operating system, the works. You are able to create *Host Groups* that act as templates so you don't have to fill out 20 drop-down menus everytime you want a host. Red Hat distributions are able to make use of *kickstart* files and Debian distros use a *preseed* file. These are used during regular unattended installs and essentially contain all the answers to the questions an OS installer would ask you. You are able to edit and store many variations within Foreman and associate them with operating systems. So you select the template you want to base your guest on and then... 
   
 

Foreman is able to run a TFTP server and act as the PXE boot server for your network. When you use PXE, you must configure your DHCP server to tell machines where the TFTP server is located. In my case I had to enter a command in the terminal of my Edgerouter-X. At this point the kernel image is fetched, booted and the kickstart or preseed unattended install commences. You can watch as the installer goes through answering the prompts on your behalf and it is quite rewarding! In my case, Foreman is accessing the Libvirt system the same way you as a user would to define and manage the VMs. Foreman supports many other hypervisors, including ESXi, as well.
  

In addition to the regular installer options, the kickstart files can pull in *snippets* to instruct the performing of other actions. After the system and packages are installed these commands will be called. Foreman is able to integrate with a FreeIPA server and take advantage of the unattended ipa-client-install command to join your guest to the specified realm. In my case my FreeIPA servers also provide DNS to the network, as well as configure automounting of user home folders and NFS shares. This is quite convenient because as soon as a guest reports that the installation is complete, you can ssh into your IPA user at the machines freshly updated DNS record hostname with all of your files waiting for you. 

---
 
## Puppet

At this point Puppet will begin running any classes assigned to the host through it's host group or individually. Some modules I run on all guests are the configuration of the snmp daemon so that Librenms may discover it and add it to monitoring, the rsyslog daemon so that it may begin sending logs to Graylog, NTP so that it may synchronize its time with the other servers and ssh key injection.  
  
---

## Katello
Katello is a Foreman plugin that allows you to manage *Content*. You can sync repositories, either on-demand or download the entire repo. During kickstart the guest will activate its *subscription* based on the assigned *Life-Cycle Environment*. The life-cycle environment just says what packages and updates a given guest or group of guests should receive. The *katello-agent* is installed on the VMs to allow reporting back to Foreman. Katello will manage their updates for you and inform you of any problems. The guests are in regular communication with the Foreman server to check and see if they need packages and initiating puppet runs to apply any changes made through the Puppet Classes. This takes a huge chunk of manual maintenance off your plate. 

---

## Conclusion
And so the VM is born! Puppet or another configuration management tool will go on to apply configurations needed for it's specific role. If it is a web server, nginx will be set up. If it's a database server then PostgreSQL may be installed and configured at this point. You are able to continously manage your guests through Foreman and it's partner apps throughout it's life until finally it is destroyed. 
 
  
It is a lot of work in the beginning setting up such an environment and it does occasionally require some sweet-talking, but for the most part it does a very good job of automating some of the most repetitive aspects of using a virtual environment. Foreman comes with a great dashboard that lets you get an overview of the state of your environment. You can see if any hosts have had failed puppet runs, what configurations have been applied recently and to whom, if they're out of sync with the package repositories or if they're not powered on at all. If you need to dig deeper, extensively detailed reports are available for each host. 
 
 

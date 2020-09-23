Title: Foreman and FreeIPA Realm Integration
Tags: virtualization, platforms, dns, freeipa, identity,
Date: 2018-08-02
Category: Tutorials
Author: Nick Ferguson
Summary: How to integrate FreeIPA with Foreman and Katello for automatic DNS records, Home directory mounting, SSH keys and Identity Management during VM provisioning.

---

# Synopsis

__A configuration by which  hosts created with Foreman auto-join your FreeIPA Realm and registered as IPA hosts__

---

## FreeIPA Host

We need to create an IPA user for foreman. I used *"foreman-user"* but you can choose something different if you'd like. This article will assume *"foreman-user"*. Avoid foreman-proxy or other usernames that occur as users on the Foreman host. Assign this user the __role__ of *Smart Proxy Host Manager*.

Before beginning, your Foreman host needs to be registered as an IPA host. 

	ipa-client-install


We need to create a __service__ for the Foreman proxy.  

If you're using the FreeIPA webui:  

`Identity => Services => "add +"`

*Example:*

	foremanproxy/foreman.example.com@EXAMPLE.COM

---

## Foreman Host

You need to install the __ipa-admintools__ package:  

	yum install ipa-admintools
	foreman-prepare-realm admin foreman-user
  

We need to edit some config files. These are the relevant sections:


	:::bash
	### /etc/foreman-proxy/settings.d/freeipa_realm.yml

	# Authentication for Kerberos-based Realms
	:keytab_path: /etc/foreman-proxy/freeipa.keytab
	:principal: foreman-user@EXAMPLE.COM

	:ipa_config: /etc/ipa/default.conf
	# Remove from DNS when deleting the FreeIPA entry
	:remove_dns: true

__/etc/foreman-proxy/settings.d/freeipa_realm.yml__  



	:::bash
	### /etc/foreman-proxy/settings.d/realm.yml

	# Can be true, false, or http/https to enable just one of the protocols
	:enabled: true

	# Available providers:
	#   realm_ad
	#   realm_freeipa
	:use_provider: realm_freeipa
__/etc/foreman-proxy/settings.d/realm.yml__  

---

### FreeIPA Host
Copy the keytab from the IPA server, where *freeipa* is the hostname of your IPA server and *foremanproxy* is the name of the service:

```bash
ipa-getkeytab -s freeipa.example.com -p foremanproxy/freeipa.example.com -k /etc/krb5.keytab *
```

Copy the keytab to the appropriate location:

```bash
cp freeipa.keytab /etc/foreman-proxy/freeipa.keyab
```



Make the foreman-proxy user owner and set correct permissions:  

```bash
chown foreman-proxy /etc/foreman-proxy/freeipa.leytab
```

```bash
chmod 600 /etc/foreman-proxy/freeipa.keytab
```

```bash
cp /etc/ipa/ca.crt /etc/pki/ca-trust/source/anchors/ipa.crt
```

```bash
update-ca-trust enable && update-ca-trust
```

```bash
systemctl restart foreman-proxy
```



Test the keytab is present:

```bash
   sudo -u foreman-user kinit -k -t /etc/foreman-proxy/freeipa.keytab foreman-user
```

You should now be able to select your realm in the Foreman webui  

`Infrastructure => Realms`  

Ensure your provisioning template calls the __*freeipa_register*__ snippet. Read over the snippet to see optional host parameters you may set.  

> If you are using FreeIPA as your DNS server and you would like the records automatically updated, set the following host parameter:  

`Name: freeipa_opts Value: —enable-dns-updates`

  
> If you are using the automount feature of FreeIPA:  

`Name: freeipa_automount Value: true`

Now when you create a host, as long as you have your realm selected, it should automatically join the realm and register with the server.  

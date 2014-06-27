# Go Developer Virtual Machine

A provisioned development box using VirtualBox and Vagrant. This will install the full stack of tools you need to run a Go micro-service.

## Dependencies

1. Upgrade to Mac OS Mavericks 
2. Install Oracle VirtualBox (http://virtualbox.org)
3. Install Vagrant (http://vagrantup.com)

## Getting Started

Clone the repo, cd into the directory and run:

```
vagrant up
```

## Provisioning

The first time you run this, it will also provision the box. If you don't know what that means, read the docs at vagrantup.com. After the first time, you will have to explicitly run `vagrant provision` if you change the `bootstrap.sh` file.

## Contributing

Before updating this repo, you must be familiar with the Vagrant documentation.

The provisioning for this box is a shell script called `bootstrap.sh`. This is essentially just a shell script. Add whichever dependencies you need at the end of the file.

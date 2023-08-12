# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://vagrantcloud.com/search.
  config.vm.box = "freebsd/FreeBSD-13.2-STABLE"
  config.disksize.size = '70GB'

  # config.vm.synced_folder "home/", "/home/vagrant"
  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  config.vm.box_check_update = true

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # NOTE: This will enable public access to the opened port
  config.vm.network "public_network"
  #   config.vm.network "forwarded_port", guest: 80, host: 8080
  #   config.vm.network "forwarded_port", guest: 443, host: 8443
  #   config.vm.network "forwarded_port", guest: 22, host: 8022
  #   config.vm.network "forwarded_port", guest: 5443, host: 5443

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine and only allow access
  # via 127.0.0.1 to disable public access
  # config.vm.network "forwarded_port", guest: 80, host: 8080, host_ip: "127.0.0.1"

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "./repos", "/vagrant_data"

  # Provider-specific configuration so you can fine-tune various
  # backing providers for Vagrant. These expose provider-specific options.
  # Example for VirtualBox:
  #
  config.vm.provider "virtualbox" do |vb|
  #   # Display the VirtualBox GUI when booting the machine
  #   vb.gui = true
  #
  #   # Customize the amount of memory on the VM:
     vb.memory = "8096"
     vb.cpus = 4
  end

#  config.vm.synced_folder "./src", "/root/src"
#  config.vm.synced_folder "./deploy", "/root/deploy"

  # View the documentation for the provider you are using for more
  # information on available options.

  # Enable provisioning with a shell script. Additional provisioners such as
  # Ansible, Chef, Docker, Puppet and Salt are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   apt-get update
  #   apt-get install -y apache2
  # SHELL

  
   config.vm.provision "shell", inline: <<-SHELL
    sudo su -
    pkg install -y htop mc git py39-pip nano vim tmux snoopy
    pip install -U pip
    # echo "Get freebsd src"
    # git clone -b  stable/12 --depth 1 https://git.freebsd.org/src.git /usr/src
    echo "Get kitchen src"
    git clone https://github.com/armbsd/kitchen.git
 SHELL

end
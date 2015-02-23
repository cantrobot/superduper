$SETUP = <<EOF
apt-get update && apt-get -y install mitmproxy bridge-utils haproxy
sed -r -i 's/ENABLED=.*/ENABLED=1/g' /etc/default/haproxy
mkdir -p /etc/{superduper,consul.d,confd}
mkdir -p /etc/confd/{conf.d,templates}
mkdir -p /var/lib/consul
ln -s /vagrant/etc/replay_and_test.py /etc/superduper/
ln -s /vagrant/etc/superduper_settings /etc/superduper/settings
ln -s /vagrant/etc/confd_haproxy.tmpl /etc/confd/templates/haproxy.tmpl
ln -s /vagrant/etc/confd_haproxy.toml /etc/confd/conf.d/haproxy.toml
ln -s /vagrant/etc/consul_web.json /etc/consul.d/web.json
ln -s /vagrant/bin/superduper /usr/local/bin/superduper
ln -s /vagrant/bin/consul /usr/local/bin/consul
ln -s /vagrant/bin/confd /usr/local/bin/confd
superduper start_consul
superduper create prod1
superduper create prod2
superduper create test1
superduper create test2
superduper move test1 test
superduper move test2 test
superduper start_confd
superduper start_proxy
echo 'echo -e "\nDualest Status\n"' >> /home/vagrant/.bashrc
echo "sudo superduper status" >> /home/vagrant/.bashrc
EOF

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.provision "shell", inline: $SETUP
end 

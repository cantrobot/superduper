# superduper
A simple POC for cloning traffic from a live cluster to a test cluster and comparing responses.

Using consul, confd, haproxy, mitmproxy, linux bridging and namespaces, superduper is a wrapper that helps manage an environment for testing various traffic cloning scenarios using a custom python script.

You can find logs and debugging information in ```/var/log/superduper```.

## Up and Testing

### Start environment
    vagrant up
    vagrant ssh
    
### Test the cluster
    curl http://192.168.50.3
    tail /var/log/superduper/*

## Usage
    usage: /usr/local/bin/superduper command [args]

    Commands:
      list                    - List webservers and namespaces
      create [name]           - Creates a webserver in a new namespace
      delete [name]           - Completele deletes the nameserver/networking/namespace
      move [name] [prod|test] - Move instance from one HAProxy backend to another (prod|test)
      start                   - Start all services
      stop                    - Stop all services
      status                  - Show status of all services
      start_proxy             - Start flow proxy
      stop_proxy              - Stop flow proxy
      start_consul            - Start consul agent
      stop_consul             - Stop consul agent
      start_confd             - Start confd
      stop_confd              - Stop confd

### Add a new backend prod instance
    superduper create prod3

### Change backends for an instance
    superduper move prod3 test

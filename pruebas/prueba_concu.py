#!/usr/bin/env python3

import time
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel, info
from mininet.net import Mininet
from mininet.node import OVSKernelSwitch, RemoteController

server_host = "10.0.0.1"
server_port = "8080"
protocol = "sr"

tp_path = "/home/deno/redes-tp1/"

server_path = tp_path + "src/start-server.py"
up_path = tp_path + "src/upload.py"
down_path = tp_path + "src/download.py"
storage_path = tp_path + "storage/"

test_files_path = tp_path + "pruebas/"
up1_name = "up1.txt"
up2_name = "up2.txt"
down1_name = "down1.txt"
down2_name = "down2.txt"


def run_concurrency_test():
  net = Mininet(topo=None, build=False, ipBase="10.0.0.0/8", switch=OVSKernelSwitch)

  info("--- Agregando componentes a la topología ---\n")
  h_server = net.addHost("h1", ip=server_host)
  h_client1 = net.addHost("h2", ip="10.0.0.2")
  h_client2 = net.addHost("h3", ip="10.0.0.3")
  h_client3 = net.addHost("h4", ip="10.0.0.4")
  h_client4 = net.addHost("h5", ip="10.0.0.5")

  switch = net.addSwitch("s1", cls=OVSKernelSwitch)

  info("--- Conectando enlaces con pérdida de 10% y delay ---\n")
  net.addLink(h_server, switch, cls=TCLink, loss=10, delay="20ms")
  net.addLink(h_client1, switch, cls=TCLink, loss=10, delay="20ms")
  net.addLink(h_client2, switch, cls=TCLink, loss=10, delay="20ms")
  net.addLink(h_client3, switch, cls=TCLink, loss=10, delay="20ms")
  net.addLink(h_client4, switch, cls=TCLink, loss=10, delay="20ms")

  info("--- Iniciando red ---\n")
  net.start()

  info("--- Iniciando servidor ---\n")
  h_server.cmd("python3 " + server_path + 
                " -H " + server_host + 
                " -p " + server_port +
                " -s " + storage_path +
                " > server.log 2>&1 &")
  time.sleep(3)

  info("--- En paralelo, 2 uploads y 2 downloads desde diferente shosts ---\n")
  h_client1.cmd("python3 " + up_path + 
                " -H " + server_host + 
                " -p " + server_port + 
                " -s " + test_files_path +
                " -n " + up1_name +
                " -r " + protocol +
                " > client1.log 2>&1 &")
  h_client2.cmd("python3 " + up_path + 
                " -H " + server_host + 
                " -p " + server_port + 
                " -s " + test_files_path +
                " -n " + up2_name +
                " -r " + protocol +
                " > client2.log 2>&1 &")
  h_client3.cmd("python3 " + down_path + 
                " -H " + server_host + 
                " -p " + server_port + 
                " -d " + test_files_path +
                " -n " + down1_name +
                " -r " + protocol +
                " > client3.log 2>&1 &")
  h_client4.cmd("python3 " + down_path + 
                " -H " + server_host + 
                " -p " + server_port + 
                " -d " + test_files_path +
                " -n " + down2_name +
                " -r " + protocol +
                " > client4.log 2>&1 &")

  CLI(net)

  info("--- Deteniendo la red ---\n")
  net.stop()


if __name__ == "__main__":
  run_concurrency_test()
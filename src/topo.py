from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI


# HOST_1 ----- (S) ----- HOST_2
def myNetwork():
    # TCLink se usa para poder configurar perdidas y delay
    net = Mininet(controller=None, link=TCLink)

    print("--- Agregando controladores y hosts ---")

    # net.addController("c0")
    h1 = net.addHost("h1", ip="10.0.0.1")
    h2 = net.addHost("h2", ip="10.0.0.2")
    s1 = net.addSwitch("s1", failMode="standalone")

    print("--- Creando enlaces con condiciones de red ---")
    # Se configura la perdida y el retraso
    # Para RTT 40 ms que pide el enunciado, necesito 10 ms por enlace
    # Para ver mejor las retrasmisiones durante las pruebas aumenten el delay
    # Para cumplir condicion de operar hasta con valores de RTT de hasta 300ms)
    net.addLink(h1, s1, loss=10, delay="100ms")
    net.addLink(h2, s1, loss=0, delay="50ms")

    print("--- Iniciando red ---")
    net.start()

    print("--- Se abre la consola de Mininet")
    CLI(net)

    net.stop()


if __name__ == "__main__":
    # rtt_ms = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    myNetwork()

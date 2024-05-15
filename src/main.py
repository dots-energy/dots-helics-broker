import helics as h

MS_TO_BROKER_DISCONNECT = 600000

def main():
    broker = h.helicsCreateBroker("zmq", "helics_broker", "-f 2 --loglevel=debug --ipv4 --timeout='60s' --port=30000")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)


if __name__ == "__main__":
    exit(main())
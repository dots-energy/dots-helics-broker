import helics as h
import os

MS_TO_BROKER_DISCONNECT = 600000

def main():
    amount_of_federates = os.getenv("AMOUNT_OF_FEDERATES", "2")
    broker_port = os.getenv("HELICS_BROKER_PORT", "30000")
    amount_of_esdl_message_federates = int(os.getenv("AMOUNT_OF_ESDL_MESSAGE_FEDERATES", "2")) + 1

    broker = h.helicsCreateBroker("zmq", "helics_broker_esdl", f"-f {amount_of_esdl_message_federates} --loglevel=debug --ipv4 --timeout='60s' --brokerport={broker_port} --port={broker_port}")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)

    broker = h.helicsCreateBroker("zmq", "helics_broker_co_simulation", f"-f {amount_of_federates} --loglevel=debug --ipv4 --timeout='60s' --brokerport={broker_port} --port={broker_port}")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)


if __name__ == "__main__":
    exit(main())
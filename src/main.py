from threading import Thread
import helics as h
import os
from Logger import LOGGER

MS_TO_BROKER_DISCONNECT = 7200000 # 2 Hours

def start_helics_broker(broker_name: str, amount_of_federates: int, broker_port: str):
    broker = h.helicsCreateBroker("zmq", broker_name, f"-f {amount_of_federates} --loglevel=debug --ipv4 --timeout='60s' --brokerport={broker_port} --port={broker_port} --globaltime")
    broker.wait_for_disconnect(MS_TO_BROKER_DISCONNECT)
    LOGGER.info(f"Started broker {broker_name} with {amount_of_federates} federates on port {broker_port}")

class HelicsInitalizationFederateExecutor:

    def __init__(self, borker_port : int, fedarate_name : str):
        self.broker_port = borker_port
        self.federate_name = fedarate_name

    def init_message_federate_info(self) -> h.HelicsFederateInfo:
        federate_info = h.helicsCreateFederateInfo()
        h.helicsFederateInfoSetBroker(federate_info, "localhost")
        h.helicsFederateInfoSetBrokerPort(federate_info, self.broker_port)
        h.helicsFederateInfoSetCoreType(federate_info, h.HelicsCoreType.ZMQ)
        h.helicsFederateInfoSetIntegerProperty(federate_info, h.HelicsProperty.INT_LOG_LEVEL, h.HelicsLogLevel.NO_PRINT)
        return federate_info
    
    def init_federate(self) -> tuple[h.HelicsMessageFederate, h.HelicsEndpoint]:
        federate_info = self.init_message_federate_info()
        message_federate = h.helicsCreateMessageFederate(self.federate_name, federate_info)
        message_enpoint = h.helicsFederateRegisterEndpoint(message_federate, "broker_endpoint_amount_of_calculations", h.HelicsDataType.INT.name)
        return message_federate, message_enpoint 
    
    def start_federate_for_amount_of_calculations(self):
        federate, endpoint = self.init_federate()
        h.helicsFederateEnterExecutingMode(federate)
        total_amount_of_calculations = 0
        while h.helicsFederateRequestTime(federate, h.HELICS_TIME_MAXTIME) != h.HELICS_TIME_MAXTIME:
            if h.helicsEndpointHasMessage(endpoint):
                additional_amount_of_calculations = int(h.helicsMessageGetString(h.helicsEndpointGetMessage(endpoint)))
                total_amount_of_calculations += int(additional_amount_of_calculations)
        return total_amount_of_calculations

def main():
    amount_of_federates = os.getenv("AMOUNT_OF_FEDERATES", "2") + 1
    broker_port = os.getenv("HELICS_BROKER_PORT", "30000")
    amount_of_esdl_message_federates = int(os.getenv("AMOUNT_OF_ESDL_MESSAGE_FEDERATES", "2"))
    

    start_helics_broker("helics_broker_initialization", amount_of_esdl_message_federates, broker_port)

    start_helics_broker("helics_broker_co_simulation", amount_of_federates, broker_port)



if __name__ == "__main__":
    exit(main())

def tsched_beh(rx_port, tx_port, rx, tx):
    '''|
    | Specify the behavior, describe data processing; there is no notion
    | of clock. Access the in/out interfaces via GetPacket() and
    | AddPacket() methods. The "tsched_beh" function does not return
    | values.
    |________'''

    if rx_port.hasPacket():
        data = rx_port.get()
        tx_port.append(data)

    if rx.hasPacket():
        data = rx.get()
        tx.append(data)

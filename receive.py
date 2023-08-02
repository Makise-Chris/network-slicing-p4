#!/usr/bin/env python3

from probe_hdrs import *


def expand(x):
    yield x
    while x.payload:
        x = x.payload
        yield x

def check_link(link_id, utilization, qdepth):
    if utilization>=5 or qdepth>=5:
        if link_id==0:
            print("==URLLC: Shoud change S1-S3-S5-S6 to S1-S3-S4-S6==")
        elif link_id==1:
            print("==mMTC: Shoud change S1-S2-S5-S4-S6 to S1-S2-S4-S5-S6==")
        elif link_id==2:
            print("==URLLC: Shoud change S1-S3-S4-S6 to S1-S3-S5-S6==")
        elif link_id==3:
            print("==mMTC: Shoud change S1-S2-S4-S5-S6 to S1-S2-S5-S4-S6==")

def handle_pkt(pkt):
    if ProbeData in pkt:
        data_layers = [l for l in expand(pkt) if l.name=='ProbeData']
        link_id = [l for l in expand(pkt) if l.name=='Probe']
        print("")
        for sw in data_layers:
            utilization = 0 if sw.cur_time == sw.last_time else 8.0*sw.byte_cnt/(sw.cur_time - sw.last_time)
            print("Switch {} - Port {}: {} Mbps, Qdepth: {}".format(sw.swid, sw.port, utilization, sw.qdepth))
            check_link(link_id[0].link_id, utilization, sw.qdepth)

def main():
    iface = 'eth0'
    print("sniffing on {}".format(iface))
    sniff(iface = iface,
          prn = lambda x: handle_pkt(x))

if __name__ == '__main__':
    main()

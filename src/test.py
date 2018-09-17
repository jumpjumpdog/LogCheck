import os, sys, xml.dom.minidom, csv
import threading

import time

import thread

from Site import BaseBandEqm



# root = xml.dom.minidom.parse("./EAA387.xml").documentElement
#
# baseBandEqms = root.getElementsByTagName("BASEBANDEQM")
# baseBandEqm = baseBandEqms[0]
# print baseBandEqm
#
# elements = baseBandEqm.getElementsByTagName("element")
# print  len(elements)
# print elements[0].toxml()
#
#
# for element in elements:
#     print  element.getElementsByTagName("CN")[0].childNodes[0].data
#     print  element.getElementsByTagName("SRN")[0].childNodes[0].data
#     print  element.getElementsByTagName("SN")[0].childNodes[0].data

class Singleton:
    password = "123"
    def __init__(self,name):
        self.name = name
    def printName(self):
        print self.name
    def printPassword(self):
        print  self.password
    def printIdPassword(self):
        print id(self.password)
        print id(self.name)


def print_time(thread_name, delay):
    count = 0
    while count<5:
        time.sleep(delay)
        count += 1
        print  "%s: %s"%(thread_name, time.ctime(time.time()))



if __name__ == "__main__":
    # singleton = Singleton("sjw")
    # singleton.printName()
    # singleton.printPassword()
    # singleton2 = Singleton("lsl")
    # singleton2.printPassword()
    #
    # singleton.printIdPassword()
    # singleton2.printIdPassword()

    try:
        thread.start_new_thread(print_time, ("Thread-1",2,))
        thread.start_new_thread(print_time,("Thread-2",4,))
    except:
        print "Error:unable to start a thread"

    threading.current_thread.join


import serial

def return_distance():
    while True:
        ser = serial.Serial('/dev/ttyACM0', 345600)
        read_serial=ser.readline().decode('utf-8').rstrip()
        print(str(read_serial))

    #while i < 10:
    #    read_serial=ser.readline()#.decode('utf-8').rstrip()
        #s[0] = str(int (ser.readline(), 16))
        #print(s[0])
    #    i += 1
    #    print(read_serial)
    #    sums +=  int(float(read_serial))
    #print(str(sums))
    #return sums / 10
    #print(read_serial)
    #return read_serial
return_distance()
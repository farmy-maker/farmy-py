import time
import sys
import spidev


CHANNEL = 0


def read_adc(spi, channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    ret = ((adc[1] & 3) << 8) + adc[2]
    return ret


def convert_volts(adc):
    ret = round((adc * 3.3) / float(1023), 4)
    return ret


def get_moisture():
    spi = spidev.SpiDev()
    spi.open(0, 0)
    adc = read_adc(spi, CHANNEL)
    ret = convert_volts(adc)
    spi.close()
    return ret


if __name__ == '__main__':
    spi = spidev.SpiDev()
    spi.open(0, 0)
    try:
        while True:
            data = read_adc(spi, CHANNEL)
            print("adc  : {:8} ".format(data))
            volts = convert_volts(data)
            print("volts: {:8.2f}".format(volts))
            time.sleep(3)
    except KeyboardInterrupt:
        spi.close()
        sys.exit(0)

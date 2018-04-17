from machine import I2C

MAXIM = 0x57
I2C_WRITE_ADDR = 0xAE
I2C_READ_ADDR = 0xAF
REG_INTR_STATUS_1 = 0x00
REG_INTR_STATUS_2 = 0x01
REG_INTR_ENABLE_1 = 0x02
REG_INTR_ENABLE_2 = 0x03
REG_FIFO_WR_PTR = 0x04
REG_OVF_COUNTER = 0x05
REG_FIFO_RD_PTR = 0x06
REG_FIFO_DATA = 0x07
REG_FIFO_CONFIG = 0x08
REG_MODE_CONFIG = 0x09
REG_SPO2_CONFIG = 0x0A
REG_LED1_PA = 0x0C
REG_LED2_PA = 0x0D
REG_PILOT_PA = 0x10
REG_MULTI_LED_CTRL1 = 0x11
REG_MULTI_LED_CTRL2 = 0x12
REG_TEMP_INTR = 0x1F
REG_TEMP_FRAC = 0x20
REG_TEMP_CONFIG = 0x21
REG_PROX_INT_THRESH = 0x30
REG_REV_ID = 0xFE
REG_PART_ID = 0xFF


class MAX30102(object):
    def __init__(self, i2c=None):
        self.i2c = i2c or I2C(0, I2C.MASTER)

        # Only enable proximity interrupt
        self._write(REG_INTR_ENABLE_1, 0x10)
        self._write(REG_INTR_ENABLE_2, 0x00)
        # Reset the FIFO read/write pointers
        self._write(REG_FIFO_RD_PTR, 0x00)
        self._write(REG_FIFO_WR_PTR, 0x00)
        # Reset the overflow counter
        self._write(REG_OVF_COUNTER, 0x00)
        # 0x50 = Average every 4 samples, enable rollover mode,
        # FIFO nearing full limit not set since we disabled it
        # See datasheet page 17 for more details
        self._write(REG_FIFO_CONFIG, 0x50)
        # 0x02 for Red only, 0x03 for SpO2 mode, 0x07 multimode LED
        self._write(REG_MODE_CONFIG, 0x03)
        # SPO2_ADC range = 4096nA, SPO2 sample rate (100 Hz), LED pulseWidth (411uS)
        # See datasheet page 18 8for more details
        self._write(REG_SPO2_CONFIG, 0x27)
        # ~7mA for LED1, LED2 and ~25mA for pilot LED
        self._write(REG_LED1_PA, 0x24)
        self._write(REG_LED2_PA, 0x24)
        self._write(REG_PILOT_PA, 0x7F)

    def _write(self, addr, reg):
        self.i2c.writeto_mem(MAXIM, addr, reg)

    def _read(self, addr):
        return self.i2c.readfrom_mem(MAXIM, addr)

    def reset(self):
        self.i2c.writeto_mem(MAXIM, REG_MODE_CONFIG, 0x40)

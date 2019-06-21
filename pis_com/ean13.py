try:
    from PIL import Image, ImageDraw
except ImportError:
    import Image, ImageDraw


class EanBarCode:
    def __init__(self):
        A = {0 : "0001101", 1 : "0011001", 2 : "0010011", 3 : "0111101", 4 : "0100011",
             5 : "0110001", 6 : "0101111", 7 : "0111011", 8 : "0110111", 9 : "0001011"}
        B = {0 : "0100111", 1 : "0110011", 2 : "0011011", 3 : "0100001", 4 : "0011101",
             5 : "0111001", 6 : "0000101", 7 : "0010001", 8 : "0001001", 9 : "0010111"}
        C = {0 : "1110010", 1 : "1100110", 2 : "1101100", 3 : "1000010", 4 : "1011100",
             5 : "1001110", 6 : "1010000", 7 : "1000100", 8 : "1001000", 9 : "1110100"}
        self.groupC = C
        self.family = {0 : (A,A,A,A,A,A), 1 : (A,A,B,A,B,B), 2 : (A,A,B,B,A,B), 3 : (A,A,B,B,B,A), 4 : (A,B,A,A,B,B),
                       5 : (A,B,B,A,A,B), 6 : (A,B,B,B,A,A), 7 : (A,B,A,B,A,B), 8 : (A,B,A,B,B,A), 9 : (A,B,B,A,B,A)}

    def makeCode(self, code):
        self.EAN13 = []
        for digit in code:
            self.EAN13.append(int(digit))
        if len(self.EAN13) == 13:
            self.verifyChecksum(self.EAN13)
        elif len(self.EAN13) == 12:
            self.EAN13.append(self.computeChecksum(self.EAN13))
        left = self.family[self.EAN13[0]]
        strCode = 'L0L'
        for i in range(0,6):
            strCode += left[i][self.EAN13[i+1]]
        strCode += '0L0L0'
        for i in range (7,13):
            strCode += self.groupC[self.EAN13[i]]
        strCode += 'L0L'
        return strCode

    def computeChecksum(self, arg):
        weight=[1,3]*6
        magic=10
        sum = 0
        for i in range(12):
            sum += int(arg[i]) * weight[i]
        z = ( magic - (sum % magic) ) % magic
        if z < 0 or z >= magic:
            return None
        return z

    def verifyChecksum(self, bits):
        computedChecksum = self.computeChecksum(bits[:12])
        codeBarChecksum = int(bits[12])
        if codeBarChecksum != computedChecksum:
            raise Exception ("Bad checksum is %s and should be %s"%(codeBarChecksum, computedChecksum))

    def getImage(self, value, height = 50, thickness = 1):
        bits = self.makeCode(value)
        code = ""
        for digit in self.EAN13:
            code += "%d" % digit
        position = 0
        im = Image.new("1",(thickness*len(bits)+position,height))
        draw = ImageDraw.Draw(im)
        draw.rectangle(((0,0),(im.size[0],im.size[1])),fill=256)
        for bit in range(len(bits)):
            if bits[bit] == '1':
                draw.rectangle(((thickness*bit+position,0),(thickness*bit+position+thickness,height-10)),fill=0)
            elif bits[bit] == 'L':
                draw.rectangle(((thickness*bit+position,0),(thickness*bit+position+thickness,height-3)),fill=0)
        return im


def get_checksum(data):
    return EanBarCode().computeChecksum(data)


def ean13_image(data, height = 100, thickness = 3):
    return EanBarCode().getImage(data, height, thickness)

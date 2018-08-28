import configparser
import re 


class NSGA2_Config():

    def __init__(self):
        self.train_name = "data/digits.train"
        self.test_name = "data/digits.train"
        self.input_shape = (8, 8, 1)
        self.noutputs = 10

    def load(self, filename):
        config = configparser.ConfigParser()
        config.read(filename)
    
    
        for sec in config.sections():
            for key, val in config[sec].items():
                val = convert(val)
                setattr(self, key.lower(), val)
                setattr(self, key.upper(), val)

        
NSGA2_Cfg = NSGA2_Config()


# auxiliary functions
def is_int(s):
    if re.fullmatch(r'[0-9]+', s):
        return True
    else:
        return False

def is_float(s):
    if re.fullmatch(r'[0-9]+\.[0-9]+', s):
        return True
    else:
        return False

def is_list(s):
    if re.fullmatch(r'\[.+\]', s):
        return True
    else:
        return False

def convert(s):
    if is_int(s):
        val = int(s)
    elif is_float(s):
        val = float(s)
    elif is_list(s):
        s = s.strip()
        s = s.strip("[")
        s = s.strip("]")
        val = s.split(',')
        newval = [] 
        for v in val:
            v = v.strip()
            v = v.strip("'")
            v = v.strip('"')
            newval.append(convert(v))
        val = newval
    else:
        val = s
    return val


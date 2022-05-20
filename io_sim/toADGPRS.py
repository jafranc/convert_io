import logging
import re
import numpy as np
import models
from models import deadoil_blackoil

# pattern_float_block = "(?:(?:(?:(?:[+-]?(?:\d*)(?:\.\d*)(?:[eE][+-]?\d+)?)\s*)+)\\n"
pattern_float_block = "(?:(?:(?:(?:[+-]?(?:\d*)(?:\.\d*)(?:[eE][+-]?\d+)?)\s*)+)\n"
pattern_float_block_of_block = "PVTO\n((?:(?:(?:(?:(?:[+-]?(?:\d*)(?:\.\d*)(?:[eE][+-]?\d+)?)\s*)+)\n)\/\n)+)"
# https://regex101.com/r/SgLVyM/1
# pattern_float_list = r"(?:(?:[+-]?(?:\d*)(?:\.\d*)(?:[eE][+-]?\d+)?)\s*)+"
pattern_float_list = "((?:(?:[+-]?(?:\d*)(?:\.\d*)(?:[eE][+-]?\d+)?)\s*)+)(?:\n|)"

#helpers
def write_gprs_blackoil(f):
    f.write('PVTO\n \t dddd\n /\n')
    f.write('COUPLING \n FIM(FLOW{NATURAL_BLACK_OIL}) \n / \n')


def write_gprs_deadoil(f):
    f.write('PVDO\n \t dddd\n /\n')
    f.write('COUPLING \n -- SEQ(PRESSURE{PRESSURE_NATURAL_DO}, TRANSPORT, 15) \n FIM(FLOW) \n / \n')


def write_gprs(dict_, fname):
    with open(fname, 'w') as f:
        if 'BLACKOIL' in dict_:
            f.write('FLUID\n \t BLACKOIL \n /\n')
            write_gprs_blackoil(f)
        elif 'DEADOIL' in dict_:
            f.write('FLUID\n \t DEADOIL \n /\n')
            write_gprs_deadoil(f)
        else:
            raise NotImplementedError

        f.write("PVTW\n \t dddd \n / \n")
        f.write("DENSITIES\n \t 1 1 1\n /\n")


class adgprs_model_io:
    iofile_: str
    model_: models.deadoil_blackoil.Deadoil_model
    key_dict: dict

    def __init__(self, iof):
        self.iofile_ = iof

    def import_fluid(self):
        logging.info("ADGPRS :: import fluid")
        lines = ''.join(open(self.iofile_).readlines())
        fkey = re.search("\s*FLUID\n(\w+)\n/", lines)
        print(fkey.group(1))

        pvo = None
        pvg = None

        if fkey.group(1) == "BLACKOIL":
            logging.info("Reading BLACKOIL case")

            pattern = pattern_float_block_of_block
            fpvo = re.search(pattern, lines)
            # processing to numpy --> TODO feed it to pvt containers
            tmp = fpvo.group(1).split('\n')[:-1]
            key = None
            pvo = {}
            val = []
            i = 0
            for item in tmp:
                if item == '/':
                    continue
                elif len(item.split()) == 1:
                    if key:
                        pvo[key] = np.stack(val)
                        key = item
                        val = []
                    else:  # first it
                        key = item
                else:
                    val.append(np.asarray(item.split(), dtype=float))

        elif fkey.group(1) == "DEADOIL":
            logging.info("Reading DEADOIL case")
            pattern = "PVDO\n(" + pattern_float_block + ")+)/"
            fpvo = re.search(pattern, lines)
            # processing to numpy --> TODO feed it to pvt containers
            pvo = np.asarray([item.split() for item in fpvo.group(1).split('\n')][:-1], dtype=float)

        pattern = "PVTW\n(.*?)(?:\n|)/"
        # pattern = "PTVW\n"+pattern_float_list+""
        fpvw = re.search(pattern, lines)
        pvtw = np.asarray(fpvw.group(1).split(), dtype=float)

        pattern = "DENSITY\n(.*?)(?:\n|)/"
        # pattern = "DENSITY\n("+pattern_float_list+")"
        fdens = re.search(pattern, lines)
        dens = np.asarray(fdens.group(1).split(), dtype=float)

        print("Done")

    def export_fluid(self):
        logging.info("ADGPRS :: export fluid")

        if isinstance(self.model_, deadoil_blackoil.Blackoil_model):
            fkey = "BLACKOIL"
        elif (isinstance(self.model_, deadoil_blackoil.Deadoil_model)):
            fkey = "DEADOIL"

        self.gprs_dict[fkey] = self.model_.fluid_.dict_

        write_gprs(self.model_.fluid_.dict_, self.iofile_)


if __name__ == "__main__":
    # mio = adgprs_model_io('../misc/gprs.deadoil.txt')
    mio = adgprs_model_io('../misc/gprs.blackoil.txt')
    mio.import_fluid()

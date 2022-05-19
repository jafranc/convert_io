import logging
import re
import models
from models import deadoil_blackoil


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

    def export_fluid(self):
        logging.info("ADGPRS :: export fluid")

        if isinstance(self.model_, deadoil_blackoil.Blackoil_model):
            fkey = "BLACKOIL"
        elif (isinstance(self.model_, deadoil_blackoil.Deadoil_model)):
            fkey = "DEADOIL"

        self.gprs_dict[fkey] = self.model_.fluid_.dict_

        write_gprs(self.model_.fluid_.dict_)

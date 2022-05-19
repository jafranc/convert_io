import logging
import json
from models.pvt import pvt

import numpy as np

# data class
from typing import List


class Fluid_obj:
    dict_: object
    name_: str
    np_: int
    #
    pname_: List[str]
    rho_sc_: List[float]
    cmp_molar_: List[float]
    table_lookup_name_: List[pvt]

    def __init__(self, name='f_', nump=1, pname=['none'], rho_sc=[np.nan], cmp_molar=[np.nan], table_lkn=[pvt()]):
        self.dict_ = {}
        self.name_ = name
        self.np_ = nump

        assert (len(pname) == nump)
        self.pname_ = pname
        assert (len(rho_sc) == nump)
        self.rho_sc_ = rho_sc
        assert (len(cmp_molar) == nump)
        self.cmp_molar_ = cmp_molar
        assert (len(table_lkn) == nump)
        self.table_lookup_name_ = table_lkn

        self.fill_dict(self.name_, self.np_, self.pname_, self.rho_sc_, self.cmp_molar_, self.table_lookup_name_)

    def read_json(self, fjson):
        self.dict_ = json.load(fjson)

    def __str__(self):
        return self.dict_.__str__()

    # def check_size(f, nump, iarg):
    #     @setter.iarg
    #     def wrapper(iarg):
    #         assert(len(iarg) == nump)
    #         return f(iarg)
    #     return wrapper(iarg)

    @property
    def name(self):
        return self.name_

    @name.setter
    def name(self, name: str):
        self.name_ = name

    @name.deleter
    def name(self):
        del self.name_

    #
    @property
    def nump(self):
        return self.nump_

    @nump.setter
    def nump(self, nump: int):
        self.nump_ = nump

    @name.deleter
    def nump(self):
        del self.nump_

    #
    @property
    def pname(self):
        return self.pname_

    @pname.setter
    def pname(self, pname: List[str]):
        self.pname_ = pname

    @pname.deleter
    def pname(self):
        del self.pname_

    #
    @property
    def rho_sc(self):
        return self.rho_sc_

    @rho_sc.setter
    def rho_sc(self, rho_sc: List[float]):
        self.rho_sc_ = rho_sc

    @rho_sc.deleter
    def rho_sc(self):
        del self.rho_sc_

    #
    @property
    def cmp_molar(self):
        return self.cmp_molar_

    @cmp_molar.setter
    def cmp_molar(self, cmp_molar: List[float]):
        self.cmp_molar_ = cmp_molar

    @cmp_molar.deleter
    def cmp_molar(self):
        del self.cmp_molar_

    #
    @property
    def table_lookup_name(self):
        return self.table_lookup_name_

    @table_lookup_name.setter
    def table_lookup_name(self, table_lookup_name: List[bool]):
        self.table_lookup_name_ = table_lookup_name

    @table_lookup_name.deleter
    def table_lookup_name(self):
        del self.table_lookup_name_

    def fill_dict(self, name, nump, pname, rhos_sc, cmp_molar, table_lookup):
        self.dict_['name'] = name
        self.dict_['np'] = nump
        self.dict_['pname'] = pname
        self.dict_['rhos_sc'] = rhos_sc
        self.dict_['cmp_molar'] = cmp_molar
        self.dict_['table_lookup'] = table_lookup

# natural formulation model
class Deadoil_model:

    fluid_ : Fluid_obj

    def __init__(self, fluid : Fluid_obj):
        self.fluid_ = fluid

    def sum_check(self):
        logging.debug("Deadoil :: sum-check")
        logging.debug("Sum check :: number of parameters")

    def sanity_check(self):
        logging.debug("Deadoil :: sum-check")
        logging.debug("Sanity check :: consistence of parameters")

class Blackoil_model(Deadoil_model):

    def sum_check(self):
        logging.debug("Blackoil :: sum-check")

    def sanity_check(self):
        logging.debug("Blackoil :: sanity-check")



if __name__ == "__main__":
    of = Fluid_obj("fluid", 2, ["w", "o"], [1000.0, 789], [1.0, 1.0], [pvt(), pvt()])
    # of = Fluid_obj()
    print(of)

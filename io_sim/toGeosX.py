import xml.etree.ElementTree as ET
import re
import logging

import models
from models import deadoil_blackoil


# model is
# fluid + pvt
# scal
# flash

class geosx_model_io:
    iofile_: str
    model_: models.deadoil_blackoil.Deadoil_model

    def __init__(self, iof):
        self.iofile_ = iof
        self.xmltree_ = ET.parse(iof)
        self.xmlroot_ = self.xmltree_.getroot()
        self.model_ = None
        print("here is the i/o class")

    # def __str__(self):
    def import_fluid(self):
        logging.info("GEOSX :: import fluid")
        # todo switch case
        for elt in self.xmlroot_.findall("./Constitutive/DeadOilFluid"):
            # print(elt.attrib['name'])
            # print(elt.attrib['phaseNames'])
            # print(elt.attrib['surfaceDensities'])
            # print(elt.attrib['componentMolarWeight'])
            # todo defer reading of table file to scal
            # print(elt.attrib['tableFiles'])
            self.model_ = deadoil_blackoil.Deadoil_model(
                deadoil_blackoil.Fluid_obj(elt.attrib['name'],
                                           len(str_dict_(elt.attrib['phaseNames'])),
                                           str_dict_(elt.attrib['phaseNames']),
                                           float_dict_(elt.attrib['surfaceDensities']),
                                           float_dict_(elt.attrib['componentMolarWeight']),
                                           str_dict_(elt.attrib['tableFiles'])))
            print(self.model_.fluid_)

        for elt in self.xmlroot_.findall("./Constitutive/BlackOilFluid"):
            self.model_ = deadoil_blackoil.Blackoil_model(
                deadoil_blackoil.Fluid_obj(elt.attrib['name'],
                                           len(str_dict_(elt.attrib['phaseNames'])),
                                           str_dict_(elt.attrib['phaseNames']),
                                           float_dict_(elt.attrib['surfaceDensities']),
                                           float_dict_(elt.attrib['componentMolarWeight']),
                                           str_dict_(elt.attrib['tableFiles'])))
            print(self.model_.fluid_)

    def export_fluid(self, fname: str) -> ET.Element:
        logging.info("GEOSX :: export fluid")
        # fluid = deadoil.Fluid_obj("fluid", 2, ["w", "o"], [1000.0, 789], [1.0, 1.0], ['pvto.txt', 'pvtw.txt'])
        if isinstance(self.model_, deadoil_blackoil.Blackoil_model):
            elt_fluid = ET.Element("BlackOilFluid", stringify(self.model_.fluid_.dict_))
        elif (isinstance(self.model_, deadoil_blackoil.Deadoil_model)):
            elt_fluid = ET.Element("DeadOilFluid", stringify(self.model_.fluid_.dict_))

        # temp
        problem = ET.Element("Problem")
        constitutive = ET.Element("Constitutive")
        constitutive.append(elt_fluid)
        problem.append(constitutive)
        xtree = ET.ElementTree()
        xtree._setroot(problem)
        indent(xtree)
        xtree.write(fname, xml_declaration="xml version=\"1.0\"")
        # xtree.write("../output/tst.xml", xml_declaration="xml version=\"1.0\"")


# helpers
def indent(tree: ET.ElementTree):
    # init indent
    for elt in tree.iter():
        elt.text = '\n'
        elt.tail = '\n'

    # dfs indent
    iter_indent(tree.getroot())

    # correct level0
    for elt in tree.getroot():
        elt.tail = elt.tail[:-1]


def iter_indent(elt: ET.Element):
    for child in elt:
        child.text += '\t'
        iter_indent(child)
        child.tail += '\t'
    elt.text += '\t'


def stringify(mdict: dict):
    rdict = {}
    for key in mdict:
        if isinstance(mdict[key], list):
            type_check = [isinstance(item, str) for item in mdict[key]]
            if all(type_check):
                mdict[key] = '[' + ','.join(mdict[key]) + ']'
        rdict[str(key)] = re.sub(r'\[', '{ ', str(mdict[key]))
        rdict[str(key)] = re.sub(r'\]', ' }', rdict[str(key)])
    return rdict


def float_dict_(istr: str):
    return [float(re.sub(r",", "", item)) for item in istr.split()[1:-1]]


def str_dict_(istr: str):
    return [str(re.sub(r",", "", item)) for item in istr.split()[1:-1]]


def int_dict_(istr: str):
    return [int(re.sub(r",", "", item)) for item in istr.split()[1:-1]]


if __name__ == "__main__":
    # read and rewrite
    mio = geosx_model_io('../misc/deadOilEgg_base_direct.xml')
    mio.import_fluid()
    mio.export_fluid()

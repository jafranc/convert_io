import argparse
import json
import logging
import io_sim


# TODO reserve events
# TODO reserve mesh/geom (meshio?)
# TODO reserve init
# TODO scal

# TODO duplicate checks on tables --

class parser:

    def __init__(self):

        self.__postt_args__ = ''

        self.__init_default__()

        descr = 'Serializer/Deserializer tool for AD-GPRS / GEOSX / ECL(OPM) \n'
        # '\t use --change-usys to change unit system \n'

        parser = argparse.ArgumentParser(description=descr)

        # flags to command the dispatch to drivers
        parser.add_argument('--fromGeosX', metavar='ifgeos', nargs=1,
                            help='file in')
        parser.add_argument('--fromOPM', metavar='ifopm', nargs=1,
                            help='file in')
        parser.add_argument('--fromADGPRS', metavar='ifgprs', nargs=1,
                            help='file in')

        parser.add_argument('--toGeosX', metavar='fgeos', nargs=1,
                            help='file out')
        parser.add_argument('--toOPM', metavar='fopm', nargs=1,
                            help='file out')
        parser.add_argument('--toADGPRS', metavar='fgprs', nargs=1,
                            help='file out')

        parser.add_argument('--model', metavar='pargs', nargs='+',
                            help='')
        parser.add_argument('--wells', action='store_true',
                            help='wellbore block')
        parser.add_argument('--solvers', action='store_true',
                            help='solver block')

        self.__dispatch__(parser.parse_args())

    def __init_default__(self):
        self.__postt_default__ = 'here is default'
        # logging.basicConfig( filename='gprs-etc.log', filemode='w', level = logging.INFO )
        logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

    def __dispatch__(self, args):
        print("Would dispatch based on pre or post processing:")
        # flag summary
        if (args.fromGeosX):
            logging.info("loading GEOSX")
            logging.info("importing file:" + str(args.fromGeosX[0]))
            self.mio = io_sim.toGeosX.geosx_model_io(args.fromGeosX[0])
            self.mio.import_fluid()
        elif (args.fromADGPRS):
            logging.info("loading AD-GPRS")
        elif (args.fromOPM):
            logging.info("loading OPM")

        logging.info("treating model :" + str(args.model))
        if args.model:
            if args.model[0] == "do":
                logging.info("deadoil")
            elif args.model[0] == "bo":
                logging.info("blackoil")

            elif args.model[0] == "comp":
                logging.info("compositional")
            else:
                raise NotImplementedError

        if args.wells:
            logging.info("wellbores")

        if args.solvers:
            logging.info("solvers")

        if (args.toGeosX):
            logging.info("loading GEOSX")
            logging.info("exporting file:" + str(args.toGeosX[0]))
            self.mio.export_fluid(args.toGeosX[0])
        elif (args.toADGPRS):
            logging.info("loading AD-GPRS")
        elif (args.toOPM):
            logging.info("loading OPM")

        logging.info("wellbores:" + str(args.wells))
        logging.info("solvers:" + str(args.solvers))


if __name__ == "__main__":
    p = parser()

# todo
# 1. propagate parsers and loggers in vtk postt
# 2. copy generation capacity
# 3. h5py reading

# x. for gen input/converter/change-usys define serializer/deserialozer from json
#   and default

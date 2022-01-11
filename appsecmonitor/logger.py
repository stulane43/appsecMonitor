import logging

class Logger:

    def __init__(self, name):
        # set up logging to file
        # logging.basicConfig(level=logging.DEBUG,
        #                     format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        #                     datefmt='%m-%d %H:%M',
        #                     filename=f'{name}.log',
        #                     filemode='w')
        # define a Handler which writes INFO messages or higher to the sys.stderr
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        # set a format which is simpler for console use
        formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
        # tell the handler to use this format
        console.setFormatter(formatter)
        # add the handler to the root logger
        logging.getLogger('').addHandler(console)
        self.log = logging.getLogger(name)
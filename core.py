from config import get_config
import logging
import os
from scrapy import Scrapy
from commandline import get_command_line
logging.basicConfig()
logging.root.setLevel(logging.NOTSET)
logger = logging.getLogger(__name__)

class WrongConfigurationError(Exception):
    pass

def main(return_results=False, parse_cmd_line=True, config_from_dict=None,external_config_file_path=None):
    
    if parse_cmd_line:
        cmd_line_args = get_command_line()
        if cmd_line_args.get('config_file', None):
            external_config_file_path = os.path.abspath(
                cmd_line_args.get('config_file'))
            logger.info("external config file is {}".format(
                external_config_file_path))

    config = get_config(
        cmd_line_args, external_config_file_path, config_from_dict) 
    keyword = config.get('keyword', None) 
    keyfile = config.get('keyfile', None)
    firefoxBinary=config.get('FIREFOX_BINARY_LOCATION', None)
    firefoxCookies=config.get('FIREFOX_COOKIES', None)
    if(firefoxBinary is None):
       raise WrongConfigurationError('the firefox binary is empty') 
    if(firefoxCookies is None or len(firefoxCookies)<1):
       raise WrongConfigurationError('the firefox cookies is empty')   

    if(len(keyword)<1 and len(keyfile)<1):
       raise WrongConfigurationError('the keyword and keyword file is empty') 
    scrapyModel=Scrapy()

    if(len(keyword)>0):
        logger.info(firefoxCookies)    
        scrapyModel.startBykeyword(keyword,firefoxCookies,firefoxBinary)
    else:        
        scrapyModel.handleitembyfile(keyfile)
                


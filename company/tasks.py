
import logging
import os
import json
from django.conf import settings

from company.exceptions import NotCompanyJson, CompanyNameNotInFormat
from company.task_helpers import create_and_save, create_company, get_file_to_dic, get_json_files, rebuild_index_search, extract_name_path

logger = logging.getLogger(__name__)

def consume_one_file(filename):
    print("consuming ", filename)
    
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        
        data_dic = get_file_to_dic(file_path)

        name = extract_name_path(file_path)

        company, created = create_company(name, data_dic)
        
        if created:
            msg = "new company created: %s " % (company.company_name)
            logger.info(msg)
            rebuild_index_search()
        else:
            msg = "company already exists  %s" % (company.company_name)
            logger.warning(msg)

    except NotCompanyJson:
            #print('failed to add')
            msg = "Json file does not follow format %s " % (file_path)
            logger.error(msg)
            #print('not json data')
    except CompanyNameNotInFormat:
        msg = "Company name does not follow format"
        logger.error(msg)

    except json.JSONDecodeError:
        msg = "Json malformed in file: %s" % (file_path)
        logger.error(msg)

    except Exception as e:
        #print('fao;ed exception here')
        msg = "%s:   error occured while consuming %s" % (e,file_path)
        logger.error(msg)


def consume_local_folder(folder_path: str):


    json_files = get_json_files(folder_path)

    #extract data
    msg = 'starting consume : %s, at: %s' %( len(json_files), folder_path)
    logger.info(msg)

    #this check is resource intensive but I'm sacrifcing for speed of completion
    #also I'm assuming that all ein will be unique for all companies

    

    create_and_save(json_files)
                                        


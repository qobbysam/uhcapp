
import logging
import os
import glob
import json
import re
from django.conf import settings
from django.utils import timezone
from django.core.management import call_command

from company.models import CompanyModel, ReportingEntityModel
from company.exceptions import NotCompanyJson, CompanyNameNotInFormat

logger = logging.getLogger(__name__)

def consume_one_file(filename):
    print("consuming ", filename)
    try:
        file_path = os.path.join(settings.MEDIA_ROOT, filename)
        f = open(file_path)
        data_dic = json.loads(f)
        f.close()

        name = extract_name_path(file_path)
        entity_name = data_dic['reporting_entity_name']
        entity_type = data_dic['reporting_entity_type']
        structure =  data_dic['reporting_structure'][0]

        plan_obj = structure['reporting_plans'][0]
        plan_name = plan_obj['plan_name']
        plan_id = plan_obj['plan_id']
        plan_id_type = plan_obj['plan_id_type']
        plan_market_type = plan_obj['plan_market_type']
        network_files = structure['in_network_files']

        entity,created = ReportingEntityModel.objects.get_or_create(
            entity_name = entity_name,
            entity_type = entity_type,


        )

        if created:
            logger.info("new entity created", entity.entity_name)

        company, created = CompanyModel.objects.get_or_create(
            company_name = name,
            entity = entity,
            plan_name = plan_name,
            plan_id = plan_id,
            plan_id_type = plan_id_type,
            plan_market_type = plan_market_type,
            network_files = network_files
        )

        if created:
            msg = "new company created: %s " % (company.company_name)
            logger.info(msg)
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

    folder_path_consume = os.path.join(settings.BASE_DIR, folder_path, "")


    #get all json files
    check_regex = folder_path_consume + "*.json"

    json_files = glob.glob(check_regex)

    #extract data
    companies = []
    companies_update = []
    failed_files = []

    companies_created = 0
    companies_updated = 0
    
    msg = 'starting consume : %s, at: %s' %( len(json_files), check_regex)
    logger.info(msg)

    #this check is resource intensive but I'm sacrifcing for speed of completion
    #also I'm assuming that all ein will be unique for all companies

    companies_check = {int(c_detail.plan_id): [c_detail.company_name, c_detail.id] for c_detail in CompanyModel.objects.all()}
    entities = {entity.entity_name: entity for entity in ReportingEntityModel.objects.all() }
    #print('companies exist', companies_check)
    for file_path in json_files:

        
        #print(data['reporting_entity_name'])

        

        try:
            f = open(file_path)
        
            data = json.load(f)

            f.close()
            company_name = extract_name_path(file_path)
            company = data_to_company(data_dic=data, cmpany_name=company_name, entities=entities)

            

            key =  int(company.plan_id)
            if key in companies_check:
                #print("exists")
                if company.company_name == companies_check[key][0]:
                    company.id = companies_check[key][1]

                    companies_update.append(company)
                    companies_updated += 1
                else:
                    #company.created_at = timezone.now(),
                    #company.modified_at = timezone.now()
                    
                    companies.append(company)
                    companies_created += 1
            
            else:
                
                #company.created_at = timezone.now(),
                #company.modified_at = timezone.now()
                companies.append(company)
                companies_created += 1
                #print('appending one file')

        except NotCompanyJson:
            #print('failed to add')
            failed_files.append(file_path)
            msg = "Json file does not follow format %s " % (file_path)
            logger.error(msg)
            #print('not json data')
        except CompanyNameNotInFormat:
            failed_files.append(file_path)
            msg = "Company name does not follow format"
            logger.error(msg)

        except json.JSONDecodeError:
            failed_files.append(file_path)
            msg = "Json malformed in file: %s" % (file_path)
            logger.error(msg)

        except Exception as e:
            #print('fao;ed exception here')
            failed_files.append(file_path)
            msg = "%s:   error occured while consuming %s" % (e,file_path)
            logger.error(msg)

           


        if len(companies) > 10:

            #batch if needed to create

            CompanyModel.objects.bulk_create(companies)

            companies.clear()
            rebuild_index_search()

        if len(companies_update) > 10:
            CompanyModel.objects.bulk_update(companies_update, [
                                                    #'name',
                                                    
                                                    'plan_name',
                                                    #'plan_id',
                                                    'entity',
                                                    'plan_id_type',
                                                    'plan_market_type',
                                                    'network_files',
                                                    'modified_at'])
            companies_update.clear()
            rebuild_index_search()
    
    if companies:
        CompanyModel.objects.bulk_create(companies)
        #print('finishing save')
        rebuild_index_search()
    
    if companies_update:
        CompanyModel.objects.bulk_update(companies_update, [
                                                    #'name',
                                                    'entity',
                                                    'plan_name',
                                                    #'plan_id',
                                                    'plan_id_type',
                                                    'plan_market_type',
                                                    'network_files',
                                                    'modified_at'])
    
    msg = "Attempted to Consumed %s , created: %s, updated: %s , failed: %s, failed_files: %s" %(len(json_files),companies_created, companies_updated, len(failed_files), failed_files  )
    logger.info(msg)

                                        


def data_to_company(data_dic: dict, company_name, entities:dict) -> CompanyModel:


    try:
        
        entity_name = data_dic['reporting_entity_name']
        entity_type = data_dic['reporting_entity_type']

        if entity_name in entities:

            entity = entities[entity_name]
        else:
            entity, created = ReportingEntityModel.objects.get_or_create(entity_name=entity_name, entity_type=entity_type)
            if created:

                entities[entity_name] = entity
        

        structure =  data_dic['reporting_structure'][0]

        plan_obj = structure['reporting_plans'][0]
        plan_name = plan_obj['plan_name']
        plan_id = plan_obj['plan_id']
        plan_id_type = plan_obj['plan_id_type']
        plan_market_type = plan_obj['plan_market_type']

        network_files = structure['in_network_files']
        

        company = CompanyModel(
            company_name= company_name,
            entity = entity,
            plan_name = plan_name,
            plan_id = plan_id,
            plan_id_type = plan_id_type,
            plan_market_type = plan_market_type,
            network_files = network_files,
            

        )

        return company
    
    except:
        #print("failed to convert", flush=True)
        raise NotCompanyJson
        

def extract_name_path(filepath: str)-> str:
    #tract name from path
    try:
        head , tail = os.path.split(filepath)

        tail_split = tail.split("_")

        #test files that I downloaded follow this pattern
        
        company_name = tail_split[1]

        #print(company_name)

        if company_name is None or company_name == "":
            raise CompanyNameNotInFormat
        
        #I am asuming that '-' is not part of the names
        return company_name.replace("-", " ")
    except:
        raise CompanyNameNotInFormat

def rebuild_index_search():

    call_command('update_index')


def check_regex(input_string:str) -> bool:

    pattern = "^[0-9]{4}-[0-9]{2}-[0-9]{2}_.+_index.json$"

    match = re.compile(pattern)

    return bool(match.match(input_string))
    
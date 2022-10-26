import xmltodict
import numpy as np


def runProcess():

    dict_language = { 'en' : 'English',
                      'cs' : 'Czech',
                      'de' : 'German',
                      'es' : 'Spanish',
                      'fr' : 'French',
                      'it' : 'Italian',
                      'nl' : 'Dutch',
                      'pl' : 'Polish',
                      'pt' : 'Portuguese'
                      }

    for iso,language in dict_language.items():
        print('-----> ', language)
        # xml_data = getData(r'G:\Nomenclature\Article.Nomenclature\binder\nomenclature\xml\\' + iso + '_product1.xml')
        xml_data = getData('xml/' + iso + '_product1.xml')
        print()

        ## SYNONYMS FOR ALL ACTIVES
        actives_entities = getActivesEntities(xml_data)
        n_actives_entities = len(actives_entities)
        print('Number of actives entities: ' + str(n_actives_entities))
        n_entitiesWithSynonyms, total_number_of_synonyms, medianSyns, MaxSyns = getSynonymsStatistics(actives_entities)
        percent_n_ActivesWithSynonyms = round((n_entitiesWithSynonyms / n_actives_entities)*100, 2)
        n_nomenclatureTerms = getNomenclatureTerms(n_actives_entities, total_number_of_synonyms)
        print('Total number of synonyms in actives entities: {}'.format(total_number_of_synonyms))
        print('Number of actives entities with synonyms in {} : {} ({}%) Median: {}, Max: {}'.format(language, n_entitiesWithSynonyms, percent_n_ActivesWithSynonyms, medianSyns, MaxSyns))
        print('Total number of nomenclature terms in {} : {}'.format(language, n_nomenclatureTerms))
        print()

        ## SYNONYMS FOR GROUPS OF DISORDERS
        groupsOfDisorders = getGroupsOfDisorders(actives_entities)
        n_groupsOfDisorders = len(groupsOfDisorders)
        print('Number of groups of disorders: ' + str(n_groupsOfDisorders))
        n_groupsWithSynonyms, total_number_of_synonyms, medianSyns, MaxSyns = getSynonymsStatistics(groupsOfDisorders)
        percent_n_groupsWithSynonyms = round((n_groupsWithSynonyms / n_groupsOfDisorders)*100, 2)
        n_nomenclatureTerms = getNomenclatureTerms(n_groupsOfDisorders, total_number_of_synonyms)
        print('Total number of synonyms in groups of disorders: {}'.format(total_number_of_synonyms))
        print('Number of groups of disorders with synonyms in {} : {} ({}%) Median: {}, Max: {}'.format(language, n_groupsWithSynonyms, percent_n_groupsWithSynonyms, medianSyns, MaxSyns))
        print('Total number of nomenclature terms for groups of disorders in {} : {}'.format(language, n_nomenclatureTerms))
        print()

        ## SYNONYMS FOR DISORDERS
        disorders = getDisorders(actives_entities)
        n_disorders = len(disorders)
        print('Number of disorders: ' + str(n_disorders))
        n_disordersWithSynonyms, total_number_of_synonyms, medianSyns, MaxSyns = getSynonymsStatistics(disorders)
        percent_n_disordersWithSynonyms = round((n_disordersWithSynonyms / n_disorders)*100, 2)
        n_nomenclatureTerms = getNomenclatureTerms(n_disorders, total_number_of_synonyms)
        print('Total number of synonyms in disorders: {}'.format(total_number_of_synonyms))
        print('Number of disorders with synonyms in {} : {} ({}%) Median: {}, Max: {}'.format(language, n_disordersWithSynonyms, percent_n_disordersWithSynonyms, medianSyns, MaxSyns))
        print('Total number of nomenclature terms in {} : {}'.format(language, n_nomenclatureTerms))
        print()

        ## SYNONYMS FOR SUBTYPES OF DISORDERS
        subtypesOfDisorders = getSubtypesOfDisorders(actives_entities)
        n_subtypesOfDisorders = len(subtypesOfDisorders)
        print('Number of subtypes of disorders: ' + str(n_subtypesOfDisorders))
        n_subtypesWithSynonyms, total_number_of_synonyms, medianSyns, MaxSyns = getSynonymsStatistics(subtypesOfDisorders)
        percent_n_subtypesWithSynonyms = round((n_subtypesWithSynonyms / n_subtypesOfDisorders)*100, 2)
        n_nomenclatureTerms = getNomenclatureTerms(n_subtypesOfDisorders, total_number_of_synonyms)
        print('Total number of synonyms in subtypes of disorders: {}'.format(total_number_of_synonyms))
        print('Number of subtypes of disorders with synonyms in {} : {} ({}%) Median: {}, Max: {}'.format(language, n_subtypesWithSynonyms, percent_n_subtypesWithSynonyms, medianSyns, MaxSyns))
        print('Total number of nomenclature terms in {} : {}'.format(language, n_nomenclatureTerms))
        print()


def getData(xmlfile):
    """
    Read an xml return a dict with xmltodict package
    :return: xml parsed as dict
    """
    with open(xmlfile, "r", encoding='ISO-8859-1') as ini:
        xml_dict = xmltodict.parse(ini.read())
    return xml_dict

def getActivesEntities(xml_data):
    """
    filter out inactive entities highlighting flag 8192
    :param xml_data:
    :return:
    """
    actives_entities = []
    for entity in xml_data["JDBOR"]["DisorderList"]["Disorder"]:
        DisorderFlagList = entity['DisorderFlagList']['DisorderFlag']
        if isinstance(DisorderFlagList, dict):
            if DisorderFlagList['Value'] != '8192':
                actives_entities.append(entity)
        else:
            DisorderFlags = []
            for DisorderFlag in DisorderFlagList:
                DisorderFlags.append(DisorderFlag['Value'])
            if not '8192' in DisorderFlags:
                actives_entities.append(entity)
    return actives_entities

def getGroupsOfDisorders(actives_entities):
    """
    keeping only groups of disorders (with flag 36547)
    :param actives_entities:
    :return:
    """
    disorders = []
    for entity in actives_entities:
        if entity['DisorderGroup']['@id'] == '36540':
            disorders.append(entity)
    return disorders

def getDisorders(actives_entities):
    """
    keeping only disorders (with flag 36547)
    :param actives_entities:
    :return:
    """
    disorders = []
    for entity in actives_entities:
        if entity['DisorderGroup']['@id'] == '36547':
            disorders.append(entity)
    return disorders

def getSubtypesOfDisorders(actives_entities):
    """
    keeping only subtypes of disorders (with flag 36547)
    :param actives_entities:
    :return:
    """
    disorders = []
    for entity in actives_entities:
        if entity['DisorderGroup']['@id'] == '36554':
            disorders.append(entity)
    return disorders

def getSynonymsStatistics(entities):
    """
    Generic method to get statistics on synonyms
    :param entities:
    :return:
    """
    list_n_synonyms = []
    for entity in entities:
        if entity['SynonymList']['@count'] != '0':
            list_n_synonyms.append(int(entity['SynonymList']['@count']))
    synonym_array = np.array(list_n_synonyms)
    total_number_of_synonyms = 0
    for n_synonym in list_n_synonyms:
        total_number_of_synonyms += n_synonym
    return len(list_n_synonyms) , total_number_of_synonyms, int(np.median(synonym_array)),np.max(synonym_array)

def getNomenclatureTerms(n_entities, n_synonyms):
    """
    Generic method to get statistics on nomenclature terms
    :param entities:
    :return:
    """
    n_nomenclatureTerms = n_entities + n_synonyms
    return n_nomenclatureTerms



if __name__ == '__main__':

    runProcess()
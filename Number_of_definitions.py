import xmltodict

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
        xml_data = getData(r'G:\Nomenclature\Article.Nomenclature\binder\nomenclature\xml\\' + iso + '_product1.xml')
        # xml_data = getData('xml/' + iso + '_product1.xml')
        ## SELECT ACTIVE ENTITIES
        actives_entities = getActivesEntities(xml_data)
        print('Number of actives entities: ' + str(len(actives_entities)))
        ## SELECT DISORDERS
        disorders = getDisorders(actives_entities)
        n_disorders = len(disorders)
        print('Number of disorders: ' + str(n_disorders))
        ## SELECT DISORDERS WITH A DEFINITION
        disordersWithDefinition = getDisordersWithDefinition(disorders)
        n_disordersWithDefinition = len(disordersWithDefinition)
        percent_n_disordersWithDefinition = round((n_disordersWithDefinition / n_disorders)*100, 2)
        print('Number of disorders with a definition in {} : {} ({}%)'.format(language, str(n_disordersWithDefinition), str(percent_n_disordersWithDefinition)))
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




def getDisordersWithDefinition(disorders):
    """
    Calculation of numbers of disorders with a definition
    # We look for the disorders that have a definition in their datas
    :param disorders:
    :return:
    """
    disordersWithDefinition = []
    for disorder in disorders:
        try:
            if disorder["SummaryInformationList"]['@count'] != '0':
                try:
                    if disorder["SummaryInformationList"]['SummaryInformation']['TextSectionList']['@count'] != '0':
                        if disorder["SummaryInformationList"]['SummaryInformation']['TextSectionList']['TextSection']['TextSectionType']['@id'] == '16907':
                              disordersWithDefinition.append(disorder)
                except:
                    pass
        except:
            pass
    return disordersWithDefinition

if __name__ == '__main__':
    runProcess()
import pympi
import re

def find_date_components(text):
    pattern = r"(\d{4})(\d{2})(\d{2})"
    match = re.search(pattern, text)
    if match:
        year = match.group(1)
        month = match.group(2)
        day = match.group(3)
        return year, month, day
    else:
        return None

def eaf_process(eaf_dir, parent_names = ['phrase'], translation_name = 'Note', item_number_tier = 'ALI item number'):
    #importing .eaf file
    eaf = pympi.Elan.Eaf(eaf_dir)
    error_box = {}
    # Find total dialects in eaf file
    dialects = [eaf.get_tier_ids_for_linguistic_type(di)[0] for di in parent_names]
    total_data = []
    for dialect in dialects:
        try:
            speaker = eaf.get_parameters_for_tier(dialect)['PARTICIPANT']
        except:
            speaker = "unknown"
        # getting tier ids
        translation_tier_id = eaf.get_tier_ids_for_linguistic_type(translation_name, dialect)
        #item_number_tier = eaf.get_tier_ids_for_linguistic_type(item_number_tier, parent_names[0])
        try:
            translation_tier_id = translation_tier_id[0]
        except:
            error_box[dialect] = "Clip tier id is not defined for {}".format(dialect)
            continue
        # getting translations
        #translation_tier_id = eaf.get_tier_ids_for_linguistic_type(translation_name, dialect)
        # try:
        #     translation_tier_id = translation_tier_id[0]
        # except:
        #     error_box[dialect] = "Translation tier id is not defined for {}".format(dialect)
        # here we continue to process if translation does not exist
        annotations_data = eaf.get_ref_annotation_data_for_tier(translation_tier_id)
        item_numbers = eaf.get_annotation_data_for_tier(item_number_tier)
        url = eaf.get_linked_files()[0]['RELATIVE_MEDIA_URL']
        year, month, day = find_date_components(url)
        for i, annotation_data in enumerate(annotations_data):
            s, e, n, t = annotation_data # here we get the starting point (s), ending point (e), number of clip (n), translation (t)
            
            data = {}
            data['start'] = s
            data['end'] = e
            data['eng_translation'] = n
            data['ir_translation'] = t
            data['order'] = i
            data['url'] = url
            data['speaker'] = speaker
            data['language'] = dialect
            data['year'] = year
            data['item_number'] = item_numbers[i]
            
            total_data.append(data)
            
    return total_data
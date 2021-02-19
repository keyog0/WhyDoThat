def remove_blank(data) :
    return data.replace(' ','')

def remove_line_change(data) :
    return data.replace('\n','')

def remove_blank_all(data) :
    return data.replace('\n','').replace(' ','')

def remove_xa0(data) :
    return data.replace('\xa0',' ')

def style_image_parse(data) :
    return [url.split()[1].split('"')[1] for url in data]

def wave_split(data,remove,wave_type='~') :
    return data.replace(' ','').replace(',','').replace(remove,'').split(wave_type)

def arr2str(array) :
        return ','.join(array)
    
    
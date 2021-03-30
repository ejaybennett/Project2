import re
#if no indicator, give it!
def indicatorFromValue(value):
    if re.match(r"""[0-9]{2,3}/[0-9]{2,3}""",str(value))!=None:
        return "blood pressure"
    elif re.match(r"""[0-9]{2,3}\s[0-9]{2,3}/[0-9]{2,3}""",str(value))!=None:
        return "weight"
    elif (float(value) > 45 and float(value) < 78):
        return "height"
    if (float(value) > 95.0 and float(value) < 106) or (float(value) > 36 and float(value) < 39):
        return "temperature"
    elif float(value) < 31 and float(value)>10:
        return "respirations"
    elif float(value) > 40 and float(value) < 180:
        return "pulse"
    elif float(value) > 90 and float(value) < 400:
        return "weight"
    else:
        return "unknown"
#convert kg to lb, c to f, cm to in
def valueFromUnit(value,unit):
    try:
        value = float(value)
    except:
        pass
    if unit in {'c','celsius'}:
        return  value*9/5+32
    elif unit in {"cm","centimeters"}:
        return value*0.3937
    elif unit in {"meter","m"}:
        return value*39.37
    elif unit in {"feet","ft"}:
        return value*1/12
    elif unit in {"kg","kilo","kilogram"}:
        return value*2.20462
    else:
        return value

def hasGroup(match,group):
    try:
        match.group(group)
        return True
    except IndexError:
        return False

def isSignAcceptable(sign, value):
    return True
#if dic is a dictionary with values aslists s, returns a dictionary with keys each
#value in collection of dic and value what keys those correspeonded to in dic AND
#the keys in dic with values themself
def invert_dictionary(dic):
    assert(type(dic) == dict)
    flipped = {}
    for k in dic.keys():
        v = dic[k]
        if type(v) == list:
            for n in v+[k]:
                flipped[n] = k
        else:
            fliped[v] = k
    return flipped
def extractVitalSign(text):
    out = {}
    text = text.lower()
##    vitalIndicators = ["beats per minute","heart rate","pulse","p",
##                       "white blood cell", "white blood cell count", "wbc count","white blood count","wbc",
##                       "o2","blood oxygen","oxygen saturation","spo2","oxygen", "oximeter","sao2","o2 sat","ox sat",
##                       "respirations","resperation rate", "resperation","rp",
##                       "blood pressure","bp",
##                       "weight","wt",'weighs','pound','lb',
##                       "height","ht",
##                       "body mass index","bmi",
##                       "hematocrit","packed cell volume","htc","pcv",
##                       "cholestrol","chol","blood cholestrol","blood chol",
##                       "calcium",
##                       "potassium",
##                       "hemoglobin","hemoglobic a1c",
##                       "sodium",
##                       "co2","carbon monoxide",
##                       "chloride",
##                       "phosphorus",
##                       "magnesium",
##                       "glucose", "blood glucose",
##                       "temperature", "temp","fever"]
    #vitalAcronyms = {"".join([w[0] for w in v.split()]):v for v in vitalIndicators if len(v)>4}
    indicatorDictionary = {
        "beats per minute":["heart rate","pulse","p","bpm","beats"],
        "white blood cell":[ "white blood cell count", "wbc count","white blood count","wbc"],
        "o2":["blood oxygen","oxygen saturation","spo2","sp o2","oxygen", "oximeter","sao2","sa o2","o2 sat","ox sat","oxi"],
        "respirations":["resperation rate", "resperation","rp","respiratory rate","resp rate"," r rate"],
        "blood pressure":["bp"],
        "weight":["wt",'weighs','pound','lb','pounds'],
        "height":["ht","in","inch","cm","'","meter","feet","ft", "foot", "inches"],
        "body mass index":["bmi"],
        "hematocrit":["packed cell volume","htc","pcv"],
        "cholestrol":["chol","blood cholestrol","blood chol"],
        "calcium":[],
        "potassium":[],
        "hemoglobin":["hemoglobic a1c"],
        "sodium":[],
        "co2":["carbon dioxide",],
        "chloride":[],
        "phosphorus":[],
        "magnesium":[],
        "glucose":["blood glucose","sugar","bg"],
        "temperature":[ "temp","fever", "degrees","f ","farenheit","c ","celsius"],
        "unknown":[]
        }
    vitalIndicators = list(indicatorDictionary.keys())
    for k in indicatorDictionary.keys():
        vitalIndicators += indicatorDictionary[k]
    indicatorDictionary = invert_dictionary(indicatorDictionary)
    #print(indicatorDictionary)
    indicatorExpr = "|".join(vitalIndicators).lower()
    #What does a number look like?
    valueExpr = r"""[0-9]{1,3}((/|\.)[0-9]{1,3}([0-9]|/{1,3})?)?"""
    #expr = r"""(P<indicator>""" +indicatorExpr+ """)\s?(is|at|:)?\s?(P<val>[0-9]{1,3}(/[0-9]{1,3})?)"""
    #This expression is for indicators in the format indicator __ format
    expr = r"""(^|\s)(?P<indicator>""" +indicatorExpr+ """)\s?('s|is|at|about|of|lab|was|measured|left|arm|right|seated|standing|
are|test|level|\(|\)|,|stat|-|=|rate|amount|of|\s|reading|:)*\s?(?P<val>"""+valueExpr+r""")\s?""" + \
r"""(?P<unit>mg/hg|celsius|c|farenheit|f |kg|kilo|lb|measured|today|hormone|pound|pounds|degree|bpm)?"""
    #print(expr)
    matches = list(re.finditer(expr,text))
    #Sometimes, indicators are after
    expr = r"""(^|\s)(?P<val>[0-9]{1,3}((/|\'|\.|\s)([0-9]|/){1,3})?)\s*(degree|of|at)?\s*(?P<indicator>fever|lb|'|inches|feet|foot|beats|pounds|pound|c |celcius|f |in|bpm)"""
    matches = matches +list(re.finditer(expr,text))
    expr = r"""(physical exam|exam|vital sign|vitals|vital signs)(\s|:|-)+(""" +valueExpr+ r"""|in|'|inches|feet|\s|lb|pound|pounds){0,5}(\s|,)+(?P<val>"""+valueExpr\
           + r""")\s?(?P<indicator>""" +indicatorExpr+ """)?"""
    #expr = r"""(physical exam|exam|vital sign|vitals|vital signs)(\s|:|-)+(bpm|p|pulse|temp|temperature|bp|\.|/|[0-9]|blood pressure|height|weight|in|'|inches|\
#feet|\s|,|lb|pound|pounds|'|"|ft|f|c|celsius){0,10}(\s|,)(?P<val>"""+valueExpr+ r""")\s?(?P<indicator>""" +indicatorExpr+ """)?"""
    theMatch = re.search(expr,text)
    if theMatch != None:
        theMatch = theMatch.group()
        #print(theMatch)
        expr = r"""(?P<val>"""+valueExpr+ r""")\s?(?P<indicator>""" +indicatorExpr+ """)?"""
        matches = matches +list(re.finditer(expr,theMatch))
    #print(indicatorExpr)
    #print(valueExpr)
    #matches = matches +list(re.finditer(expr,text))
    #indicatorDictionary = vitalAcronyms
    #print(matches)
    #for k in vitalIndicators:
    #    if k not in indicatorDictionary.keys():
            #print(k, "is missing from indicator dictionary!")
    assert all([k in indicatorDictionary.keys() for k in vitalIndicators])
    for m in matches:
        #print(m)
        value = m.group("val").strip()
        indicator = m.group("indicator")
        if indicator == None:
            indicator = indicatorFromValue(value)
        if hasGroup(m,"unit"):
            unit = m.group("unit")
        else:
            unit = None
        if unit != None:
            unit = m.group("unit").strip()
        try:
            value = valueFromUnit(value,unit)
        except:
            pass
        indicator = indicatorDictionary[indicator]
        if isSignAcceptable(value,indicator):
            out[indicator] = value
    for indicator in out.keys():
        try:
            out[indicator] = float(out[indicator])
        except:
            #print("something failed!")
            continue
    return out

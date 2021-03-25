import re
#convert lb to kg,
def valueFromUnit(value,unit):
    try:
        value = float(value)
    if unit in {'c','celsius'}:
        return  value*9/5+32
    elif unit in {"kg","kilo","kilogram"}:
        return value*2.20462
    else:
        return value
def isSignAcceptable(sign, value):
    return True
def extractVitalSignFromText(text):
    out = {}
    text = text.lower()
    vitalIndicators = ["beats per minute","heart rate","pulse","p"
                        "white blood cell", "white blood cell count", "wbc count","wbc",
                       "o2","blood oxygen","oxygen saturation","spo2","oxygen", "oximeter","sao2","o2 sat","ox sat"
                       "respirations","resperation rate", "resperation","rp"
                       "blood pressure","bp"
                       "weight","wt",
                       "height","ht",
                       "body mass index","bmi",
                       "hematocrit","packed cell volume","htc","pcv"
                       "cholestrol","chol","blood cholestrol","blood chol",
                       "calcium",
                       "potassium",
                       "hemoglobin","hemoglobic a1c",
                       "sodium",
                       "co2","carbon monoxide",
                       "chloride",
                       "phosphorus",
                       "magnesium",
                       "glucose", "blood glucose",
                       "temperature", "temp","fever"]
    #vitalAcronyms = {"".join([w[0] for w in v.split()]):v for v in vitalIndicators if len(v)>4}
    indicatorDictionary = {
        "beats per minute":"beats per minute",
        "heart rate":"beats per minute",
        "pulse": "beats per minute",
        "resperation rate": "resperation rate"
        }
    forExpr = "|".join(vitalIndicators+list(vitalAcronyms.keys())).lower()
    #expr = r"""(P<indicator>""" +forExpr+ """)\s?(is|at|:)?\s?(P<val>[0-9]{1,3}(/[0-9]{1,3})?)"""
    expr = r"""(^|\s)(?P<indicator>""" +forExpr+ """)\s?('s|is|at|lab|was|
are|test|level|\(|\)|,|stat|-|=|rate|amount|of|reading|:)*\s?(?P<val>[0-9]{1,3}((/|\.)[0-9]{1,3})?)\s?\
(?P<unit>mg/hg|celsius|c|farenheit|f|kg|kilo|lb|measured|today|hormone|pound|pounds|degree|bpm)?"""
    #print(expr)
    matches = list(re.finditer(expr,text))
    indicatorDictionary = vitalAcronyms
    sometimesAfter = ["fever", "pounds"]
    assert all( for k in indicatorDictionary.keys())
    for m in matches:
        value = m.group("val")
        indicator = m.group("indicator")
        unit = m.group("unit")
        value = valueFromUnit(value,unit)
        if indicator in vitalAcronyms:
            indicator = vitalAcronyms[indicator]
        if isSignAcceptable(value,indicator):
            out[indicator] = value
    for indicator in out.keys():
        try:
            out[indicator] = float(out[indicator])
        except:
            continue
    return out

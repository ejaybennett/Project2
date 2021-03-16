import re
def isSignAcceptable(sign, value):
    return True
def extractVitalSignFromText(text):
    out = {}
    text = text.lower()
    vitalIndicators = ["Beats Per Minute","heart rate", "White Blood Cell", 
                        "pulse", "O2", "respirations", "blood pressure",
                       "glucose", "blood glucose", "temperature"]
    vitalAcronyms = {"".join([w[0] for w in v.split()]):v for v in vitalIndicators}
    forExpr = "|".join(vitalIndicators+list(vitalAcronyms.keys())).lower()
    #expr = r"""(P<indicator>""" +forExpr+ """)\s?(is|at|:)?\s?(P<val>[0-9]{1,3}(/[0-9]{1,3})?)"""
    expr = r"""(^|\s)(?P<indicator>""" +forExpr+ """)\s?(is|at|:)?\s?(?P<val>[0-9]{1,3}(/[0-9]{1,3})?)"""
    #print(expr)
    matches = list(re.finditer(expr,text))
    for m in matches:
        value = m.group("val")
        indicator = m.group("indicator")
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

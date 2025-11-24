# scoring.py
import re
from .utils import tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import language_tool_python

sentiment_analyzer = SentimentIntensityAnalyzer()

grammar_tool = language_tool_python.LanguageToolPublicAPI('en-US')


RUBRIC_IMAGE_PATH="/mnt/data/8f022ef2-4456-4b09-a530-565c68df177d.png"

SALUTATIONS={
 "excellent":["excited to introduce","feeling great"],
 "good":["good morning","good afternoon","good evening","hello everyone"],
 "normal":["hello","hi"]
}

MUST_HAVE={
 "name":["my name is","i am","myself"],
 "age":["years old","i am","i am"],
 "class_school":["class","school"],
 "family":["family","mother","father","parents"],
 "hobbies":["hobby","hobbies","i like","i enjoy","playing"]
}

GOOD_TO_HAVE={
 "about_family":["about my family"],
 "origin":["i am from"],
 "goal":["goal","dream","ambition"],
 "fun_fact":["fun fact","something unique"],
 "strengths":["strength","achievement","achievements"]
}

FILLER_WORDS=set([
 "um","uh","like","you know","so","actually","basically",
 "right","i mean","well","kinda","sort of","okay","hmm","ah"
])

def _lower(t): return t.lower()

def salutation_points(t):
    t=_lower(t)
    if any(s in t for s in SALUTATIONS["excellent"]): return 5,"Excellent"
    if any(s in t for s in SALUTATIONS["good"]): return 4,"Good"
    if any(s in t for s in SALUTATIONS["normal"]): return 2,"Normal"
    return 0,"No salutation"

def count_kw(text,groups):
    text=_lower(text)
    found=0; items=[]
    for k,plist in groups.items():
        if any(p in text for p in plist):
            found+=1; items.append(k)
    return found,items

def compute_flow(t):
    t=_lower(t)
    keys=["hello","my name","i am","class","school","family","hobby","thank"]
    pos=[t.find(k) for k in keys]
    valid=[p for p in pos if p>=0]
    if valid==sorted(valid) and len(valid)>=3: return 5,"Order followed"
    return 0,"Order not followed"

def compute_wpm(words,sec):
    return words/(sec/60) if sec>0 else 0

def speech_pts(wpm):
    if wpm>161: return 2,f"Too fast {wpm:.1f}"
    if 141<=wpm<=160: return 6,f"Fast {wpm:.1f}"
    if 111<=wpm<=140: return 10,f"Ideal {wpm:.1f}"
    if 81<=wpm<=110: return 6,f"Slow {wpm:.1f}"
    return 2,f"Too slow {wpm:.1f}"

def grammar_pts(t):
    matches=grammar_tool.check(t)
    errors=len(matches)
    words=max(1,len(tokenize(t)))
    errors_100=(errors/words)*100
    score_raw=1-min(errors_100/10,1)
    if score_raw>0.9: pts=10
    elif score_raw>=0.7: pts=8
    elif score_raw>=0.5: pts=6
    elif score_raw>=0.3: pts=4
    else: pts=2
    return pts,errors,score_raw

def ttr_pts(t):
    tokens=tokenize(t.lower())
    if len(tokens)==0: return 2,0.0
    distinct=len(set(tokens))
    ttr=distinct/len(tokens)
    if ttr>=0.9: pts=10
    elif ttr>=0.7: pts=8
    elif ttr>=0.5: pts=6
    elif ttr>=0.3: pts=4
    else: pts=2
    return pts,ttr

def clarity_pts(t):
    tok=tokenize(t.lower())
    total=max(1,len(tok))
    fcount=sum(1 for x in tok if x in FILLER_WORDS)
    rate=(fcount/total)*100
    if rate<=3: pts=15
    elif rate<=6: pts=12
    elif rate<=9: pts=9
    elif rate<=12: pts=6
    else: pts=3
    return pts,rate,fcount

def engagement_pts(t):
    val=sentiment_analyzer.polarity_scores(t)["pos"]
    if val>=0.9: pts=15
    elif val>=0.7: pts=12
    elif val>=0.5: pts=9
    elif val>=0.3: pts=6
    else: pts=3
    return pts,val

def score_transcript(text,sec):
    words=len(tokenize(text))
    spts,smsg=salutation_points(text)
    mcount,mitems=count_kw(text,MUST_HAVE)
    gcount,gitems=count_kw(text,GOOD_TO_HAVE)
    mpts=min(mcount*4,20)
    gpts=min(gcount*2,10)
    fpts,fmsg=compute_flow(text)
    wpm=compute_wpm(words,sec)
    sppts,spmsg=speech_pts(wpm)
    gpts2,ge,gr=grammar_pts(text)
    ttrp,ttrv=ttr_pts(text)
    cpts,crate,ccount=clarity_pts(text)
    epts,epv=engagement_pts(text)
    total=spts+mpts+gpts+fpts+sppts+gpts2+ttrp+cpts+epts
    return {
        "overall_score":total,
        "word_count":words,
        "wpm":round(wpm,2),
        "rubric_image":RUBRIC_IMAGE_PATH,
        "criteria":{
          "salutation":{"points":spts,"detail":smsg},
          "must_have":{"points":mpts,"found":mitems},
          "good_to_have":{"points":gpts,"found":gitems},
          "flow":{"points":fpts,"detail":fmsg},
          "speech_rate":{"points":sppts,"detail":spmsg,"wpm":wpm},
          "grammar":{"points":gpts2,"errors":ge,"raw":gr},
          "ttr":{"points":ttrp,"value":ttrv},
          "clarity":{"points":cpts,"rate":crate,"count":ccount},
          "engagement":{"points":epts,"sentiment":epv}
        }
    }

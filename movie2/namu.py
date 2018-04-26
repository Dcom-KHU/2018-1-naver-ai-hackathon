import ijson
import pandas as pd

filename = 'corpus/namuwiki_20160229.json'
# Read file to memory, it takes some time.
with open(filename, 'r') as f:
    objects = ijson.items(f, 'meta.view.columns.item')
    columns = list(objects)

# this black list article does not contain natural language knowledge
black_list_title = ['공지사항/차단 내역/통합본']

# Article contains title, text, and other things
# Let's extract title and text from several articles
for i in range(3):
    print(data[i]['title'])
    print(data[i]['text'])
    print()

# Using regular expression, we can strip some grammar. Let's see how we can do it. 
import re
text = "딴 사람도 아니고 프로팀 [[Counter Logic Gaming|CLG]] 소속 전 서포터 [[스티브 차우|차우스터]]가 남긴 말이다."
t1 = re.sub(r"\[\[([^\]|]*)\]\]", r'\1', text) # remove link
print(t1)
t2 = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]+)\]\]", r'\1', text) # remove link
print(t2)

def strip(text):               
    text = re.sub(r"\{\{\{#\!html[^\}]*\}\}\}", '', text, flags=re.IGNORECASE|re.MULTILINE|re.DOTALL) # remove html
    text = re.sub(r"#redirect .*", '', text, flags=re.IGNORECASE) # remove redirect
    text = re.sub(r"\[\[분류:.*", '', text) # remove 분류
    text = re.sub(r"\[\[파일:.*", '', text) # remove 파일
    text = re.sub(r"\* 상위 문서 ?:.*", '', text) # remove 상위문서        
    text = re.sub(r"\[youtube\(\w+\)\]", '', text, flags=re.IGNORECASE) # remove youtube
    text = re.sub(r"\[include\(([^\]|]*)(\|[^]]*)?\]", r'\1', text, flags=re.IGNORECASE) # remove include
    text = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]|]+)\]\]", r'\1', text) # remove link
    text = re.sub(r"\[\*([^\]]*)\]", '', text) # remove 각주
    text = re.sub(r"\{\{\{([^\ }|]*) ([^\}|]*)\}\}\}", r'\2', text) # remove text color/size
    text = re.sub(r"'''([^']*)'''", r'\1', text) # remove text bold
    text = re.sub(r"(~~|--)([^']*)(~~|--)", '', text) # remove strike-through
    
    text = re.sub(r"\|\|(.*)\|\|", '', text) # remove table
                                   
    text = chinese.sub('', text) # remove chinese
    text = japanese.sub('', text) # remove japanese
    return text

for i in range(2):
    print(data[i]['title'])
    # print(data[i]['text'])
    print(strip(data[i]['text']))
    print()

# Generate raw text corpus

MIN_TEXT_SIZE = 5000

count = 10
with open('input.txt', 'w') as f:
    for article in data:
        if len(article['text']) < MIN_TEXT_SIZE or len(article['text']) >= MAX_ARTICLE_SIZE:        
            continue # skip too small, too large articles

        text = strip(article['text'])
        f.write("%s\n%s\n\n\n" % (article['title'], text))
        # print(article['title'])
        # print(article['text'])
        # print(text)
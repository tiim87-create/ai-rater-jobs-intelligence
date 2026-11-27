import argparse,json,re
from pathlib import Path
from bs4 import BeautifulSoup

def parse(paths,date):
    rows=[]; ranges=[]; total=None
    for path in paths:
        soup=BeautifulSoup(Path(path).read_text(encoding='utf-8'),'html.parser')
        label=soup.select_one('#facet-jobs-loaded')
        m=re.fullmatch(r'Showing\s+(\d+)-(\d+)\s+of\s+(\d+)\s+results',label.get_text(strip=True))
        start,end,n=map(int,m.groups())
        if total is not None and total!=n: raise ValueError('Inconsistent totals')
        total=n; ranges.append((start,end))
        cards=soup.select('a.jobs-section__item')
        if len(cards)!=end-start+1: raise ValueError('Page count mismatch')
        for a in cards:
            fields=[' '.join(x.split()) for x in a.select_one('.paragraph-4').get_text().split('•')]
            if len(fields)!=4: raise ValueError('Unexpected listing fields')
            rows.append(dict(page=(start-1)//25+1,title=' '.join(a.select_one('h4').get_text().split()),url=a['href'],fields=fields))
    expected=1
    for start,end in sorted(ranges):
        if start!=expected: raise ValueError('Missing or overlapping pages')
        expected=end+1
    if expected!=total+1 or len(rows)!=total: raise ValueError('Incomplete catalog')
    if len({r['fields'][3] for r in rows})!=total or len({r['url'] for r in rows})!=total: raise ValueError('Duplicate listings')
    return dict(date=date,source='https://jobs.telusdigital.com/search/cfm5/ai-community/jobs/in',reported_total=total,jobs=sorted(rows,key=lambda r:r['page']))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--date',required=True);p.add_argument('--output',required=True);p.add_argument('paths',nargs='+');a=p.parse_args();d=parse(a.paths,a.date);Path(a.output).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n');print('PASS',len(d['jobs']))

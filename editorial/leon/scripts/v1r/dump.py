import fitz,sys
L=sys.argv[1]
d=fitz.open(f'ref/leons-thinking-book-vol1-{L}-interior.pdf')
for i,p in enumerate(d):
    sp=sorted([(round(s['bbox'][1]),round(s['bbox'][0]),s['text'].strip()) for b in p.get_text('dict')['blocks'] for l in b.get('lines',[]) for s in l['spans'] if s['text'].strip()])
    print(f"## p{i+1}: "+" | ".join(t for y,x,t in sp))

import sys, urllib.request
url = sys.argv[1] if len(sys.argv) > 1 else 'https://example.com'
req = urllib.request.Request(url, headers={'User-Agent': 'mycurl/1.0'})
with urllib.request.urlopen(req) as res:
    print(f'HTTP Status: {res.status}')
    for k, v in res.headers.items(): print(f'{k}: {v}')
    print('\n' + res.read().decode('utf-8', errors='ignore')[:1000])

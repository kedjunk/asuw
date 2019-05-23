#!usr/bin/python2
# encoding: utf-8

from multiprocessing.pool import ThreadPool
import requests
import re
import sys

ua = 'Mozilla/5.0 (Linux; Android 8.1.0; Redmi 6A Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 YaBrowser/18.10.2.119.00 Mobile Safari/537.36'

def check(i):
    s = requests.Session()
    html = s.get('https://appleid.apple.com/account#!&page=create',
              headers={
                  'User-agent': ua,
                  'Referer': 'https://appleid.apple.com/account',
                  'Accept-Encoding': 'gzip, deflate, sdch, br',
                  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
                }
            )
    data = dict(zip(['scnt', 'apikey', 'sessionid'], re.findall(r'(?i)(?:scnt|apikey|sessionid): \'(.*?)\'', html.text)))
    res = s.post('https://appleid.apple.com/account/validation/appleid', 
             headers={'User-agent': ua,
                      'Origin': 'https://appleid.apple.com',
                      'Referer': 'https://appleid.apple.com/account',
                      'X-Apple-Request-Context': 'create',
                      'Requested-With': 'XMLHttpRequest',
                      'scnt': data['scnt'],
                      'X-Apple-Api-Key': data['apikey'],
                      'X-Apple-ID-Session-Id': data['sessionid'],
                      'Accept': 'application/json, text/javascript, */*; q=0.01',
                      'Accept-Encoding': 'gzip, deflate, br',
                      'Accept-Language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
                      'Content-Type': 'application/json',
                      'X-Apple-I-FD-Client-Info': '{"U":"%s","L":"id-ID","Z":"GMT+07:00","V":"1.1","F":"kWa44j1e3NlY5BSo9z4ofjb75PaK4Vpjt1szHVXU3vtnTDovyhbQ3zIRbPhj03x.dXnYbFdH6PEwHXXTSHCSPmtd0wVYPIG_qvoPfybYb5EvYTrYesR2hQnH6hAOfUftmF5wMQE5nXxQD6CKaMhQWx2KlTTpZHgfLMC7AeLd7FmrpwoNN5uQ4s5uQ1szHVzZrefOJQuyPB94UXuGlfUm4ly_03y8rnawSdrxQDq8yatDpQT18u0I4b6DWHZDoUs_43wuZPup_nH2t05oaYAhrcpMxE6DBUr5xj6Kks6PraZEPLnLzMnZVCsiqTCb4uqRDPfBjPr2u5fXwxf7_OLgiPFMqbN0TUMpwoNRe98vPSb_GGEOpBSKxUC56MnGWpwoNSUC53ZXnN87gq1a293lio8dOHr_i.uJtHoqvynx9MsFyxYMH0XKJ7lrHay.9aB.KB4D93tG2hixAwlMsITxYMJ5uFBHeNNW5BNlYicklY5BqNAE.lTjV.5Ec"}' % ua
                      },
             data='{"emailAddress": "' + i[1] + '"}'
             )

    stat = '\x1b[33mUNCHECK'
    owndmn, rscd = '', ''
    ui = '[ '

    if res:
        stat = '\x1b[31;1mUNKNOW'
        res = res.json()
        if res['valid']:
            stat = '\x1b[31mDIE'
            if res['used']:
                stat = '\x1b[32mLIVE'
                open('valid_apple.txt', 'a').write(i[1] + '\n')
                
            ui += ('{0}\x1b[0m ] Thread-{1}: {2}'.format(stat, i[0], i[1]))
            if res['appleOwnedDomain']:
                ui += ' [apple owned domain]'
            if res['isRecycledDomain']:
                ui += ' [Recycled Domain]'
    print (ui)


file = raw_input('?: email list: ')
threads = raw_input('?: threads (int): ')

print ('') # new line
p = ThreadPool(int(threads))
p.map(check, [(num, x.strip()) for num, x in enumerate(open(file).readlines(), start=1)])

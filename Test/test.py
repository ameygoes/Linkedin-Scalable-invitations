import requests
s = requests.Session()
token = s.cookies.get_dict().get('JSESSIONID').replace('"','')
headers = {
        'accept': 'application/vnd.linkedin.normalized+json+2.1',
        'csrf-token': token,
        'dnt': '1',
        'referer': 'https://www.linkedin.com/search/results/people/?facetCurrentCompany=%5B%22{}%22%5D&origin=COMPANY_PAGE_CANNED_SEARCH&page={}'.format(company_id, page_no),
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'x-li-lang': 'en_US',
        'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_people;dhIfWyZ7T8m+SR5/ck6/vw==',
        'x-li-track': '{"clientVersion":"1.7.3019","osName":"web","timezoneOffset":6,"deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1366,"displayHeight":768}',
        'x-restli-protocol-version': '2.0.0'
}
resp = self.s.get('https://www.linkedin.com/voyager/api/search/blended?count=10&filters=List(currentCompany-%3E{},resultType-%3EPEOPLE)&origin=COMPANY_PAGE_CANNED_SEARCH&q=all&queryContext=List(spellCorrectionEnabled-%3Etrue)&start={}'.format(company_id,(int(page_no)-1) * 10), headers=headers).json()
print(resp)
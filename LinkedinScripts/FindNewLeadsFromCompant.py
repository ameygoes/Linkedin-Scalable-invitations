# -*- coding: utf-8 -*-
# Last Changed: 30-09-2020
# Author: Tufayel Ahmed
# Github: https://www.github.com/TufayelLUS
# LinkedIn: https://www.linkedin.com/in/tufayel-ahmed-cse/
# For paid web scraping projects, contact in LinkedIn!
# Follow me in github for more premium projects!
# This script collects all *COMPANY WISE* profiles listed in linkedin
# It collects profile details along with their email addresses

import json
import requests
import re
import csv
import os
from urllib.parse import quote


# Script Configuration
linkedin_email = os.environ.get("LINKED_IN_UN_2") # place your linkedin login email
linkedin_password = os.environ.get("LINKED_IN_PASS_2") # place your linkedin login password
target_company_link = "https://www.linkedin.com/company/barclays-bank/" # place company URL in mentioned format only! do not remove trailing slash
# End Script Configuration

class LinkedIn:

    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36 OPR/67.0.3575.97"
            }

    
    def login(self,email,password):
        # creates a session
        try:
            sc = self.s.get("https://www.linkedin.com/login", headers=self.headers).text
        except:
            return False
        csrfToken = sc.split('csrfToken" value="')[1].split('"')[0]
        sid = sc.split('sIdString" value="')[1].split('"')[0]
        pins = sc.split('pageInstance" value="')[1].split('"')[0]
        lcsrf = sc.split('loginCsrfParam" value="')[1].split('"')[0]
        data = {
            'csrfToken': csrfToken,
            'session_key': email,
            'ac': '2',
            'sIdString': sid,
            'parentPageKey': 'd_checkpoint_lg_consumerLogin',
            'pageInstance': pins,
            'trk': 'public_profile_nav-header-signin',
            'authUUID': '',
            'session_redirect': 'https://www.linkedin.com/feed/',
            'loginCsrfParam': lcsrf,
            'fp_data': 'default',
            '_d': 'd',
            'showGoogleOneTapLogin': 'true',
            'controlId': 'd_checkpoint_lg_consumerLogin-login_submit_button',
            'session_password': password,
            'loginFlow': 'REMEMBER_ME_OPTIN'
            }
        try:
            after_login = self.s.post("https://www.linkedin.com/checkpoint/lg/login-submit",headers=self.headers,data=data).text
        except:
            return False
        is_logged_in = after_login.split('<title>')[1].split('</title>')[0]
        if is_logged_in == "LinkedIn":
            return True
        else:
            return False

    def bulkScan(self, profiles):
        # scans a list of profiles for email
        all_emails = []
        for profile in profiles:
            profile = profile + "/detail/contact-info/"
            sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
            emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+',sc)
            all_emails.extend(emails_found)
        return all_emails

    def singleScan(self, profile):
        # scans a single account for email
        profile = profile + "/detail/contact-info/"
        sc = self.s.get(profile, headers=self.headers, allow_redirects=True).text
        emails_found = re.findall(r'[a-zA-Z0-9\.\-\_i]+@[\w.]+',sc)
        return emails_found

    def saveRecord(self, data):
        with open('leads.csv', mode='a+', encoding='utf-8', newline='') as csvFile:
            fieldnames = ["Profile Link", "Full Name", "Headline", "Country"]
            writer = csv.DictWriter(csvFile, fieldnames=fieldnames)
            if os.stat('leads.csv').st_size == 0:
                writer.writeheader()
            writer.writerow({"Profile Link":data[0], "Full Name":data[1], "Headline":data[2], "Country":data[3]})

    def saveEmail(self, email):
        with open('emails.csv', mode='a+', encoding='utf-8') as emFile:
            if os.stat('emails.csv').st_size == 0:
                emFile.write("Email\n")
            emFile.write(email + "\n")



    def listProfiles(self, company_id, page_no, need_count=False):
        token = self.s.cookies.get_dict().get('JSESSIONID').replace('"','')
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
        print(json.dumps(resp, indent=4, sort_keys=True))
        profiles = resp.get('data').get('elements')[0].get('elements')
        all_profile_links = []
        if need_count:
            page_count = resp.get('data').get('paging').get('total')
        for profile in profiles:
            print(f"================= \n Printing Profile: \n {profile}")
            person_name = profile.get('title').get('text')
            profile_link = profile.get('navigationUrl')
            headline = profile.get('headline').get('text')
            country = profile.get('subline').get('text')
            print("Profile Link: {}".format(profile_link))
            print("Full Name: {}".format(person_name))
            print("Headline: {}".format(headline))
            print("Country: {}".format(country))
            data = []
            data.append(profile_link)
            data.append(person_name)
            data.append(headline)
            data.append(country)
            # self.saveRecord(data)
        if need_count:
            return all_profile_links, page_count
        else:
            return all_profile_links

    def getCompanyID(self, company_link):
        try:
            company_username = company_link.split('.com/company/')[1].replace('/','')
        except:
            print("Wrong Company URL. Company Format should be https://www.linkedin.com/company/company_Username/!")
            return None
       
        token = self.s.cookies.get_dict().get('JSESSIONID').replace('"','')
        headers = {
            'csrf-token': token,
            'referer': 'https://www.linkedin.com/',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
        }
        api_link = 'https://www.linkedin.com/voyager/api/organization/companies?decorationId=com.linkedin.voyager.deco.organization.web.WebCompanyStockQuote-2&q=universalName&universalName={}'.format(quote(company_username))
        resp = self.s.get(api_link, headers=headers).json()
        company_id = resp.get('elements')[0].get('entityUrn').split(':')[-1]
        return company_id



if __name__ == "__main__":
    connection = LinkedIn()
    login_state = connection.login(linkedin_email, linkedin_password)
    if login_state:
        print("Logged in to LinkedIn!")
        company_id = connection.getCompanyID(target_company_link)
        if company_id is not None:
            print("Collecting all company member profiles upto 10000!")
            profile_list, page_count = connection.listProfiles(company_id, 1, True)
            print("=============================== COMPANY list profile response ===============================")
            print(profile_list, page_count)
            # for page_no in range(2,page_count+1):
            #     profile_list.extend(connection.listProfiles(company_id, page_no))
            # print("Profile list collected and saved! Extracting emails ...")
            # all_emails = connection.bulkScan(profile_list)
            # for email in all_emails:
            #     print(email)
            #     connection.saveEmail(email)
    else:
        print("Unable to login to LinkedIn!")
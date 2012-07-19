#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import tweepy
import time
from datetime import timedelta,datetime
from gmailsend import *
import urllib2
import json
import webbrowser
from optparse import OptionParser

def parse_options():
    parser = OptionParser()
    parser.add_option(
            '-d','--destination',
            action='store',
            dest='send_to',
            default=None,
            help='mail address to send alarm')
    parser.add_option(
            '-u','--user',
            action='store',
            dest='gmail_user',
            default=None,
            help='Gmail User Name')
    parser.add_option(
            '-p','--passwd',
            action='store',
            dest='gmail_pw',
            default=None,
            help='Gmail password')
    (options, args) = parser.parse_args()
    return options

class SearchWord(object):
    def __init__(self, word, send_to, gmail_user, gmail_pw):
        self.api = tweepy.API()
        self.ids = []
        self.word = word
        self.send_to = send_to
        self.gmail_user = gmail_user
        self.gmail_pw = gmail_pw

    def search(self, mail=None):
        ids_new = []
        new_tweets = []
        print '*'*5,'Search',self.word,'*'*5
        try:
            tweets = self.api.search(self.word)
        except:
            print 'Can not get tweet from search api...'
            return -1
        for tweet in reversed(tweets):
            if not self.find_in_text(tweet.text,['譲','通し','3日','３日','チケ']):
                continue
            ids_new.append(tweet.id_str)
            if not tweet.id_str in self.ids:
                new_tweets.append(tweet)
                print '>',tweet.from_user
                print '>',
                print (tweet.created_at + timedelta(hours=9)).\
                        strftime('%Y-%m-%d %H:%M:%S')
                print 
                print tweet.text
                print '-'*50
        if new_tweets:
            print '   --> ','NEW TWEET FOUND!!'
            if mail:
                self.send_mail(new_tweets, mail_type=mail)
        self.ids = ids_new[:]
        limit = self.api.rate_limit_status()
        print limit['remaining_hits'],'/',
        print limit['hourly_limit'],
        print 'reset_time',
        print datetime.fromtimestamp(limit['reset_time_in_seconds']).\
                strftime('%Y-%m-%d %H:%M:%S')

    def find_in_text(self, text, words):
        for word in words:
            if text.find(word) != -1:
                return True
        return False

    def send_mail(self, tweets, mail_type):
        title = 'New Tweets fuji!'
        body = ''
        for tweet in tweets:
            body+= tweet.text + '\n\n'
            body+= '> @{0} :\n'.format(tweet.from_user)
            body+= '> {0}\n'.format((tweet.created_at+timedelta(hours=9)).\
                    strftime('%Y-%m-%d %H:%m:%d'))
            url = self.shorten_url(tweet)
            body+= url + '\n'
            webbrowser.open(url)
            body+= '---\n'
        body+= '\n'
        body+= '**********'
        body+= '\n'
        body+= 'search word: \n'
        body+= self.word + '\n'
        print 'sending to {0}... '.format(self.send_to)
        if mail_type == 'gmail':
            sg = sendGmail('utf-8',title, body, \
                    self.gmail_user, self.send_to, \
                    self.gmail_user, self.gmail_pw)
        else:
            #TODO: nomal mail send
            pass
        try:
            sg.sendMail()
        except:
            print 'Can not send mail...'
        else:
            print 'sent!'
    
    def shorten_url(self, tweet):
        api_url = 'https://www.googleapis.com/urlshortener/v1/url'
        origin_url = 'https://twitter.com/intent/tweet?in_reply_to='
        origin_url+= tweet.id_str
        req = urllib2.Request(api_url, '{longUrl:"%s"}' % origin_url)
        req.add_header('Content-Type', 'application/json')
        result = urllib2.urlopen(req)
        return json.load(result).get('id')

def make_word(word_list):
    return ' OR '.join(word_list) + ' -RT'

def sleep(n):
    for i in range(n):
        if i < n / 2:
            print '.',
        elif i < n * 3 / 4:
            print '_',
        else:
            print '*',
        sys.stdout.flush()
        time.sleep(1)
    print 

if __name__ == '__main__':    
    word1 = make_word(['フジ','fuji'])

    opt = parse_options()
    
    mail_type = None
    if opt.send_to:
        mail_type = 'mail'
        if opt.gmail_user and opt.gmail_pw:
            mail_type = 'gmail'
    
    search1 = SearchWord(word1, opt.send_to, opt.gmail_user, opt.gmail_pw)
    
    while True:
        search1.search(mail=mail_type)
        sleep(15)

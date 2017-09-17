import twitter

## REDOWNLOAD WHEN THEY HAVE FIXED THE TWITTER_MODE='EXTENDED' ISSUE

class Twitter_Page():


    def __init__(self):

        # replace with your own keys
        self.api = twitter.Api(consumer_key='',
                  consumer_secret='',
                  access_token_key='',
                  access_token_secret='',
                  )

    def convert(self, string):
        string = string.encode('ascii', 'ignore').decode('utf-8')
        return string

    def verify(self):
        """ verifies the keys work, returns true if has access to twitter,
        false if not """

        verify_dict = self.api.VerifyCredentials().AsDict()
        return verify_dict['screen_name'] == "Xavier_Spade"  


    def get_posts(self):
        """ returns an array of the twitter statuses of WakeUp2Politics """ 

        statuses = self.api.GetUserTimeline(screen_name='WakeUp2Politics') 
        return [self.convert(s.text) for s in statuses] 


if __name__ == '__main__':

    api = Twitter_Page() 
    print(api.verify())
    print('----------------- POSTS --------------------')
    print(api.get_posts())


































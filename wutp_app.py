import os
from tkinter import *
from tkinter import ttk 
from twitter_info import Twitter_Page 
from wutp import Wutp 

class App(Tk):
    
    # -- bullet point symbols
    BLACK_CIRCLE = '\u25CF'
    BLACK_DIAMOND = '\u25C6' 
    BLACK_TRIANGLE = '\u25BA'
    BLACK_PARALLEL = '\u25B0'

    def __init__(self):
        super().__init__()

        # -- getting current directory 
        self.directory = os.path.dirname(os.path.realpath('__file__'))

        # -- more taller than wider 
        self.width = 1000 
        self.height = 600 
        self.geometry('%dx%d' % (self.width, self.height))
        
        self.title('Wake Up To Politics v1') 
       
        self.config()

        # -- getting all urls in order
        self.urls = Wutp.get_ordered_urls()
        
        # -- getting all the dates in order 
        self.dates = Wutp.get_dates() 

        # -- setting article counter, newest is 0
        self.current_article = 0

        self.draw_article(self.urls[self.current_article]) 


    def draw_article(self, url):
        """ puts content of an article on a canvas """
       
        self.draw_header()         
        self.draw_twitter_feed() 
        self.draw_canvas()

        # -- getting newsletter data   
        wutp = Wutp(url) 
        content = wutp.traverse()
      
        # -- setting a symbol to place before each point
        symbols = [self.BLACK_CIRCLE, self.BLACK_DIAMOND, self.BLACK_TRIANGLE,
                self.BLACK_PARALLEL]
        symbol_counter = 0
      
        # -- adding it to the canvas
        for heading,points in content.items():
            self.draw_heading(heading) 
            for point in points:
                current_symbol = symbol_counter % 4
                self.draw_point(point, symbol=symbols[current_symbol])

            # -- iterate to next symbol after each heading
            symbol_counter += 1 
        
        # -- update the window and get the bounding box for the widgets and set
        # -- that as the scrolling region for the scrollbar
        self.update()
        self.canvas.configure(scrollregion=self.canvas.bbox("all")) 
        self.twitter_canvas.configure(scrollregion=self.twitter_canvas.bbox("all"))

        # -- adding button
        self.draw_buttons() 
    
    def draw_twitter_feed(self):

        self.draw_twitter_canvas()
        
        twitter_page = Twitter_Page()
        tweets = twitter_page.get_posts() 

        for tweet in tweets:
            self.draw_tweet(tweet) 





    def draw_canvas(self):
        """ draws canvas with a frame and a scrollbar in the root window """

        self.canvas = Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient= VERTICAL,
                command=self.canvas.yview) 
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # make sure to add scrollbar before adding the canvas
        self.scrollbar.pack(side=RIGHT, fill=Y)
        self.canvas.pack(side=TOP, fill=BOTH, expand=1, padx=20, pady=20)
       
        # adding a frame to hold all the widgets, ttk Frame doesn't support
        # background config option 
        self.frame = Frame(self.canvas) 
        self.canvas.create_window(0,0,window=self.frame, anchor='nw')
        

    def draw_heading(self, heading):
        """ draws a heading onto the canvas """ 

        heading_label = ttk.Label(self.frame, text=heading, background="blue",
                foreground="white", anchor=CENTER)
        
        heading_label.configure(font=('Times', 15, "bold"))
        heading_label.configure(wraplength=self.width) 
        heading_label.pack(side=TOP, fill=X, ipady=10)

    def draw_point(self, point, symbol='\u25CF'):
        """ draws a point onto the canvas in a Text widget, can take a symbol
        as a parameter with which to place before the point """ 
        
        point_box = Text(self.frame, bg="white", fg="black", wrap=WORD,
                height=8, font=('arial', 14), pady=5, padx=20)

        point_box.insert(1.0, symbol + ' ')
        point_box.insert('insert', point)
        point_box.configure(state='disabled')
        point_box.pack(side=TOP, fill=X)

    def draw_header(self):
        """ draws the header which has the date """
        
        HEADER_COLOR = 'grey'

        self.header_frame = Frame(self, background=HEADER_COLOR)

        # -- adding the date 
        article_date = self.dates[self.current_article] 
        
        date_label = ttk.Label(self.header_frame, text=article_date,
                background=HEADER_COLOR) 
        date_label.pack(side=RIGHT, padx=25) 

        # -- adding header
        self.header_frame.pack(side=TOP, fill=X) 

    def draw_buttons(self):
        """ draws next, previous, and twitter toggle buttons """ 
        self.button_frame = Frame(self)

        # -- getting images
        prev_image = PhotoImage(file=self.directory + '/images/previous.png')
        prev_image = prev_image.subsample(10, 10) 

        next_image = PhotoImage(file=self.directory + '/images/next.png')
        next_image = next_image.subsample(10, 10) 
       
        # -- adding image to label
        prev_label = ttk.Label(self.button_frame, image = prev_image)
        next_label = ttk.Label(self.button_frame, image = next_image)

        prev_label.image = prev_image
        next_label.image = next_image

        # -- adding a twitter hide button
        self.twitter_hide = ttk.Button(self.button_frame, text='hide twitter')
        
        # -- adding the buttons to the frame 
        prev_label.pack(side=RIGHT, padx=75) 
        self.twitter_hide.pack(side=RIGHT, padx=200) 
        next_label.pack(side=LEFT, padx=75)

        # -- adding bindings and commands
        prev_label.bind('<Button-1>', self.prev_article)
        next_label.bind('<Button-1>', self.next_article) 
        self.twitter_hide.config(command=self.hide_twitter) 

        # -- adding frame to canvas
        self.button_frame.pack(side=BOTTOM, fill=X)

    def prev_article(self, event=None):
        """ redraws canvas with previous article """
        
        # -- destory current view
        self.destroy_view()

        # -- redraw with prev article in urls stack
        self.current_article += 1
        self.draw_article(self.urls[self.current_article])


    def next_article(self, event=None):
        """ redraws canvas with next article """
    
        # -- destroy current view
        self.destroy_view() 

        # -- redraw with next article in urls stack
        self.current_article -= 1 
        self.draw_article(self.urls[self.current_article])

    def draw_twitter_canvas(self):
        """ draws twitter canvas with a frame of fixed width """

        self.TWITTER_WIDTH = 100 
        
        self.twitter_canvas= Canvas(self, width=self.TWITTER_WIDTH)
        self.twitter_scrollbar = ttk.Scrollbar(self, orient= VERTICAL,
                command=self.twitter_canvas.yview) 
        self.twitter_canvas.configure(yscrollcommand=self.twitter_scrollbar.set)
        
        # make sure to add scrollbar before adding the canvas
        self.twitter_scrollbar.pack(side=RIGHT, fill=Y)
        self.twitter_canvas.pack(side=RIGHT, fill=Y)
       
        # adding a frame to hold all the widgets, ttk Frame doesn't support
        # background config option 
        self.twitter_frame = Frame(self.twitter_canvas)
        self.twitter_canvas.create_window(0,0,window=self.twitter_frame,
                anchor='nw', width=self.TWITTER_WIDTH)

        
        # -- adding the twitter logo
        twitter_logo = PhotoImage(file=self.directory + '/images/twitter_icon.png')
        twitter_logo = twitter_logo.subsample(30, 30) 

        # -- adding image to label
        twitter_label = ttk.Label(self.twitter_frame, image = twitter_logo)

        twitter_label.image = twitter_logo 

        twitter_label.pack(side=TOP, pady=10)

    def draw_tweet(self, tweet_content):
        """ draws a tweet onto the twitter canvas' frame """

        tweet = Text(self.twitter_frame, bg="white", fg="black", wrap=WORD, 
                     height=6, font=('arial', 10), pady=5, padx=10)

        tweet.insert(1.0, tweet_content)
        tweet.configure(state='disabled')
        tweet.pack(side=TOP)

    def hide_twitter(self):
        """ hides the twitter sidebar """

        # -- change the button
        self.twitter_hide.config(text='twitter disabled', state='disabled')  
        self.twitter_hide.config(command=self.show_twitter)

        self.twitter_canvas.pack_forget() 
        self.twitter_scrollbar.pack_forget()

        


    def show_twitter(self):
        """ shows the twitter sidebar """

        # -- THIS DOESN'T WORK B/C OF PACK()...NEED TO REDRAW EVERYTHING
        
        # -- change the button
        self.twitter_hide.config(text='hide twitter') 
        self.twitter_hide.config(command=self.hide_twitter)

        self.twitter_canvas.pack()
        self.twitter_scrollbar.pack() 

    def destroy_view(self):
        """ calls destroy() on canvas, scrollbars, header, footer, and twitter
        feed """ 

        self.canvas.destroy()
        self.scrollbar.destroy()
        self.header_frame.destroy()
        self.button_frame.destroy()
        self.twitter_canvas.destroy()
        self.twitter_scrollbar.destroy()





if __name__=='__main__':
    
    app = App()
    
    app.mainloop()

































































#######
tdgsync
#######
tdgsync 0.5 8-June-2012

************
Introduction
************


tdgsync is a python based solution for syncing your computer's ip 
a defined ftp server, especially for home servers which don't have
a static ip address.


***********
Depedencies
***********

* tweepy

tweepy is for making tdgsync tweets between interval which you would have
written to "sync.config". These tweets will include date and time. You can
customize content of the tweets with changing the "sentence" file. 


* psutil

psutil library is for tracking the system which runs tdgsync. It can give
details of memory,cpu,hard drive usage. (even core number of your cpu)

* httplib2

httplib2 is used for getting your ip on the internet from some services.
For default, it uses my own small php page on http://tdgunes.org/getip/

But it is recommended to use your own web page for getting ip, in order
to protect your privacy. 

****************************
Getting Started with tdgsync
****************************

tdgsync doesn't have a setup.py at this present.(Maybe in future!)
But preparing it is not very hard as it seems.

Before starting, you should know that tdgsync is designed for home server owners
which they have a web page on the web that they can access it with FTP.

IP changes will be sent via FTP to that web page so that you can know your
home server ip.

* 1. Be sure you have all the depedencies that written above.

tweepy, psutil and httplib2 are can be found easily on the your package
system, if you are using a linux distro. If not, you can install them
by hand. 

Note: You will be using tdgsync as a cronjob. You should check if you have
cron in your system. 

* 2. Clone, or download tdgsync from this page.

* 3. Prepare a settings folder wherever you wish. 

You can copy configs folder from the tdgsync package. 

* 4. Start editing!

There are three files: 

index.html - This is the page that will be sent via FTP. You can use
all of the tags ({cpunumber}, {ip}, etc.) here as you are going to do
the same in your sentences file.

sync.config - This is the configuration file that has all the details
about tdgsync. (For example, start messages, ip change messages)

sentences - mostly for users that going to use twitter message service.

All of these files are not blank, you can figure them out by checking my
configuration.


* 5. Running tdgsync

After trying different methods to run tdgsync, I believe logical way to 
run tdgsync for between intervals is using cron. 

You can simply write

crontab -e

to enter a cronjob to the cron. Usually all of the Linux distros have examples of
adding a cronjob. 

Add


    

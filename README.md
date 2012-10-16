When [I quit LiveJournal][quit] I worried that some future owner of
the site would do something distasteful with my data -- like decide
that my private posts should be made public.  I wrote two quick
scripts: one to archive all my posts locally, and one to delete them
from the site one by one.

After writing over the years two or three LJ exporters into different
formats, I came to realize the most future-proof archive is plain
text. So this program saves each post into an individual text file
with the post metadata listed like RFC822 mail headers at the top.


WARNING: I wrote this years ago and only thought to publish it now.
From a skim through the code it appears to only save a listed set of
post metadata (subject, date, etc.).  If I were to write it now I'd
have it instead just save any attributes provided by the LiveJournal
export protocol.  The difference is that there is other post metadata
(like "current music" or whatever) that LJ added over the years that
this doesn't save.  Oh well, too late now -- I only cared about the
post text anyway.

WARNING 2: You'll need to adjust the code to use it on your own
content.  Don't worry, it's pretty simple.


[quit]: http://evan.livejournal.com/991055.html

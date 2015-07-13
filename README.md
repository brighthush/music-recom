# music-recom
Crawl play lists data from xiami. Using these lists data to train recommendation model.


## Crawl Scripts  
The main script to crawl data from xiami is in python directory. The main python source file
is named "xiami.py". You can have a look at it and get to know the structure of data output.  

## data struction  
colls.txt
{colls_id : [[song_id, artist_id], [song_id, artist_id], ...], ...}

arts.txt
{artist_id : artist_name, ...}

songs.txt
{song_id : song_name, ...}

colls_name.txt
{coll_url : coll_name, ...}


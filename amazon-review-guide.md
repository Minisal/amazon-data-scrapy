# amazonproducts_spider guide

data:
( # not need in summary; Unfinished #; )

product:
	ASIN 
	number of reviews => num_review
	review score => rating
	crawl_url 
	product_url 
	position 
	price 
	# company
	# category

productDetail:
	ASIN 
	title 
	best sellers rank #
	category sellers rank #
	listed date #

review
	review text => review_title + review_body
	star rating => review_rating
	time => review_date
	asin
	reivew_id




0. change code
	1. postgreSQL create
		add column in table
			ALTER TABLE products ADD price varchar(128);   
			ALTER TABLE products ADD listedDate varchar(2056);  
			ALTER TABLE products ADD crawl_url varchar(2056);   
			ALTER TABLE products ADD product_url varchar(2056);   
			ALTER TABLE products ADD position varchar(128); 

			ALTER TABLE product_detail ADD category_product_detail varchar(2056);   

		delete column in table
			ALTER TABLE products DROP column product_desc;
			ALTER TABLE products DROP column listeddate;

	2. items
	3. spider
	4. pipline (postgreSQL insert)
	...


1. environment 
		> pip3 install scrapy
		> pip3 install redis
		> pip3 install numpy
		> pip3 install scrapy_proxies
		> brew install postgresql

2. create databse
		> createdb
		> psql
		> create database amazon_db;   # ";"
		> \l
   remenber => Owner : YOUR-USER-NAME
		
   create table
   		> \c amazon_db
   		> CREATE TABLE products(
   		  asin varchar(2056),
          category varchar(2056),
          company varchar(2056),
          product_desc varchar(2056)
          num_review int,
          rating varchar(128),
          price varchar(128),
          listedDate varchar(2056),
          crawl_url varchar(2056),
		  product_url varchar(2056),
		  position varchar(128),
          PRIMARY KEY( asin )
          );

        > CREATE TABLE reviews(
          review_id varchar(128),
          asin varchar(2056),
          review_title varchar(128),
          review_rating varchar(128),
          review_date varchar(128),
          review_body varchar(2056)
          PRIMARY KEY( review_id )
          );

         > CREATE TABLE product_detail(
          asin varchar(2056),
		  listed_date varchar(2056), 
		  title varchar(2056), 
		  best_sellers_rank varchar(2056),
		  catehory_sellers_rank varchar(2056),
          PRIMARY KEY( asin )
          );

        > quit


3. select category 
	amazonproducts/amazonproducts/spiders/amazonproducts_spider.py
		line 27 -> 34
		category_start_url
		category_URL_list
4.  set postgreSQL
	amazon2/amazon2/config.json
		{
		"database":"amazon_db", 
		"user":"YOUR-USER-NAME", 
		"host":"127.0.0.1", 
		"port":"5432"
		}
5. set Redis
	amazonpriducts/amazonproducts/settings.py
		# REDIS
		redis_host = '127.0.0.1' 
		redis_port = 6379
		redis_db = 0 # max:15
	terminal
		> redis-server
6. set proxy
	amazonpriducts/amazonproducts/proxies_http_ip.txt
		http://username:password@host2:port


7. START # notice the sequence
	amazonpriducts/amazonproducts
		> scrapy crawl amazonproducts
	amazon2/amazon2
		> scrapy crawl amazon2
	priductDetial/productDetial
		> scrapy crawl productDetail

8. show data
	1) csv
	2)
		> psql
		> \c amazon_db
		> \d
		> \d products
		> select * from products;    # ";"

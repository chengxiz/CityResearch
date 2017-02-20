# Who are interested in greenhouse issues

This repository contains the project: *City Research: People from where are interested in greenhouse issues*. The city research project provides a whole process of KDD (Knowledge discovery and data mining), including data selection, data pre-processing and enrichment, data reduction and projection, data mining, and pattern interpretation and reporting.

## Project Object
The object of the project is to discover the spatial distribution patterns of the characters of all papers from academic databases with specific keywords. 
 
## Project process
### Data selection
In this project, [wanfang](http://www.wanfangdata.com/) is regarded as the selected academic database. The keyword list consists of several keywords related to greenhouse issues. For each paper, there are several characters need to further discussed: 
1. The geographic entity of research object (i.e. for a paper named ["Food, Fuel, and Freeways: An Iowa perspective on how far food travels, fuel usage, and greenhouse gas emissions"](http://lib.dr.iastate.edu/leopold_pubspapers/3/), Iowa state is the geographic entity.
2. The geographic entity of research institues which authors are employeed. In the above case, Iowa State University (three times) and University of Northern Iowa are what I refer.
3. The keyword used for searching the paper. In the above case, "greenhouse gas emissions" is the keyword.

[Scrapy](https://scrapy.org/), An open source and collaborative framework for extracting the data you need from websites, is utilized to build a new dataset and select data subsets from the dataset of [wanfang](http://www.wanfangdata.com/).
### Data pre-processing and enrichment
In this project, duplicated records from all extracted data need to eliminated first (which means the sample paper is considered as more than one record in the database）. Then geographic entities need to be formally represented from geonames with the help of [geoNames](http://www.geonames.org/).
### Data reduction and projection
Uninterested properites of the dataset are removed to make the database smaller and less redundant.
### Data mining
A series of cluster analysis are made to explore the spatial pattern of the dataset.
### Pattern interpretation and reporting
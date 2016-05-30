Modeling Enron’s Corporate Culture Through Emails
--------------------------
####Jonathan Kyl, Greg Adams, & Graham Northrup

This repository contains the code and some results of our analysis of [Enron's internal email database].

###Contents
 * `text_sim.py` - Contains a class called ```Comparitor``` that builds a [Latent Semantic Indexing] model from a random sample of files in a path. It contains a method to assign all files in the path a mean cosine similarity score, and write the top-k results to csv.

 * `models` - Contains `.mm` and `.lsi` files created with `Comparitor`. These files can be loaded as standalone instances of a training corpus and LSI model, respectively.

 * `output` - Contains csv files of the top-k (filename, score) tuples written by `Comparitor`.

 * `consolidate.py` - Parses the csv files in `output` which contain the top-k results as found by `Comparitor`, and copies the corresponding files from `all_files` to `consolidated_output` (not included, as they exceed git's size limits).

 * `final_output` - Contains multiple results of running `Comparitor` on `consolidated_output` in csv form. 

 * `prep_files` - Contains scripts for setting up the EC2 instances used to run `Comparitor` in parallel.

 * `database_funcs.py` - Utility functions for interfacing with an sqlite3 database.

 * `network.py` Uses Networkx to build a network from all of the emails that had metadata associated with them (600k). Then uses a ranking algorithm to find the 10 people with the highest weights in the graph and saves it to an output file. Requires the database created by parse_xmls.py
 
 * `parse_xmls.py` From the unzipped xml files, creates a database containing the metadata for each email. Used with network.py to build the network.

###Dependencies
 * [numpy]
 * [scipy]
 * [gensim]
 * [networkx]
 * [sqlite3]
 * [unzip]

All of the above (and more) can be installed by running `setup_instance.sh`

[Enron's internal email database]: <https://aws.amazon.com/datasets/enron-email-data/>
[Latent Semantic Indexing]: <https://en.wikipedia.org/wiki/Latent_semantic_indexing>
[numpy]: <https://github.com/numpy/numpy>
[scipy]: <https://github.com/scipy/scipy>
[gensim]: <https://github.com/piskvorky/gensim>
[networkx]: <https://github.com/networkx/networkx>

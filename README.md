Modeling Enron’s Email Culture Through Emails
--------------------------
####Jonathan Kyl, Greg Adams, & Graham Northrup

This repository contains the code and some results of our analysis of Enron's internal email database, available here

###Files
 * `text_sim.py` - Contains a class called ```Comparitor``` that builds a Latent Semantic Indexing model from a random sample of files in a path. It can also assign all files in the path a mean cosine similarity score, and write the top-k ```(filename, score)``` tuples to csv.

 * `prep_files` Directory containing scripts etc. for setting up the EC2 instances use to run the text similarity in parallel.

 * `database_funcs.py` Basic stuff for working with databases.

 * `network.py` Uses Networkx to build a network from all of the emails that had metadata associated with them (600k). Then uses a ranking algorithm to find the 10 people with the highest weights in the graph and saves it to an output file. Requires the database created by parse_xmls.py
 
 * `parse_xmls.py` From the unzipeed xml files, creates a database containing the metadata for each email. Used with network.py to build the network.
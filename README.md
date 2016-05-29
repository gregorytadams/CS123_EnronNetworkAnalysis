CS123_EnronNetworkAnalysis
--------------------------
### Jon Kyl, Greg Adams, Graham Northrup

This is the git repository containing our files for our CS123 project, analyzing emails from Enron for averageness.

network.py (Original) Uses Networkx to build a network from all of the emails that had metadata associated with them (600k). Then uses a ranking algorithm to find the 10 people with the highest weights in the graph and saves it to an output file. Requires the database created by parse_xmls.py

text_sim.py (Original, uses gensim) Builds a class for working with text files and comparing them to find a similarity score. This was used to find the most average emails.

parse_xmls.py (Original) From the unzipeed xml files, creates a database containing the metadata for each email. Used with network.py to build the network.

prep_files (Original) Directory containing scripts etc. for setting up the EC2 instances use to run the text similarity in parallel.

database_funcs.py (Original) Basic stuff for working with databases.
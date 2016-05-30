Modeling Enron’s Email Culture Through Emails
--------------------------
####Jonathan Kyl, Greg Adams, & Graham Northrup

This is the git repository containing the following files for our CS123 project:

```text_sim.py``` - Contains a class called ```Comparitor``` that builds a Latent Semantic Indexing model from a random sample of a bucket of emails, and assigns all emails in that bucket a mean cosine similarity score. 

parse_xmls.py From the unzipeed xml files, creates a database containing the metadata for each email. Used with network.py to build the network.

prep_files (Original) Directory containing scripts etc. for setting up the EC2 instances use to run the text similarity in parallel.

database_funcs.py (Original) Basic stuff for working with databases.

```network.py``` Uses Networkx to build a network from all of the emails that had metadata associated with them (600k). Then uses a ranking algorithm to find the 10 people with the highest weights in the graph and saves it to an output file. Requires the database created by parse_xmls.py
[![Edwards Lab](https://img.shields.io/badge/Bioinformatics-EdwardsLab-03A9F4)](https://edwards.sdsu.edu/research)

# Simple NCBI Taxonomy

A pure python NCBI taxonomy parser.

Set up the NCBI taxonomy like you would for [taxonkit](https://bioinf.shenwei.me/taxonkit) or set the `NCBI_TAXONOMY` or `TAXONKIT_DB` environment
variables to your directory that contains `nodes.dmp`, `names.dmp`, etc.

Then you can load the data and iterate through the whole tree. This provides more access to the taxonomic data than `taxonkit`. For example, I can't
figure out an easy way to get the parent id and name out of `taxonkit`. 

There is an example script in [src](src/) that demonstrates how to iterate the tree.

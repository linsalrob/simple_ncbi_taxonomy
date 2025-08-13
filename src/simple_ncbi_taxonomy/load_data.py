import gzip
import sys
import os

from .config import get_db_dir
from .taxonomy import TaxonNode, TaxonName, TaxonDivision

defaultdir = get_db_dir()

def read_taxa():
    """
    Read the taxonomy tree. An alias for read_nodes()
    """
    return read_nodes()


def read_nodes(directory=defaultdir):
    """
    Read the node information from the default location
    """

    if not directory:
        directory = defaultdir
    if not os.path.exists(directory + '/nodes.dmp'):
        sys.stderr.write("Cannot find nodes.dmp in " + directory + "\n")
        sys.exit(-1)

    taxa = {}
    fin = open(directory + '/nodes.dmp', 'r')
    for line in fin:
        line = line.rstrip('\t|\n')
        cols = line.split('\t|\t')
        t = TaxonNode(*cols)
        taxa[cols[0]] = t
    fin.close()
    return taxa


def extended_names(directory=defaultdir):
    """
    Extended names returns "genbank synonym" and "synonym" as well as
    "scientific name" and "blast name". Because we are reading more
    names it is slower and consumes more memory
    """

    if not directory:
        directory = defaultdir
    if not os.path.exists(directory + '/names.dmp'):
        sys.stderr.write("Cannot find names.dmp in " + directory + "\n")
        sys.exit(-1)

    names = {}
    blastname = {}
    genbankname = {}
    synonym = {}
    fin = open(directory + '/names.dmp', 'r')
    for line in fin:
        line = line.rstrip('\t|\n')
        cols = line.split('\t|\t')
        t = TaxonName(*cols)
        if "scientific name" in cols[3]:
            names[cols[0]] = t
        elif "blast name" in cols[3]:
            blastname[cols[0]] = t
        elif "genbank synonym" in cols[3]:
            genbankname[cols[0]] = t
        elif "synonym" in cols[3]:
            synonym[cols[0]] = t

    fin.close()
    return names, blastname, genbankname, synonym


def read_names(directory=defaultdir):
    """
    Read the name information from the default location
    """

    if not directory:
        directory = defaultdir

    names = {}
    blastname = {}

    if os.path.exists(directory + '/names.dmp'):
        fin = open(directory + '/names.dmp', 'r')
    elif os.path.exists(directory + '/names.dmp.gz'):
        fin = gzip.open(directory + '/names.dmp', 'r')
    else:
        sys.stderr.write("Cannot find names.dmp in " + directory + "\n")
        sys.exit(-1)

    for line in fin:
        line = line.rstrip('\t|\n')
        cols = line.split('\t|\t')
        t = TaxonName(*cols)
        if "scientific name" in cols[3]:
            names[cols[0]] = t
        if "blast name" in cols[3]:
            blastname[cols[0]] = t
    fin.close()
    return names, blastname


def read_divisions(directory=defaultdir):
    """
    Read the divisions.dmp file
    """

    if not directory:
        directory = defaultdir
    if not os.path.exists(directory + '/division.dmp'):
        sys.stderr.write("Cannot find division.dmp in " + directory + "\n")
        sys.exit(-1)

    divs = {}
    fin = open(directory + '/division.dmp', 'r')
    for line in fin:
        line = line.rstrip('\t|\n')
        cols = line.split('\t|\t')
        t = TaxonDivision(*cols)
        divs[cols[0]] = t
    fin.close()
    return divs


def load_ncbi_taxonomy(directory=defaultdir):
    """
    Load all the data from the taxonomy database.
    Returns a tuple of (nodes, names, blastnames, divisions)
    """

    if not directory:
        directory = defaultdir

    nodes = read_nodes(directory)
    names, blastnames = read_names(directory)
    divisions = read_divisions(directory)

    return nodes, names, blastnames, divisions

def read_gi_tax_id(dtype='nucl', directory=defaultdir):
    """
    Read gi_taxid.dmp. You can specify the type of database that you
    want to parse, default is nucl (nucleotide), can also accept prot
    (protein).

    Returns a hash of gi and taxid
    """

    if not directory:
        directory = defaultdir

    if dtype != 'nucl' and dtype != 'prot':
        sys.stderr.write("Type must be either nucl or prot, not " + dtype + "\n")
        sys.exit(-1)
    file_in = directory + "/gi_taxid_" + dtype + ".dmp.gz"
    if not os.path.exists(file_in):
        sys.stderr.write("Cannot find " + file_in + "\n")
        sys.exit(-1)

    taxid = {}
    with gzip.open(file_in, 'r') as fin:
        for line in fin:
            line = line.decode().strip()
            parts = line.split("\t")
            taxid[parts[0]] = parts[1]
    fin.close()
    return taxid


def read_tax_id_gi(dtype='nucl', directory=defaultdir):
    """
    Read gi_taxid.dmp. You can specify the type of database that you
    want to parse, default is nucl (nucleotide), can also accept prot
    (protein).

    NOTE: This method returns taxid -> gi not the other way around. This
    may be a one -> many mapping (as a single taxid maps to more than
    one gi), and so we return a list of gi's for each taxid.

    Returns a hash of taxid and gi
    """

    if not directory:
        directory = defaultdir

    if dtype != 'nucl' and dtype != 'prot':
        sys.stderr.write("Type must be either nucl or prot, not " + dtype + "\n")
        sys.exit(-1)
    file_in = directory + "/gi_taxid_" + dtype + ".dmp.gz"
    if not os.path.exists(file_in):
        sys.stderr.write("Cannot find " + file_in + "\n")
        sys.exit(-1)

    tax_id = {}
    with gzip.open(file_in, 'r') as fin:
        for line in fin:
            line = line.decode().strip()
            parts = line.split("\t")
            if parts[1] not in tax_id:
                tax_id[parts[1]] = []
            tax_id[parts[1]].append(parts[0])
    fin.close()
    return tax_id

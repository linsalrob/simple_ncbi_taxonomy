"""
Reead a list of taxonomy IDs from a file and convert them to pplacer format.

The format we need is tax_id,parent_id,rank,tax_name,root,domain,phylum,class,order,family,genus,species

"""

import os
import sys
import argparse
from simple_ncbi_taxonomy import load_ncbi_taxonomy, bcolors
__author__ = 'Rob Edwards'


def taxids_to_pplacer(taxids, verbose=False):
    # load the taxonomy data
    if verbose:
        print(f"{bcolors.OKBLUE}Loading taxonomy data...{bcolors.ENDC}", file=sys.stderr)
    nodes, names, blastnames, divisions = load_ncbi_taxonomy()
    if verbose:
        print(f"{bcolors.OKBLUE}Done.{bcolors.ENDC}", file=sys.stderr)

    wanted = ['root', 'domain', 'phylum', 'class', 'order', 'family', 'genus', 'species']
    altdomain = ['superkingdom', 'acellular root', 'domain']
    for tid in taxids:
        if tid not in nodes:
            print(f"{bcolors.FAIL}TaxID {tid} not found in taxonomy data.{bcolors.ENDC}", file=sys.stderr)
            continue
        wname = {rank: "" for rank in wanted}
        wname['root'] = 1
        pid = nodes[tid].parent
        while pid is not None and pid != '1':
            if nodes[pid].rank in wanted:
                #wname[nodes[pid].rank] = names[pid].get_name()
                wname[nodes[pid].rank] = pid
            if nodes[pid].rank in altdomain:
                #wname['domain'] = names[pid].get_name()
                wname['domain'] = pid
            pid = nodes[pid].parent
        print(f"{tid},{nodes[tid].parent},{nodes[tid].rank},{names[tid].get_name()},"
              f"{wname['root']},{wname['domain']},{wname['phylum']},{wname['class']},"
              f"{wname['order']},{wname['family']},{wname['genus']},{wname['species']}")



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=' ')
    parser.add_argument('-f', help='input file', required=True)
    parser.add_argument('-v', help='verbose output', action='store_true')
    args = parser.parse_args()

    tids = set()
    with open(args.f, 'r') as fin:
        for line in fin:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tids.add(line)
    taxids_to_pplacer(tids, verbose=args.v)


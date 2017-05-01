import sqlite3
import datetime

conn = sqlite3.connect('test.db')

c = conn.cursor()

pubchem_lst = []

pubchem_lst2 = []

pubchem_lst3 = []

tuple_lst = [] #CONTAINS THE SPECIFIED PARAMETERS TO BE EXTRACTED FROM THE SDF

tuple_lst2 = [] #CONTAINS THE PROPERLY FORMATED PARAMETERS FOR SQL INSERTION

with open("Compound_000000001_000025000.sdf", 'r') as fil:
    for line in fil:
        line = line.strip()

        pubchem_lst.append(line)
    fil.close()

for i in range(0, len(pubchem_lst)):
    if pubchem_lst[i] != '$$$$':
        pubchem_lst2.append(pubchem_lst[i])
    if pubchem_lst[i] == '$$$$':
        pubchem_lst3.append(pubchem_lst2)
        pubchem_lst2 = []

for i in range(0,len(pubchem_lst3)):

    if '> <PUBCHEM_COMPOUND_CID>' in pubchem_lst3[i]: #this gets the pubchem ID
        tuple_lst.append(pubchem_lst3[i][pubchem_lst3[i].index('> <PUBCHEM_COMPOUND_CID>') + 1])

    # This gets the INCHI
    if '> <PUBCHEM_IUPAC_INCHI>' in pubchem_lst3[i]:
        tuple_lst.append(pubchem_lst3[i][pubchem_lst3[i].index('> <PUBCHEM_IUPAC_INCHI>') + 1])

    # This gets the INCHI_KEY
    if '> <PUBCHEM_IUPAC_INCHIKEY>' in pubchem_lst3[i]:
        tuple_lst.append(pubchem_lst3[i][pubchem_lst3[i].index('> <PUBCHEM_IUPAC_INCHIKEY>') + 1])

    # this gets the proper IUPAC name
    if '> <PUBCHEM_IUPAC_NAME>' in pubchem_lst3[i]:
        tuple_lst.append(pubchem_lst3[i][pubchem_lst3[i].index('> <PUBCHEM_IUPAC_NAME>') + 1])

    # if it doesn't exist, then placeholder 'DNE' is inserted
    if '> <PUBCHEM_IUPAC_NAME>' not in pubchem_lst3[i]:
        tuple_lst.append('DNE')

    # This statment obtains the smiles for the commpund
    if '> <PUBCHEM_OPENEYE_CAN_SMILES>' in pubchem_lst3[i]: # this gets the proper SMILES configuration
        tuple_lst.append(pubchem_lst3[i][pubchem_lst3[i].index("> <PUBCHEM_OPENEYE_CAN_SMILES>") + 1])


for i in range(0,len(tuple_lst), 5):
    tuple_lst2.append([int(tuple_lst[i]), tuple_lst[i+1], tuple_lst[i+2], tuple_lst[i+3], tuple_lst[i+4]])


HTML_list = []
for i in range(0, len(tuple_lst2)):
    HTML_list.append([tuple_lst2[i][0], 'nil', datetime.datetime.now().date()])


c.execute('''DROP TABLE IF EXISTS PubChem_Ref;''')

c.execute('''DROP TABLE IF EXISTS HTML_BLOB;''')

c.execute('''CREATE TABLE IF NOT EXISTS HTML_BLOB(
             PUBCHEM_CID INT,
             HTML BLOB,
             CREATION_DATE DATE,
             PRIMARY KEY (PUBCHEM_CID));''')

c.execute('''CREATE TABLE IF NOT EXISTS PubChem_Ref (
              PUBCHEM_CID INT,
              PUBCHEM_INCHI TEXT,
              PUBCHEM_INCHIKEY TEXT,
              PUBCHEM_IUPAC TEXT,
              PUBCHEM_SMILES TEXT,
              PRIMARY KEY(PUBCHEM_CID, PUBCHEM_INCHI, PUBCHEM_INCHIKEY));''')

conn.commit()

c.executemany('''INSERT INTO PubChem_Ref
                (PUBCHEM_CID, PUBCHEM_INCHI, PUBCHEM_INCHIKEY, PUBCHEM_IUPAC, PUBCHEM_SMILES)
                 VALUES (?, ?, ?, ?, ?);''', tuple_lst2)
c.executemany('''INSERT INTO HTML_BLOB (PUBCHEM_CID, HTML, CREATION_DATE) VALUES (?, ?, ?);''', HTML_list)

conn.commit()
conn.close()

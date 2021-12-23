import requests
from IPython.display import display, Markdown
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import json
import pickle
import os
import csv


def fetch_data():

    _transport = RequestsHTTPTransport(
        url='https://api.datacite.org/graphql',
        use_json=True,
    )

    client = Client(
        transport=_transport,
        fetch_schema_from_transport=True,
    )

    # Generate the GraphQL query: find all outputs of FREYA grant award (https://cordis.europa.eu/project/id/777523) from funder (EU) to date
    query_params = {
        "funderId" : "https://doi.org/10.13039/501100000780",
        "funderAwardQuery" : "fundingReferences.awardNumber:777523",
        "maxWorks" : 200
    }

    query = gql("""query getGrantOutputsForFunderAndAward($funderId: ID!, $funderAwardQuery: String!, $maxWorks: Int!)
    {
    funder(id: $funderId) {
      name
      works(query: $funderAwardQuery, first: $maxWorks) {
          totalCount
          nodes {
            id
            formattedCitation(style: "vancouver")
            titles {
              title
            }
            descriptions {
              description
            }        
            types {
              resourceType
            }
            dates {
              date
              dateType
            }
            versionOfCount
            rights {
              rights
              rightsIdentifier
              rightsUri
            }        
            creators {
              id
              name
            }
            fundingReferences {
              funderIdentifier
              funderName
              awardNumber
              awardTitle
            }
            citationCount
            viewCount
            downloadCount
          }
        }
      }
    }
    """)

    data = client.execute(query, variable_values=json.dumps(query_params))

    return data


def build_matrix(data):
    all_creator_names_by_node = []
    all_creator_names_set = set([])
    funder = data['funder']['works']
    for r in funder['nodes']:
        if r['versionOfCount'] > 0:
            # If the current output is a version of another one, exclude it
            continue
        # To minimise cropping of names in the below, retain just the first letter of the first name
        # if the author name is well formatted
        creator_names = []
        for name in [s['name'] for s in r['creators'] if s['name']]:
            if name.find(",") > 0:
                creator_names.append(name[0:name.index(",") + 3])
            elif name.find(",") == 0:
                creator_names.append(name[1:].strip())
            else:
                creator_names.append(name)
        all_creator_names_by_node.append(creator_names)
        all_creator_names_set.update(creator_names)

    # Assemble data structures for the co-authorship chord diagram
    all_creator_names = sorted(list(all_creator_names_set))

    # Initialise chord data matrix
    length = len(all_creator_names)
    coauthorship_matrix = []
    for i in range(length):
        r = []
        for j in range(length):
            r.append(0)
        coauthorship_matrix.append(r)

    # Populate chord data matrix
    for node_creators in all_creator_names_by_node:
        for creator in node_creators:
            c_pos = all_creator_names.index(creator)
            for co_creator in node_creators:
                co_pos = all_creator_names.index(co_creator)
                if c_pos != co_pos:
                    coauthorship_matrix[c_pos][co_pos] += 1

    return coauthorship_matrix, all_creator_names

have_data = False
if os.path.exists('/home/james/Desktop/coauthorship_matrix.pkl') and os.path.exists('/home/james/Desktop/all_creator_names.pkl'):
    have_data = True

co_mtx, cnames = None, None

if not have_data:
    gql_data = fetch_data()
    co_mtx, c_names = build_matrix(gql_data)

    with open('/home/james/Desktop/coauthorship_matrix.pkl', 'wb') as outpf:
        pickle.dump(co_mtx, outpf)

    with open('/home/james/Desktop/all_creator_names.pkl', 'wb') as outpf:
        pickle.dump(c_names, outpf)
else:
    with open('/home/james/Desktop/coauthorship_matrix.pkl', 'rb') as inpf:
        co_mtx = pickle.load(inpf)

    with open('/home/james/Desktop/all_creator_names.pkl', 'rb') as inpf:
        c_names = pickle.load(inpf)

if co_mtx is not None:
    print(co_mtx)
    print(len(co_mtx))

if c_names is not None:
    print(c_names)
    print(len(c_names))

pairs = []
for r_idx in range(0, len(c_names)):
    for c_idx in range(0, len(c_names)):
        if c_idx < r_idx:
            if co_mtx[r_idx][c_idx] > 0:
                pairs.append([c_names[c_idx], c_names[r_idx], co_mtx[r_idx][c_idx]])

with open('/home/james/Desktop/coauthorship_pairs.csv', 'w') as outpf:
    my_writer = csv.writer(outpf, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
    my_writer.writerow(['source', 'target', 'value'])
    for i in pairs:
        my_writer.writerow(i)












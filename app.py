from flask import Flask, render_template
import random
import ast

app = Flask(__name__)

# Function to read data from the text file
def read_data():
    edges = []
    nodes = {}
    existing_edges = {}
    original_text = ""
    coreferences = {}
    with open('sentences.txt', 'r') as file:
        original_text = file.read()
    # Load coreference data from 'coreferences.txt' as JSON
    with open('coreferences.txt', 'r') as file:
        coreferences = ast.literal_eval(file.read())


    with open('output.txt', 'r') as file:
        id_counter = 0
        for line in file:
            sentence_num, confidence, arg1, rel, arg2 = line.strip().split('|')
            if arg1==arg2:
                continue

            if arg1 not in nodes:
                nodes[arg1] = {"id": arg1, "sent": int(sentence_num), "color": "blue", "x": 0, "y": 0, "boost": [int(sentence_num)]}
            else:
                nodes[arg1]["sent"] = min(nodes[arg1]["sent"], int(sentence_num))
                nodes[arg1]["boost"] = nodes[arg1]["boost"]+[int(sentence_num)]
            if arg2 not in nodes:
                nodes[arg2] = {"id": arg2, "sent": int(sentence_num), "color": "blue", "x": 0, "y": 0, "boost": [int(sentence_num)]}
            else:
                nodes[arg2]["sent"] = min(nodes[arg2]["sent"], int(sentence_num))
                nodes[arg2]["boost"] = nodes[arg2]["boost"]+[int(sentence_num)]
            
            # Create a key for the edge
            edge_key = tuple(sorted([arg1, arg2]))
            if edge_key in existing_edges:
                # Append new relationship to the existing edge
                existing_edges[edge_key].append((rel,sentence_num))
            else:
                # Create a new edge entry
                existing_edges[edge_key] = [(rel,sentence_num)]
        
        # Construct edges with combined relationships
        for (source, target), rels in existing_edges.items():
            edges.append({
                "source": source,
                "target": target,
                "id": rels
            })

    graph_data = {
        "nodes": list(nodes.values()),
        "links": edges,
        "text": original_text,
        "coreferences": coreferences
    }
    return graph_data

@app.route('/')
def index():
    data = read_data()  # Get data from the text file
    return render_template('index.html', graph_data=data)  # Pass data directly (not as a JSON string)

if __name__ == '__main__':
    app.run(debug=True)


# ============================================================
# Life Sciences Commercial Analytics Knowledge Graph Explorer
# ============================================================
#
# Domain:         Commercial Analytics for Life Sciences
# Developed For:  Python Task 6 - Knowledge Graph Explorer
# Author:         Merina Roy
# Date:           2024-06-11
#
# FEATURES:

#   1. Entity Exploration
#   2. Relationship Exploration
#   3. Knowledge Queries
#   4. Graph Insights
#   5. Custom Discovery Rule (High-Influence Product)
#   6. Knowledge Graph Visualization
#   7. Report Generation (download)
#   8. [UNIQUE] Relationship Path Finder
#   9. [UNIQUE] Interactive Analytics Dashboard

#PSEUDOCODE :

# 1. Import required libraries and configure the logging system.
# 2. Create an Entity class to represent different ontology entities.
# 3. Create a Relationship class to represent connections between entities.
# 4. Initialize the Knowledge Graph Explorer and create data structures.
# 5. Load Products, Customers, Sales Representatives, Distributors, Regions, and Market Segments.
# 6. Store all entities and assign unique identifiers to each entity.
# 7. Define relationships between entities based on business rules.
# 8. Build the knowledge graph by adding entities as nodes and relationships as edges.
# 9. Implement entity exploration features to view and search entities.
# 10. Implement relationship exploration to analyze connections between entities.
# 11. Create knowledge queries to retrieve domain-specific information.
# 12. Generate graph insights such as most connected entity and most active sales representative.
# 13. Apply the High-Influence Product discovery rule to classify products.
# 14. Visualize the knowledge graph and relationship networks using interactive graphs.
# 15. Generate reports and launch the Streamlit-based Knowledge Graph Explorer application.

# ===============================================================================================

# ===============================================================================================
# IMPORT REQUIRED LIBRARIES
# ===============================================================================================

import matplotlib
matplotlib.use("Agg")                        #Visualization Libraries
import matplotlib.pyplot as plt              # used for plots
import matplotlib.patches as mpatches        # used for Graph Legends
import numpy as np                           # For numerical operations
import streamlit as st                       # For deployment
import networkx as nx                        # For knowledge graph creation
from collections import Counter, defaultdict # For data counting
import json, logging, datetime, io           # Reading/Generating datasets

# ============================================================
# LOGGING CONFIGURATION
# ============================================================
# This part of the code is for audit purpose to record system errors.

logging.basicConfig(
    filename="knowledge_graph_errors.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# ============================================================
# ENTITY CLASS
# ============================================================
#The Entity class is used to represent each node in the knowledge graph. It stores the unique ID, name, and type
#of every entity such as Products, Customers, Sales Representatives, Distributors, Regions, and Market Segments.
#This provides a structured and reusable way to manage entity information throughout the application.

class Entity:
    """Represents an entity within the Commercial Analytics Knowledge Graph."""

    def __init__(self, entity_id: str, entity_name: str, entity_type: str):
        self.entity_id   = entity_id
        self.entity_name = entity_name
        self.entity_type = entity_type

    def __str__(self):
        return f"{self.entity_id} | {self.entity_name} | {self.entity_type}"

    def to_dict(self):
        return {"ID": self.entity_id, "Name": self.entity_name, "Type": self.entity_type}


# ============================================================
# RELATIONSHIP CLASS
# ============================================================
#The Relationship class is used to represent connections between two entities in the knowledge graph. It stores
# the source entity, target entity, and relationship type.

class Relationship:
    """Represents a directed relationship between two entities."""

    def __init__(self, source: str, target: str, relationship_type: str):
        self.source            = source
        self.target            = target
        self.relationship_type = relationship_type

    def __str__(self):
        return f"{self.source} --{self.relationship_type}--> {self.target}"

    def to_dict(self):
        return {"Source": self.source, "Relationship": self.relationship_type, "Target": self.target}


# ============================================================
# KNOWLEDGE GRAPH EXPLORER CLASS
# ============================================================
# THIS IS THE CENTRAL NERVOUS SYSTEM OF THE ENTIRE PROGRAM

class KnowledgeGraphExplorer:
    """Create, manage and explore the Commercial Analytics Knowledge Graph."""

    def __init__(self):
        self.entities: dict      = {}
        self.relationships: list = []
        self.graph               = nx.DiGraph()

    # ----------------------------------------------------------
    # LOAD SAMPLE DATA
    # ----------------------------------------------------------
    # Sample datasets are loaded by calling each methods

    def load_sample_data(self):
        """Load all predefined entities and relationships."""

        # ---- PRODUCTS (12) ----
        products = [
            Entity("P001","OncoCure","Product"),    Entity("P002","CardioSafe","Product"),
            Entity("P003","GlucoCare","Product"),   Entity("P004","ImmunoPlus","Product"),
            Entity("P005","NeuroAid","Product"),    Entity("P006","VacciShield","Product"),
            Entity("P007","RenoLife","Product"),    Entity("P008","HepatoCare","Product"),
            Entity("P009","RespiraX","Product"),    Entity("P010","DermoHeal","Product"),
            Entity("P011","OrthoFlex","Product"),   Entity("P012","VisionPro","Product"),
        ]

        # ---- CUSTOMERS (18) ----
        customers = [
            Entity("C001","Apollo Hospital","Customer"),     Entity("C002","Fortis Hospital","Customer"),
            Entity("C003","Max Healthcare","Customer"),      Entity("C004","Aster Hospitals","Customer"),
            Entity("C005","Manipal Hospitals","Customer"),   Entity("C006","MedPlus","Customer"),
            Entity("C007","Apollo Pharmacy","Customer"),     Entity("C008","Care Hospital","Customer"),
            Entity("C009","Yashoda Hospital","Customer"),    Entity("C010","Narayana Health","Customer"),
            Entity("C011","KIMS Hospital","Customer"),       Entity("C012","Rainbow Hospital","Customer"),
            Entity("C013","Metro Pharmacy","Customer"),      Entity("C014","HealthKart Medical","Customer"),
            Entity("C015","Sun Pharma Retail","Customer"),   Entity("C016","Global Medics","Customer"),
            Entity("C017","WellCare Clinics","Customer"),    Entity("C018","Prime Healthcare","Customer"),
        ]

        # ---- SALES REPRESENTATIVES (10) ----
        sales_reps = [
            Entity("SR001","Rahul Sharma","Sales Representative"),
            Entity("SR002","Priya Patel","Sales Representative"),
            Entity("SR003","Arjun Singh","Sales Representative"),
            Entity("SR004","Neha Gupta","Sales Representative"),
            Entity("SR005","Ravi Kumar","Sales Representative"),
            Entity("SR006","Sneha Roy","Sales Representative"),
            Entity("SR007","Amit Verma","Sales Representative"),
            Entity("SR008","Karan Mehta","Sales Representative"),
            Entity("SR009","Anjali Rao","Sales Representative"),
            Entity("SR010","Vikas Nair","Sales Representative"),
        ]

        # ---- DISTRIBUTORS (8) ----
        distributors = [
            Entity("D001","ABC Distributors","Distributor"),
            Entity("D002","HealthLink Distribution","Distributor"),
            Entity("D003","MedSupply Logistics","Distributor"),
            Entity("D004","BioChain Distribution","Distributor"),
            Entity("D005","LifeCare Logistics","Distributor"),
            Entity("D006","Prime Distribution Services","Distributor"),
            Entity("D007","HealthBridge Supply","Distributor"),
            Entity("D008","Global Pharma Distribution","Distributor"),
        ]

        # ---- REGIONS (6) ----
        regions = [
            Entity("R001","North India","Region"),      Entity("R002","South India","Region"),
            Entity("R003","East India","Region"),       Entity("R004","West India","Region"),
            Entity("R005","Central India","Region"),    Entity("R006","North-East India","Region"),
        ]

        # ---- MARKET SEGMENTS (6) ----
        segments = [
            Entity("M001","Oncology","Market Segment"),     Entity("M002","Cardiology","Market Segment"),
            Entity("M003","Diabetes","Market Segment"),     Entity("M004","Vaccines","Market Segment"),
            Entity("M005","Neurology","Market Segment"),    Entity("M006","Dermatology","Market Segment"),
        ]

        for e in products + customers + sales_reps + distributors + regions + segments:
            self.entities[e.entity_id] = e

        # ---- RELATIONSHIPS ----
        self.relationships = []

        targets = [
            ("P001","M001"),("P002","M002"),("P003","M003"),("P004","M004"),
            ("P005","M005"),("P006","M004"),("P007","M003"),("P008","M001"),
            ("P009","M005"),("P010","M006"),("P011","M002"),("P012","M006"),
        ]
        for s,t in targets:
            self.relationships.append(Relationship(s,t,"TARGETS"))

        sold_in = [
            ("P001","R001"),("P001","R002"),("P002","R003"),("P002","R004"),
            ("P003","R001"),("P003","R005"),("P004","R002"),("P004","R006"),
            ("P005","R003"),("P005","R004"),("P006","R001"),("P006","R006"),
            ("P007","R002"),("P007","R005"),("P008","R003"),("P008","R006"),
            ("P009","R001"),("P009","R004"),("P010","R002"),("P010","R003"),
            ("P011","R005"),("P011","R006"),("P012","R001"),("P012","R002"),
        ]
        for s,t in sold_in:
            self.relationships.append(Relationship(s,t,"SOLD_IN"))

        purchases = [
            ("C001","P001"),("C001","P008"),("C002","P002"),("C002","P005"),
            ("C003","P003"),("C003","P006"),("C004","P004"),("C004","P011"),
            ("C005","P001"),("C005","P009"),("C006","P010"),("C006","P012"),
            ("C007","P007"),("C007","P003"),("C008","P002"),("C008","P008"),
            ("C009","P005"),("C009","P009"),("C010","P001"),("C010","P004"),
            ("C011","P006"),("C011","P010"),("C012","P011"),("C012","P012"),
            ("C013","P003"),("C013","P007"),("C014","P002"),("C014","P005"),
            ("C015","P008"),("C015","P010"),("C016","P001"),("C016","P006"),
            ("C017","P009"),("C017","P011"),("C018","P004"),("C018","P012"),
        ]
        for s,t in purchases:
            self.relationships.append(Relationship(s,t,"PURCHASES"))

        manages = [
            ("SR001","C001"),("SR001","C002"),("SR002","C003"),("SR002","C004"),
            ("SR003","C005"),("SR003","C006"),("SR004","C007"),("SR004","C008"),
            ("SR005","C009"),("SR005","C010"),("SR006","C011"),("SR006","C012"),
            ("SR007","C013"),("SR007","C014"),("SR008","C015"),("SR008","C016"),
            ("SR009","C017"),("SR010","C018"),
        ]
        for s,t in manages:
            self.relationships.append(Relationship(s,t,"MANAGES"))

        promotes = [
            ("SR001","P001"),("SR001","P008"),("SR002","P003"),("SR002","P006"),
            ("SR003","P009"),("SR003","P005"),("SR004","P007"),("SR004","P002"),
            ("SR005","P004"),("SR005","P011"),("SR006","P010"),("SR006","P012"),
            ("SR007","P003"),("SR007","P007"),("SR008","P002"),("SR008","P008"),
            ("SR009","P009"),("SR009","P011"),("SR010","P004"),("SR010","P012"),
        ]
        for s,t in promotes:
            self.relationships.append(Relationship(s,t,"PROMOTES"))

        distributes = [
            ("D001","P001"),("D001","P002"),("D001","P003"),
            ("D002","P004"),("D002","P005"),("D002","P006"),
            ("D003","P007"),("D003","P008"),("D004","P009"),("D004","P010"),
            ("D005","P011"),("D005","P012"),("D006","P001"),("D006","P005"),
            ("D007","P003"),("D007","P009"),("D008","P002"),("D008","P010"),
        ]
        for s,t in distributes:
            self.relationships.append(Relationship(s,t,"DISTRIBUTES"))

        operates_in = [
            ("D001","R001"),("D001","R002"),("D002","R003"),("D002","R004"),
            ("D003","R001"),("D003","R005"),("D004","R002"),("D004","R006"),
            ("D005","R003"),("D005","R004"),("D006","R005"),("D006","R006"),
            ("D007","R001"),("D007","R003"),("D008","R002"),("D008","R004"),
        ]
        for s,t in operates_in:
            self.relationships.append(Relationship(s,t,"OPERATES_IN"))

        located_in = [
            ("C001","R002"),("C002","R001"),("C003","R001"),("C004","R002"),
            ("C005","R002"),("C006","R002"),("C007","R002"),("C008","R002"),
            ("C009","R002"),("C010","R002"),("C011","R002"),("C012","R002"),
            ("C013","R003"),("C014","R001"),("C015","R004"),("C016","R003"),
            ("C017","R005"),("C018","R006"),
        ]
        for s,t in located_in:
            self.relationships.append(Relationship(s,t,"LOCATED_IN"))

        covers = [
            ("SR001","R001"),("SR002","R001"),("SR003","R002"),("SR004","R002"),
            ("SR005","R003"),("SR006","R003"),("SR007","R004"),("SR008","R004"),
            ("SR009","R005"),("SR010","R006"),
        ]
        for s,t in covers:
            self.relationships.append(Relationship(s,t,"COVERS"))

        # Build NetworkX graph
        self.graph.clear()
        for eid, entity in self.entities.items():
            self.graph.add_node(eid, name=entity.entity_name, etype=entity.entity_type)
        for rel in self.relationships:
            self.graph.add_edge(rel.source, rel.target, rel_type=rel.relationship_type)


    # ----------------------------------------------------------
    # FEATURE 1 — ENTITY EXPLORATION
    # ----------------------------------------------------------

    def get_entities_by_type(self, entity_type):
        try:
            return [e.to_dict() for e in self.entities.values() if e.entity_type == entity_type]
        except Exception as exc:
            logging.error("get_entities_by_type: %s", exc); return []

    def search_entity(self, query):
        try:
            q = query.lower()
            return [e.to_dict() for e in self.entities.values()
                    if q in e.entity_name.lower() or q in e.entity_id.lower()]
        except Exception as exc:
            logging.error("search_entity: %s", exc); return []

    def get_entity_connections(self, entity_id):
        try:
            if entity_id not in self.entities:
                return {}
            outgoing = [r.to_dict() for r in self.relationships if r.source == entity_id]
            incoming = [r.to_dict() for r in self.relationships if r.target == entity_id]
            return {"outgoing": outgoing, "incoming": incoming}
        except Exception as exc:
            logging.error("get_entity_connections: %s", exc); return {}


    # ----------------------------------------------------------
    # FEATURE 2 — RELATIONSHIP EXPLORATION
    # ----------------------------------------------------------
    # To explore connections between two entities eg customer and product or customer and company.

    def get_relationships_by_type(self, rel_type):
        try:
            return [r.to_dict() for r in self.relationships if r.relationship_type == rel_type]
        except Exception as exc:
            logging.error("get_relationships_by_type: %s", exc); return []

    def get_all_relationship_types(self):
        return sorted({r.relationship_type for r in self.relationships})


    # ----------------------------------------------------------
    # FEATURE 3 — KNOWLEDGE QUERIES
    # ----------------------------------------------------------
    # Knowledge Queries were introduced to enable users to retrieve meaningful
    # business information from the knowledge graph. 

    def query_products_by_segment(self, segment_name):
        try:
            seg_ids = [eid for eid,e in self.entities.items()
                       if e.entity_type == "Market Segment" and segment_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "TARGETS" and rel.target in seg_ids:
                    prod = self.entities.get(rel.source)
                    seg  = self.entities.get(rel.target)
                    if prod:
                        result.append({"Product ID": prod.entity_id, "Product": prod.entity_name,
                                       "Segment": seg.entity_name if seg else rel.target})
            return result
        except Exception as exc:
            logging.error("query_products_by_segment: %s", exc); return []

    def query_products_by_region(self, region_name):
        try:
            reg_ids = [eid for eid,e in self.entities.items()
                       if e.entity_type == "Region" and region_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "SOLD_IN" and rel.target in reg_ids:
                    prod = self.entities.get(rel.source)
                    reg  = self.entities.get(rel.target)
                    if prod:
                        result.append({"Product ID": prod.entity_id, "Product": prod.entity_name,
                                       "Region": reg.entity_name if reg else rel.target})
            return result
        except Exception as exc:
            logging.error("query_products_by_region: %s", exc); return []

    def query_customers_by_region(self, region_name):
        try:
            reg_ids = [eid for eid,e in self.entities.items()
                       if e.entity_type == "Region" and region_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "LOCATED_IN" and rel.target in reg_ids:
                    cust = self.entities.get(rel.source)
                    reg  = self.entities.get(rel.target)
                    if cust:
                        result.append({"Customer ID": cust.entity_id, "Customer": cust.entity_name,
                                       "Region": reg.entity_name if reg else rel.target})
            return result
        except Exception as exc:
            logging.error("query_customers_by_region: %s", exc); return []

    def query_sales_rep_products(self, rep_name):
        try:
            rep_ids = [eid for eid,e in self.entities.items()
                       if e.entity_type == "Sales Representative" and rep_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "PROMOTES" and rel.source in rep_ids:
                    rep  = self.entities.get(rel.source)
                    prod = self.entities.get(rel.target)
                    if prod:
                        result.append({"Rep ID": rep.entity_id, "Sales Rep": rep.entity_name,
                                       "Product ID": prod.entity_id, "Product": prod.entity_name})
            return result
        except Exception as exc:
            logging.error("query_sales_rep_products: %s", exc); return []

    def query_distributor_regions(self, distributor_name):
        try:
            dist_ids = [eid for eid,e in self.entities.items()
                        if e.entity_type == "Distributor" and distributor_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "OPERATES_IN" and rel.source in dist_ids:
                    dist = self.entities.get(rel.source)
                    reg  = self.entities.get(rel.target)
                    if reg:
                        result.append({"Distributor ID": dist.entity_id, "Distributor": dist.entity_name,
                                       "Region ID": reg.entity_id, "Region": reg.entity_name})
            return result
        except Exception as exc:
            logging.error("query_distributor_regions: %s", exc); return []

    def query_customers_by_product(self, product_name):
        try:
            prod_ids = [eid for eid,e in self.entities.items()
                        if e.entity_type == "Product" and product_name.lower() in e.entity_name.lower()]
            result = []
            for rel in self.relationships:
                if rel.relationship_type == "PURCHASES" and rel.target in prod_ids:
                    cust = self.entities.get(rel.source)
                    prod = self.entities.get(rel.target)
                    if cust:
                        result.append({"Customer ID": cust.entity_id, "Customer": cust.entity_name,
                                       "Product": prod.entity_name if prod else rel.target})
            return result
        except Exception as exc:
            logging.error("query_customers_by_product: %s", exc); return []


    # ----------------------------------------------------------
    # FEATURE 4 — GRAPH INSIGHTS
    # ----------------------------------------------------------
    # "DYNAMIC GRAPH INSIGHTS - It will change with every dataset"

    def generate_insights(self):
        try:
            insights = {}

            degree_seq = sorted(self.graph.degree(), key=lambda x: x[1], reverse=True)
            if degree_seq:
                top_id, top_deg = degree_seq[0]
                top_name = self.entities[top_id].entity_name if top_id in self.entities else top_id
                top_type = self.entities[top_id].entity_type if top_id in self.entities else ""
                insights["Most Connected Entity"] = f"{top_name} ({top_type}) — {top_deg} connections"

            seg_counts = Counter()
            for rel in self.relationships:
                if rel.relationship_type == "TARGETS":
                    seg_counts[rel.target] += 1
            if seg_counts:
                top_seg_id = seg_counts.most_common(1)[0][0]
                top_seg_name = self.entities[top_seg_id].entity_name if top_seg_id in self.entities else top_seg_id
                insights["Most Targeted Market Segment"] = f"{top_seg_name} — targeted by {seg_counts[top_seg_id]} products"

            mgmt_counts = Counter()
            for rel in self.relationships:
                if rel.relationship_type == "MANAGES":
                    mgmt_counts[rel.source] += 1
            if mgmt_counts:
                top_sr_id = mgmt_counts.most_common(1)[0][0]
                top_sr_name = self.entities[top_sr_id].entity_name if top_sr_id in self.entities else top_sr_id
                insights["Most Active Sales Rep"] = f"{top_sr_name} — manages {mgmt_counts[top_sr_id]} customers"

            purch_counts = Counter()
            for rel in self.relationships:
                if rel.relationship_type == "PURCHASES":
                    purch_counts[rel.target] += 1
            if purch_counts:
                top_prod_id = purch_counts.most_common(1)[0][0]
                top_prod_name = self.entities[top_prod_id].entity_name if top_prod_id in self.entities else top_prod_id
                insights["Most Purchased Product"] = f"{top_prod_name} — purchased by {purch_counts[top_prod_id]} customers"

            region_cust = Counter()
            for rel in self.relationships:
                if rel.relationship_type == "LOCATED_IN":
                    region_cust[rel.target] += 1
            if region_cust:
                top_reg_id = region_cust.most_common(1)[0][0]
                top_reg_name = self.entities[top_reg_id].entity_name if top_reg_id in self.entities else top_reg_id
                insights["Region With Most Customers"] = f"{top_reg_name} — {region_cust[top_reg_id]} customers"

            dist_prod = Counter()
            for rel in self.relationships:
                if rel.relationship_type == "DISTRIBUTES":
                    dist_prod[rel.source] += 1
            if dist_prod:
                top_dist_id = dist_prod.most_common(1)[0][0]
                top_dist_name = self.entities[top_dist_id].entity_name if top_dist_id in self.entities else top_dist_id
                insights["Distributor Covering Most Products"] = f"{top_dist_name} — distributes {dist_prod[top_dist_id]} products"

            insights["Graph Density"] = f"{nx.density(self.graph):.4f}"
            return insights
        except Exception as exc:
            logging.error("generate_insights: %s", exc); return {}


    # ----------------------------------------------------------
    # FEATURE 5 — CUSTOM DISCOVERY RULE
    # ----------------------------------------------------------
    #Knowledge Queries were introduced to enable users to
    #retrieve meaningful business information from the knowledge
    #graph. 

    def apply_high_influence_product_rule(self):
        """
        High-Influence Product Rule
        Score = (Customer Reach x 2) + (Regional Reach x 3) + (Segment Breadth x 4)
        HIGH >= 12 | MEDIUM 6-11 | LOW < 6
        """
        try:
            scores = []
            for pid, e in self.entities.items():
                if e.entity_type != "Product":
                    continue
                cust_count    = sum(1 for r in self.relationships if r.relationship_type == "PURCHASES" and r.target == pid)
                region_count  = sum(1 for r in self.relationships if r.relationship_type == "SOLD_IN"   and r.source == pid)
                segment_count = sum(1 for r in self.relationships if r.relationship_type == "TARGETS"   and r.source == pid)
                score = (cust_count * 2) + (region_count * 3) + (segment_count * 4)
                classification = "HIGH" if score >= 12 else "MEDIUM" if score >= 6 else "LOW"
                scores.append({
                    "Product ID": e.entity_id, "Product": e.entity_name,
                    "Customer Reach": cust_count, "Regional Reach": region_count,
                    "Segment Breadth": segment_count, "Influence Score": score,
                    "Classification": classification,
                })
            return sorted(scores, key=lambda x: x["Influence Score"], reverse=True)
        except Exception as exc:
            logging.error("apply_high_influence_product_rule: %s", exc); return []


    # ----------------------------------------------------------
    # FEATURE 6 — GRAPH VISUALIZATION
    # ----------------------------------------------------------
    # To Visualize the Graphical Contents

    COLOR_MAP = {
        "Product":              "#4CAF50",
        "Customer":             "#2196F3",
        "Sales Representative": "#FF9800",
        "Distributor":          "#9C27B0",
        "Region":               "#F44336",
        "Market Segment":       "#00BCD4",
    }

    def _node_colors(self, nodes):
        return [self.COLOR_MAP.get(self.entities[n].entity_type if n in self.entities else "", "#CCCCCC") for n in nodes]

    def visualize_full_graph(self, figsize=(18, 13)):
        try:
            plt.close("all")
            fig, ax = plt.subplots(figsize=figsize)
            pos = nx.spring_layout(self.graph, seed=42, k=1.8)
            colors = self._node_colors(self.graph.nodes())
            labels = {n: self.entities[n].entity_name[:12] if n in self.entities else n for n in self.graph.nodes()}
            nx.draw_networkx_nodes(self.graph, pos, node_color=colors, node_size=500, alpha=0.9, ax=ax)
            nx.draw_networkx_labels(self.graph, pos, labels=labels, font_size=6, ax=ax)
            nx.draw_networkx_edges(self.graph, pos, alpha=0.3, arrows=True, arrowsize=10, ax=ax)
            patches = [mpatches.Patch(color=c, label=t) for t,c in self.COLOR_MAP.items()]
            ax.legend(handles=patches, loc="upper left", fontsize=8)
            ax.set_title("Life Sciences Commercial Analytics — Knowledge Graph", fontsize=14, fontweight="bold")
            ax.axis("off")
            fig.tight_layout()
            return fig
        except Exception as exc:
            logging.error("visualize_full_graph: %s", exc)
            plt.close("all")
            return plt.figure()

    def visualize_subgraph(self, entity_id, depth=2):
        try:
            plt.close("all")
            if entity_id not in self.graph:
                return plt.figure()
            nodes = {entity_id}
            frontier = {entity_id}
            for _ in range(depth):
                new_frontier = set()
                for n in frontier:
                    new_frontier.update(self.graph.successors(n))
                    new_frontier.update(self.graph.predecessors(n))
                nodes.update(new_frontier)
                frontier = new_frontier
            sub = self.graph.subgraph(nodes).copy()
            colors = self._node_colors(sub.nodes())
            labels = {n: self.entities[n].entity_name if n in self.entities else n for n in sub.nodes()}
            edge_labels = {(u,v): d.get("rel_type","") for u,v,d in sub.edges(data=True)}
            fig, ax = plt.subplots(figsize=(12, 8))
            pos = nx.spring_layout(sub, seed=42, k=2.5)
            nx.draw_networkx_nodes(sub, pos, node_color=colors, node_size=700, alpha=0.9, ax=ax)
            nx.draw_networkx_labels(sub, pos, labels=labels, font_size=8, ax=ax)
            nx.draw_networkx_edges(sub, pos, alpha=0.4, arrows=True, arrowsize=15, ax=ax)
            nx.draw_networkx_edge_labels(sub, pos, edge_labels=edge_labels, font_size=6, ax=ax)
            center_name = self.entities[entity_id].entity_name if entity_id in self.entities else entity_id
            ax.set_title(f"Subgraph: {center_name} (depth={depth})", fontsize=12, fontweight="bold")
            ax.axis("off")
            fig.tight_layout()
            return fig
        except Exception as exc:
            logging.error("visualize_subgraph: %s", exc)
            plt.close("all")
            return plt.figure()


    # ----------------------------------------------------------
    # UNIQUE FEATURE A — RELATIONSHIP PATH FINDER
    # ----------------------------------------------------------
    # The Relationship Path Finder identifies and displays the
    # shortest connection path between two entities in the
    # knowledge graph. It helps users understand how entities
    # are indirectly related through intermediate nodes and
    # relationships.

    def find_all_paths(self, source_id, target_id, max_paths=5, cutoff=6):
        """Find up to max_paths simple paths between two entities (undirected)."""
        try:
            undirected = self.graph.to_undirected()
            if source_id not in undirected or target_id not in undirected:
                return []
            # Use islice to avoid generating ALL paths before slicing (performance fix)
            from itertools import islice
            all_paths_gen = nx.all_simple_paths(undirected, source_id, target_id, cutoff=cutoff)
            paths = sorted(islice(all_paths_gen, 500), key=len)   # cap at 500 to avoid hang
            return paths[:max_paths]
        except Exception as exc:
            logging.error("find_all_paths: %s", exc); return []

    def describe_path(self, path):
        """Annotate each step in a path with entity names, types and relationship labels."""
        try:
            steps = []
            for i, node_id in enumerate(path):
                ent   = self.entities.get(node_id)
                name  = ent.entity_name if ent else node_id
                etype = ent.entity_type if ent else "Unknown"
                if i < len(path) - 1:
                    next_id   = path[i + 1]
                    rel_label = "—"
                    if self.graph.has_edge(node_id, next_id):
                        rel_label = self.graph[node_id][next_id].get("rel_type", "—")
                    elif self.graph.has_edge(next_id, node_id):
                        rel_label = self.graph[next_id][node_id].get("rel_type", "—")
                    steps.append({"Step": i+1, "Entity ID": node_id, "Entity Name": name,
                                  "Entity Type": etype, "Relationship to Next": rel_label})
                else:
                    steps.append({"Step": i+1, "Entity ID": node_id, "Entity Name": name,
                                  "Entity Type": etype, "Relationship to Next": "(destination)"})
            return steps
        except Exception as exc:
            logging.error("describe_path: %s", exc); return []

    def visualize_path(self, path):
        """Draw the path highlighted within its local neighbourhood."""
        try:
            plt.close("all")
            undirected = self.graph.to_undirected()
            neighborhood = set(path)
            for n in path:
                neighborhood.update(list(undirected.neighbors(n))[:3])
            sub = undirected.subgraph(neighborhood).copy()
            path_edges = set(zip(path, path[1:]))

            node_colors = []
            node_sizes  = []
            for n in sub.nodes():
                if n == path[0]:
                    node_colors.append("#FFD700"); node_sizes.append(1200)
                elif n == path[-1]:
                    node_colors.append("#FF4500"); node_sizes.append(1200)
                elif n in path:
                    node_colors.append("#00E5FF"); node_sizes.append(900)
                else:
                    ent = self.entities.get(n)
                    node_colors.append(self.COLOR_MAP.get(ent.entity_type if ent else "", "#CCCCCC"))
                    node_sizes.append(400)

            labels = {n: self.entities[n].entity_name[:14] if n in self.entities else n for n in sub.nodes()}
            edge_colors = ["#FF6F00" if (u,v) in path_edges or (v,u) in path_edges else "#CCCCCC" for u,v in sub.edges()]
            edge_widths  = [3.5       if (u,v) in path_edges or (v,u) in path_edges else 0.8       for u,v in sub.edges()]

            fig, ax = plt.subplots(figsize=(13, 8))
            pos = nx.spring_layout(sub, seed=7, k=2.2)
            nx.draw_networkx_nodes(sub, pos, node_color=node_colors, node_size=node_sizes, alpha=0.93, ax=ax)
            nx.draw_networkx_labels(sub, pos, labels=labels, font_size=7, ax=ax)
            nx.draw_networkx_edges(sub, pos, edge_color=edge_colors, width=edge_widths, alpha=0.85, ax=ax)
            legend_items = [
                mpatches.Patch(color="#FFD700", label="Source"),
                mpatches.Patch(color="#FF4500", label="Target"),
                mpatches.Patch(color="#00E5FF", label="Path Node"),
                mpatches.Patch(color="#CCCCCC", label="Neighbour"),
            ]
            ax.legend(handles=legend_items, loc="upper left", fontsize=8)
            src_name = self.entities[path[0]].entity_name  if path[0]  in self.entities else path[0]
            tgt_name = self.entities[path[-1]].entity_name if path[-1] in self.entities else path[-1]
            ax.set_title(f"Path: {src_name}  ->  {tgt_name}  ({len(path)-1} hops)", fontsize=12, fontweight="bold")
            ax.axis("off")
            fig.tight_layout()
            return fig
        except Exception as exc:
            logging.error("visualize_path: %s", exc)
            plt.close("all")
            return plt.figure()


    # ----------------------------------------------------------
    # UNIQUE FEATURE B — CHART DATA HELPERS
    # ----------------------------------------------------------

    def chart_entity_distribution(self):
        return dict(Counter(e.entity_type for e in self.entities.values()))

    def chart_relationship_distribution(self):
        return dict(Counter(r.relationship_type for r in self.relationships))

    def chart_product_customer_reach(self):
        prod_cust = Counter()
        for r in self.relationships:
            if r.relationship_type == "PURCHASES":
                prod_cust[r.target] += 1
        return [{"Product": self.entities[pid].entity_name if pid in self.entities else pid,
                 "Customers": cnt} for pid, cnt in prod_cust.most_common()]

    def chart_region_density(self):
        region_data = {}
        for eid, e in self.entities.items():
            if e.entity_type == "Region":
                region_data[eid] = {"Region": e.entity_name, "Customers": 0, "Products": 0, "Distributors": 0}
        for r in self.relationships:
            if   r.relationship_type == "LOCATED_IN"   and r.target in region_data:
                region_data[r.target]["Customers"]    += 1
            elif r.relationship_type == "SOLD_IN"       and r.target in region_data:
                region_data[r.target]["Products"]     += 1
            elif r.relationship_type == "OPERATES_IN"   and r.target in region_data:
                region_data[r.target]["Distributors"] += 1
        return list(region_data.values())

    def chart_rep_performance(self):
        rep_data = {}
        for eid, e in self.entities.items():
            if e.entity_type == "Sales Representative":
                rep_data[eid] = {"Rep": e.entity_name, "Customers Managed": 0, "Products Promoted": 0}
        for r in self.relationships:
            if   r.relationship_type == "MANAGES"  and r.source in rep_data:
                rep_data[r.source]["Customers Managed"] += 1
            elif r.relationship_type == "PROMOTES"  and r.source in rep_data:
                rep_data[r.source]["Products Promoted"] += 1
        return sorted(rep_data.values(), key=lambda x: x["Customers Managed"], reverse=True)

    def chart_segment_heatmap_data(self):
        prod_ids   = [eid for eid,e in self.entities.items() if e.entity_type == "Product"]
        seg_ids    = [eid for eid,e in self.entities.items() if e.entity_type == "Market Segment"]
        prod_names = [self.entities[p].entity_name for p in prod_ids]
        seg_names  = [self.entities[s].entity_name for s in seg_ids]
        targets_set = {(r.source, r.target) for r in self.relationships if r.relationship_type == "TARGETS"}
        # Use numpy array — more reliable with matplotlib imshow
        matrix = np.array([[1 if (p,s) in targets_set else 0 for s in seg_ids] for p in prod_ids],
                           dtype=float)
        return prod_names, seg_names, matrix


    # ----------------------------------------------------------
    # FEATURE 7 — REPORT GENERATION
    # ----------------------------------------------------------
    # In the form of txt file within the application 

    def generate_report_text(self):
        try:
            lines = []
            SEP  = "=" * 65
            sep2 = "-" * 65
            lines += [SEP, "  LIFE SCIENCES COMMERCIAL ANALYTICS", "  KNOWLEDGE GRAPH REPORT",
                      f"  Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", SEP]

            lines += ["\n1. ONTOLOGY SUMMARY", sep2, "Domain : Commercial Analytics", "Entity Types (6):"]
            for etype in ["Product","Customer","Sales Representative","Distributor","Region","Market Segment"]:
                cnt = sum(1 for e in self.entities.values() if e.entity_type == etype)
                lines.append(f"   * {etype:<25} {cnt} entities")
            lines.append("\nRelationship Types (9):")
            for rt in self.get_all_relationship_types():
                cnt = sum(1 for r in self.relationships if r.relationship_type == rt)
                lines.append(f"   * {rt:<20} {cnt} relationships")

            lines += ["\n2. ENTITY COUNTS", sep2,
                      f"   Total Entities      : {len(self.entities)}",
                      f"   Total Relationships : {len(self.relationships)}",
                      f"   Graph Nodes         : {self.graph.number_of_nodes()}",
                      f"   Graph Edges         : {self.graph.number_of_edges()}"]

            lines += ["\n3. RELATIONSHIP COUNTS BY TYPE", sep2]
            rt_counter = Counter(r.relationship_type for r in self.relationships)
            for rt, cnt in rt_counter.most_common():
                lines.append(f"   {rt:<20} : {cnt}")

            lines += ["\n4. KNOWLEDGE QUERIES EXECUTED", sep2]
            for label, results in [
                ("Products targeting Oncology",       self.query_products_by_segment("Oncology")),
                ("Products sold in South India",       self.query_products_by_region("South India")),
                ("Customers in North India",           self.query_customers_by_region("North India")),
                ("Products promoted by Rahul Sharma",  self.query_sales_rep_products("Rahul")),
                ("Regions covered by ABC Distributors",self.query_distributor_regions("ABC")),
                ("Customers purchasing OncoCure",      self.query_customers_by_product("OncoCure")),
            ]:
                lines.append(f"   {label} : {len(results)} found")

            lines += ["\n5. GRAPH INSIGHTS", sep2]
            for key, val in self.generate_insights().items():
                lines.append(f"   {key:<45} : {val}")

            lines += ["\n6. CUSTOM DISCOVERY RULE -- HIGH-INFLUENCE PRODUCT", sep2,
                      "   Score = (Customer Reach x 2) + (Regional Reach x 3) + (Segment Breadth x 4)",
                      "   HIGH >= 12  |  MEDIUM 6-11  |  LOW < 6", ""]
            for row in self.apply_high_influence_product_rule():
                lines.append(f"   {row['Product']:<15} | Score:{row['Influence Score']:>3} | {row['Classification']:<6}"
                              f"| Cust:{row['Customer Reach']} Reg:{row['Regional Reach']} Seg:{row['Segment Breadth']}")

            lines += ["\n7. RECOMMENDATIONS", sep2,
                      "   1. Prioritise HIGH-influence products in marketing campaigns.",
                      "   2. Expand distributor network in North-East India.",
                      "   3. Increase Sales Rep coverage in Central India.",
                      "   4. Leverage South India dense customer base for cross-sell.",
                      "   5. Explore Dermatology segment for portfolio expansion.",
                      "", SEP, "  END OF REPORT", SEP]
            return "\n".join(lines)
        except Exception as exc:
            logging.error("generate_report_text: %s", exc); return "Error generating report."


# ============================================================
# STREAMLIT APPLICATION
# ============================================================
# For deployment purpose

# Page name constants — defined once so menu labels and elif checks
# always use the exact same string object (avoids hidden emoji issues)
PAGE_DASHBOARD    = "Home - Dashboard"
PAGE_ENTITIES     = "Entity Exploration"
PAGE_RELATIONS    = "Relationship Exploration"
PAGE_QUERIES      = "Knowledge Queries"
PAGE_INSIGHTS     = "Graph Insights"
PAGE_DISCOVERY    = "Discovery Rule"
PAGE_VIZGRAPH     = "Graph Visualization"
PAGE_PATHFINDER   = "Path Finder"
PAGE_ANALYTICS    = "Analytics Dashboard"
PAGE_REPORT       = "Report"

MENU_LABELS = [
    f"🏠  {PAGE_DASHBOARD}",
    f"🔍  {PAGE_ENTITIES}",
    f"🔗  {PAGE_RELATIONS}",
    f"📊  {PAGE_QUERIES}",
    f"💡  {PAGE_INSIGHTS}",
    f"⭐  {PAGE_DISCOVERY}",
    f"🌐  {PAGE_VIZGRAPH}",
    f"🔮  {PAGE_PATHFINDER}",
    f"📈  {PAGE_ANALYTICS}",
    f"📄  {PAGE_REPORT}",
]


@st.cache_resource
def get_explorer():
    explorer = KnowledgeGraphExplorer()
    explorer.load_sample_data()
    return explorer


def _render_fig(fig):
    """Render a matplotlib figure and immediately close it to free memory."""
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def main():
    st.set_page_config(
        page_title="Life Sciences KG Explorer",
        page_icon="🕸️",          # Changed: graph/network icon instead of DNA
        layout="wide",
    )

    st.sidebar.title("🕸️ KG Explorer")
    st.sidebar.markdown("**Life Sciences — Commercial Analytics**")
    st.sidebar.markdown("---")
    menu = st.sidebar.radio("Navigation", MENU_LABELS)
    st.sidebar.markdown("---")
    st.sidebar.caption("Author: Merina Roy | Python Task 6")

    explorer = get_explorer()

    # Resolve current page using exact constant match to avoid any substring confusion
    if   MENU_LABELS[0] == menu:   current_page = PAGE_DASHBOARD
    elif MENU_LABELS[1] == menu:   current_page = PAGE_ENTITIES
    elif MENU_LABELS[2] == menu:   current_page = PAGE_RELATIONS
    elif MENU_LABELS[3] == menu:   current_page = PAGE_QUERIES
    elif MENU_LABELS[4] == menu:   current_page = PAGE_INSIGHTS
    elif MENU_LABELS[5] == menu:   current_page = PAGE_DISCOVERY
    elif MENU_LABELS[6] == menu:   current_page = PAGE_VIZGRAPH
    elif MENU_LABELS[7] == menu:   current_page = PAGE_PATHFINDER
    elif MENU_LABELS[8] == menu:   current_page = PAGE_ANALYTICS
    else:                          current_page = PAGE_REPORT

    # ================================================================
    # DASHBOARD
    # ================================================================
    if current_page == PAGE_DASHBOARD:
        st.title("🕸️ Life Sciences Commercial Analytics")
        st.subheader("Knowledge Graph Explorer")
        st.markdown(
            "This application models commercial analytics data for a Life Sciences organisation "
            "using a **Knowledge Graph**. Entities and relationships are represented as an "
            "interconnected graph, enabling exploration and discovery of business intelligence patterns."
        )
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Entities",      len(explorer.entities))
        c2.metric("Total Relationships", len(explorer.relationships))
        c3.metric("Entity Types",        6)
        c4.metric("Relationship Types",  len(explorer.get_all_relationship_types()))
        st.markdown("---")
        st.info(
            "🔮 **New!** Try the **Path Finder** to discover how any two entities are connected, "
            "and the **Analytics Dashboard** for interactive charts and heatmaps."
        )

    # ================================================================
    # ENTITY EXPLORATION
    # ================================================================
    elif current_page == PAGE_ENTITIES:
        st.title("🔍 Entity Exploration")
        tab1, tab2, tab3 = st.tabs(["Browse by Type", "Search Entity", "Entity Connections"])

        with tab1:
            entity_types = sorted({e.entity_type for e in explorer.entities.values()})
            selected_type = st.selectbox("Select Entity Type", entity_types)
            results = explorer.get_entities_by_type(selected_type)
            st.success(f"Found **{len(results)}** entities of type **{selected_type}**")
            st.dataframe(results, use_container_width=True)

        with tab2:
            query = st.text_input("Search by name or ID", placeholder="e.g. Apollo, P001")
            if query:
                results = explorer.search_entity(query)
                if results:
                    st.success(f"Found **{len(results)}** result(s)")
                    st.dataframe(results, use_container_width=True)
                else:
                    st.warning("No entities found.")

        with tab3:
            entity_names = {
                f"{e.entity_id} — {e.entity_name}": e.entity_id
                for e in sorted(explorer.entities.values(), key=lambda x: x.entity_type + x.entity_name)
            }
            selected_label = st.selectbox("Select an Entity", list(entity_names.keys()))
            if selected_label:
                eid = entity_names[selected_label]
                connections = explorer.get_entity_connections(eid)
                ent = explorer.entities[eid]
                st.markdown(f"**{ent.entity_name}** | *{ent.entity_type}* | `{ent.entity_id}`")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown("**Outgoing Relationships**")
                    out = connections.get("outgoing", [])
                    if out:
                        enriched = []
                        for r in out:
                            tgt = explorer.entities.get(r["Target"])
                            enriched.append({"Relationship": r["Relationship"],
                                             "Target ID": r["Target"],
                                             "Target Name": tgt.entity_name if tgt else r["Target"],
                                             "Target Type": tgt.entity_type if tgt else ""})
                        st.dataframe(enriched, use_container_width=True)
                    else:
                        st.info("No outgoing relationships.")
                with col_b:
                    st.markdown("**Incoming Relationships**")
                    inc = connections.get("incoming", [])
                    if inc:
                        enriched = []
                        for r in inc:
                            src = explorer.entities.get(r["Source"])
                            enriched.append({"Source ID": r["Source"],
                                             "Source Name": src.entity_name if src else r["Source"],
                                             "Source Type": src.entity_type if src else "",
                                             "Relationship": r["Relationship"]})
                        st.dataframe(enriched, use_container_width=True)
                    else:
                        st.info("No incoming relationships.")

    # ================================================================
    # RELATIONSHIP EXPLORATION
    # ================================================================
    elif current_page == PAGE_RELATIONS:
        st.title("🔗 Relationship Exploration")
        rel_types = explorer.get_all_relationship_types()
        selected_rt = st.selectbox("Select Relationship Type", rel_types)
        if selected_rt:
            rels = explorer.get_relationships_by_type(selected_rt)
            st.success(f"Found **{len(rels)}** relationships of type **{selected_rt}**")
            enriched = []
            for r in rels:
                src = explorer.entities.get(r["Source"])
                tgt = explorer.entities.get(r["Target"])
                enriched.append({"Source ID": r["Source"], "Source": src.entity_name if src else r["Source"],
                                  "Source Type": src.entity_type if src else "", "Relationship": r["Relationship"],
                                  "Target ID": r["Target"], "Target": tgt.entity_name if tgt else r["Target"],
                                  "Target Type": tgt.entity_type if tgt else ""})
            st.dataframe(enriched, use_container_width=True)
        st.markdown("---")
        st.subheader("Relationship Type Summary")
        rt_counts = Counter(r.relationship_type for r in explorer.relationships)
        st.dataframe([{"Relationship Type": rt, "Count": cnt} for rt, cnt in rt_counts.most_common()],
                     use_container_width=True)

    # ================================================================
    # KNOWLEDGE QUERIES
    # ================================================================
    elif current_page == PAGE_QUERIES:
        st.title("📊 Knowledge Queries")
        query_options = [
            "Q1 — Products targeting a Market Segment",
            "Q2 — Products sold in a Region",
            "Q3 — Customers located in a Region",
            "Q4 — Products promoted by a Sales Representative",
            "Q5 — Regions covered by a Distributor",
            "Q6 — Customers purchasing a Product",
        ]
        selected_query = st.selectbox("Select a Knowledge Query", query_options)
        st.markdown("---")

        if selected_query.startswith("Q1"):
            segments = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Market Segment"])
            seg = st.selectbox("Market Segment", segments)
            if st.button("Run Query"):
                results = explorer.query_products_by_segment(seg)
                st.success(f"**{len(results)}** product(s) targeting **{seg}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

        elif selected_query.startswith("Q2"):
            regions = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Region"])
            reg = st.selectbox("Region", regions)
            if st.button("Run Query"):
                results = explorer.query_products_by_region(reg)
                st.success(f"**{len(results)}** product(s) sold in **{reg}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

        elif selected_query.startswith("Q3"):
            regions = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Region"])
            reg = st.selectbox("Region", regions)
            if st.button("Run Query"):
                results = explorer.query_customers_by_region(reg)
                st.success(f"**{len(results)}** customer(s) in **{reg}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

        elif selected_query.startswith("Q4"):
            reps = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Sales Representative"])
            rep = st.selectbox("Sales Representative", reps)
            if st.button("Run Query"):
                results = explorer.query_sales_rep_products(rep)
                st.success(f"**{len(results)}** product(s) promoted by **{rep}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

        elif selected_query.startswith("Q5"):
            dists = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Distributor"])
            dist = st.selectbox("Distributor", dists)
            if st.button("Run Query"):
                results = explorer.query_distributor_regions(dist)
                st.success(f"**{len(results)}** region(s) covered by **{dist}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

        elif selected_query.startswith("Q6"):
            prods = sorted([e.entity_name for e in explorer.entities.values() if e.entity_type == "Product"])
            prod = st.selectbox("Product", prods)
            if st.button("Run Query"):
                results = explorer.query_customers_by_product(prod)
                st.success(f"**{len(results)}** customer(s) purchasing **{prod}**") if results else st.warning("No results.")
                if results: st.dataframe(results, use_container_width=True)

    # ================================================================
    # GRAPH INSIGHTS
    # ================================================================
    elif current_page == PAGE_INSIGHTS:
        st.title("💡 Graph Insights")
        insights = explorer.generate_insights()
        for idx, (key, val) in enumerate(insights.items(), 1):
            st.markdown(f"**Insight {idx}: {key}**")
            st.info(val)

    # ================================================================
    # DISCOVERY RULE
    # ================================================================
    elif current_page == PAGE_DISCOVERY:
        st.title("⭐ Custom Discovery Rule — High-Influence Product")
        st.markdown("""
### Rule Definition

**Purpose:** Identify products with the highest commercial reach across customers, regions, and market segments.

**Score Formula:**
```
Influence Score = (Customer Reach x 2) + (Regional Reach x 3) + (Segment Breadth x 4)
```

| Classification | Score Range |
|----------------|-------------|
| 🟢 HIGH        | >= 12       |
| 🟡 MEDIUM      | 6 – 11      |
| 🔴 LOW         | < 6         |
        """)
        st.markdown("---")
        st.subheader("Product Influence Scores")
        rule_results = explorer.apply_high_influence_product_rule()

        def badge(cls):
            return {"HIGH": "🟢 HIGH", "MEDIUM": "🟡 MEDIUM"}.get(cls, "🔴 LOW")

        display = [{"Product": r["Product"], "Customer Reach": r["Customer Reach"],
                    "Regional Reach": r["Regional Reach"], "Segment Breadth": r["Segment Breadth"],
                    "Score": r["Influence Score"], "Classification": badge(r["Classification"])}
                   for r in rule_results]
        st.dataframe(display, use_container_width=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("🟢 HIGH",   sum(1 for r in rule_results if r["Classification"] == "HIGH"))
        c2.metric("🟡 MEDIUM", sum(1 for r in rule_results if r["Classification"] == "MEDIUM"))
        c3.metric("🔴 LOW",    sum(1 for r in rule_results if r["Classification"] == "LOW"))

    # ================================================================
    # GRAPH VISUALIZATION
    # ================================================================
    # Title page (Navigation panel)

    elif current_page == PAGE_VIZGRAPH:
        st.title("🌐 Knowledge Graph Visualization")
        viz_tab1, viz_tab2 = st.tabs(["Full Graph", "Entity Subgraph"])

        with viz_tab1:
            st.markdown("Complete knowledge graph — nodes colour-coded by entity type.")
            with st.spinner("Rendering full graph…"):
                fig = explorer.visualize_full_graph(figsize=(18, 13))
            _render_fig(fig)

        with viz_tab2:
            st.markdown("Explore a subgraph centred on a specific entity.")
            entity_names = {
                f"{e.entity_id} — {e.entity_name} ({e.entity_type})": e.entity_id
                for e in sorted(explorer.entities.values(), key=lambda x: x.entity_type + x.entity_name)
            }
            selected_label = st.selectbox("Select Entity", list(entity_names.keys()))
            depth = st.slider("Neighbourhood Depth", 1, 3, 2)
            if st.button("Generate Subgraph"):
                eid = entity_names[selected_label]
                with st.spinner("Rendering subgraph…"):
                    fig2 = explorer.visualize_subgraph(eid, depth=depth)
                _render_fig(fig2)

    # ================================================================
    # PATH FINDER  (UNIQUE FEATURE A)
    # ================================================================
    elif current_page == PAGE_PATHFINDER:
        st.title("🔮 Relationship Path Finder")
        st.markdown(
            "Discover **how any two entities are connected** through the knowledge graph — "
            "even when there is no direct relationship between them. "
            "The finder traces every path and shows you the chain of relationships step by step."
        )

        entity_options = {
            f"{e.entity_id} — {e.entity_name} ({e.entity_type})": e.entity_id
            for e in sorted(explorer.entities.values(), key=lambda x: x.entity_type + x.entity_name)
        }
        all_labels = list(entity_options.keys())

        col_src, col_tgt = st.columns(2)
        with col_src:
            src_label = st.selectbox("🟡 Source Entity", all_labels, index=0, key="pf_src")
        with col_tgt:
            tgt_label = st.selectbox("🔴 Target Entity", all_labels,
                                     index=min(5, len(all_labels) - 1), key="pf_tgt")

        col_opt1, col_opt2 = st.columns(2)
        with col_opt1:
            max_paths = st.slider("Max Paths to Show", 1, 5, 3, key="pf_maxpaths")
        with col_opt2:
            cutoff = st.slider("Max Path Length (hops)", 2, 8, 5, key="pf_cutoff")

        if st.button("Find Paths", use_container_width=True):
            src_id = entity_options[src_label]
            tgt_id = entity_options[tgt_label]

            if src_id == tgt_id:
                st.warning("Source and target must be different entities.")
            else:
                with st.spinner("Searching the graph…"):
                    try:
                        paths = explorer.find_all_paths(src_id, tgt_id,
                                                        max_paths=max_paths, cutoff=cutoff)
                    except Exception as exc:
                        st.error(f"Path search error: {exc}")
                        paths = []

                if not paths:
                    st.error(
                        f"No path found between **{explorer.entities[src_id].entity_name}** "
                        f"and **{explorer.entities[tgt_id].entity_name}** "
                        f"within {cutoff} hops. Try increasing the max path length."
                    )
                else:
                    src_name = explorer.entities[src_id].entity_name
                    tgt_name = explorer.entities[tgt_id].entity_name
                    st.success(f"Found **{len(paths)}** path(s) between **{src_name}** and **{tgt_name}**")

                    for idx, path in enumerate(paths, 1):
                        hop_label = (
                            f"Path {idx}  —  {len(path)-1} hop(s):  "
                            + "  ->  ".join(
                                explorer.entities[n].entity_name if n in explorer.entities else n
                                for n in path
                            )
                        )
                        with st.expander(hop_label, expanded=(idx == 1)):
                            steps = explorer.describe_path(path)
                            if steps:
                                st.dataframe(steps, use_container_width=True)
                            # Narrative sentence
                            parts = []
                            for s in steps:
                                parts.append(f"**{s['Entity Name']}** *({s['Entity Type']})*")
                                if s["Relationship to Next"] != "(destination)":
                                    parts.append(f" `{s['Relationship to Next']}` ")
                            st.markdown("**Path:** " + "".join(parts))

                    st.markdown("---")
                    st.subheader(f"Graph View — Shortest Path ({len(paths[0])-1} hops)")
                    with st.spinner("Rendering path visualisation…"):
                        try:
                            fig = explorer.visualize_path(paths[0])
                            _render_fig(fig)
                        except Exception as exc:
                            st.error(f"Visualisation error: {exc}")
                    st.caption("🟡 Gold = Source  |  🔴 Orange-Red = Target  |  🔵 Cyan = Path Nodes  |  Orange edges = path")

    # ================================================================
    # ANALYTICS DASHBOARD  (UNIQUE FEATURE B)
    # ================================================================
    elif current_page == PAGE_ANALYTICS:
        plt.close("all")   # Clear any lingering matplotlib state before rendering
        st.title("📈 Interactive Analytics Dashboard")
        st.markdown(
            "Visual analytics across all dimensions of the knowledge graph — "
            "entity mix, relationship breakdown, product reach, regional density, "
            "sales rep performance, and a product-segment heatmap."
        )

        at1, at2, at3, at4, at5 = st.tabs([
            "Entity & Relationship Mix",
            "Product Customer Reach",
            "Regional Density",
            "Sales Rep Performance",
            "Segment Heatmap",
        ])

        # ---- Tab 1: Entity & Relationship Mix ----
        with at1:
            st.subheader("Entity Type Distribution")
            try:
                etype_data = explorer.chart_entity_distribution()
                labels = list(etype_data.keys())
                values = list(etype_data.values())
                colors = ["#4CAF50","#2196F3","#FF9800","#9C27B0","#F44336","#00BCD4"]
                # Trim colors list to match label count
                colors = colors[:len(labels)]

                fig1, (ax_pie, ax_bar) = plt.subplots(1, 2, figsize=(13, 5))
                ax_pie.pie(values, labels=labels, colors=colors, autopct="%1.0f%%",
                           startangle=140, textprops={"fontsize": 8})
                ax_pie.set_title("Entity Mix", fontweight="bold")
                bars = ax_bar.barh(labels, values, color=colors)
                ax_bar.bar_label(bars, padding=3)
                ax_bar.set_xlabel("Count")
                ax_bar.set_title("Entity Counts by Type", fontweight="bold")
                ax_bar.invert_yaxis()
                fig1.tight_layout()
                _render_fig(fig1)
            except Exception as exc:
                st.error(f"Entity distribution chart error: {exc}")

            st.markdown("---")
            st.subheader("Relationship Type Distribution")
            try:
                rt_data   = explorer.chart_relationship_distribution()
                rt_labels = list(rt_data.keys())
                rt_values = list(rt_data.values())
                # Use tab10 colormap — has 10 colours, safe for up to 10 relationship types
                cmap = plt.get_cmap("tab10")
                bar_colors = [cmap(i % 10) for i in range(len(rt_labels))]

                fig2, ax2 = plt.subplots(figsize=(12, 4))
                bars2 = ax2.bar(rt_labels, rt_values, color=bar_colors, edgecolor="white")
                ax2.bar_label(bars2, padding=3)
                ax2.set_ylabel("Count")
                ax2.set_title("Relationship Counts by Type", fontweight="bold")
                ax2.tick_params(axis="x", rotation=25)
                fig2.tight_layout()
                _render_fig(fig2)
            except Exception as exc:
                st.error(f"Relationship distribution chart error: {exc}")

        # ---- Tab 2: Product Customer Reach ----
        with at2:
            st.subheader("Customer Reach per Product")
            st.markdown("Higher bars = broader market penetration.")
            try:
                reach_data = explorer.chart_product_customer_reach()
                prod_names = [d["Product"]   for d in reach_data]
                cust_cnts  = [d["Customers"] for d in reach_data]
                bar_cols   = ["#4CAF50" if c >= 3 else "#FFC107" if c == 2 else "#F44336"
                               for c in cust_cnts]

                fig3, ax3 = plt.subplots(figsize=(12, 5))
                bars3 = ax3.bar(prod_names, cust_cnts, color=bar_cols, edgecolor="white")
                ax3.bar_label(bars3, padding=3)
                ax3.set_ylabel("Number of Customers")
                ax3.set_title("Customer Reach by Product", fontweight="bold")
                ax3.tick_params(axis="x", rotation=20)
                ax3.legend(handles=[
                    mpatches.Patch(color="#4CAF50", label="High (>=3)"),
                    mpatches.Patch(color="#FFC107", label="Medium (2)"),
                    mpatches.Patch(color="#F44336", label="Low (1)"),
                ], fontsize=8)
                fig3.tight_layout()
                _render_fig(fig3)
            except Exception as exc:
                st.error(f"Customer reach chart error: {exc}")

        # ---- Tab 3: Regional Density ----
        with at3:
            st.subheader("Regional Commercial Density")
            st.markdown("Customer presence, product availability and distributor coverage per region.")
            try:
                region_rows = explorer.chart_region_density()
                reg_names   = [d["Region"]       for d in region_rows]
                cust_vals   = [d["Customers"]    for d in region_rows]
                prod_vals   = [d["Products"]     for d in region_rows]
                dist_vals   = [d["Distributors"] for d in region_rows]

                x   = np.arange(len(reg_names))   # numpy array for reliable bar positioning
                w   = 0.27

                fig4, ax4 = plt.subplots(figsize=(13, 5))
                b1 = ax4.bar(x - w,   cust_vals, w, label="Customers",    color="#2196F3")
                b2 = ax4.bar(x,       prod_vals, w, label="Products",     color="#4CAF50")
                b3 = ax4.bar(x + w,   dist_vals, w, label="Distributors", color="#9C27B0")
                for b in [b1, b2, b3]:
                    ax4.bar_label(b, padding=2, fontsize=7)
                ax4.set_xticks(x)
                ax4.set_xticklabels(reg_names, rotation=15)
                ax4.set_ylabel("Count")
                ax4.set_title("Regional Commercial Density", fontweight="bold")
                ax4.legend()
                fig4.tight_layout()
                _render_fig(fig4)

                st.markdown("**Summary Table**")
                st.dataframe(region_rows, use_container_width=True)
            except Exception as exc:
                st.error(f"Regional density chart error: {exc}")

        # ---- Tab 4: Sales Rep Performance ----
        with at4:
            st.subheader("Sales Representative Performance")
            try:
                rep_rows  = explorer.chart_rep_performance()
                rep_names = [d["Rep"]               for d in rep_rows]
                mgmt_vals = [d["Customers Managed"] for d in rep_rows]
                prom_vals = [d["Products Promoted"] for d in rep_rows]

                x5 = np.arange(len(rep_names))   # numpy array for reliable positioning
                w5 = 0.38

                fig5, ax5 = plt.subplots(figsize=(13, 5))
                bm = ax5.bar(x5 - w5/2, mgmt_vals, w5, label="Customers Managed", color="#2196F3")
                bp = ax5.bar(x5 + w5/2, prom_vals, w5, label="Products Promoted",  color="#FF9800")
                ax5.bar_label(bm, padding=2, fontsize=8)
                ax5.bar_label(bp, padding=2, fontsize=8)
                ax5.set_xticks(x5)
                ax5.set_xticklabels([n.split()[0] for n in rep_names], rotation=15)
                ax5.set_ylabel("Count")
                ax5.set_title("Sales Rep — Customers Managed vs Products Promoted", fontweight="bold")
                ax5.legend()
                fig5.tight_layout()
                _render_fig(fig5)

                st.markdown("**Full Rep Table**")
                st.dataframe(rep_rows, use_container_width=True)
            except Exception as exc:
                st.error(f"Sales rep chart error: {exc}")

        # ---- Tab 5: Segment Heatmap ----
        with at5:
            st.subheader("Product x Market Segment Heatmap")
            st.markdown("Which products target which segments? Green = targeted.")
            try:
                prod_names, seg_names, matrix = explorer.chart_segment_heatmap_data()

                fig6, ax6 = plt.subplots(figsize=(10, 7))
                im = ax6.imshow(matrix, cmap="Greens", aspect="auto", vmin=0, vmax=1)
                ax6.set_xticks(range(len(seg_names)))
                ax6.set_xticklabels(seg_names, rotation=30, ha="right", fontsize=9)
                ax6.set_yticks(range(len(prod_names)))
                ax6.set_yticklabels(prod_names, fontsize=9)
                for i in range(len(prod_names)):
                    for j in range(len(seg_names)):
                        val = int(matrix[i, j])   # numpy indexing — correct for 2D array
                        ax6.text(j, i, "\u2713" if val else "",
                                 ha="center", va="center",
                                 color="white" if val else "#DDDDDD", fontsize=13)
                ax6.set_title("Product x Market Segment Coverage", fontweight="bold", fontsize=12)
                fig6.colorbar(im, ax=ax6, fraction=0.03, pad=0.04, label="Targeted")
                fig6.tight_layout()
                _render_fig(fig6)
            except Exception as exc:
                st.error(f"Heatmap chart error: {exc}")

    # ================================================================
    # REPORT
    # ================================================================
    elif current_page == PAGE_REPORT:
        st.title("📄 Knowledge Graph Report")
        report_text = explorer.generate_report_text()
        st.text_area("Report Preview", report_text, height=600)
        st.download_button(
            label="Download Report (.txt)", data=report_text.encode("utf-8"),
            file_name="knowledge_graph_report.txt", mime="text/plain",
        )
        json_data = {"entities": [e.to_dict() for e in explorer.entities.values()],
                     "relationships": [r.to_dict() for r in explorer.relationships]}
        st.download_button(
            label="Download Graph Dataset (.json)",
            data=json.dumps(json_data, indent=2).encode("utf-8"),
            file_name="knowledge_graph_dataset.json", mime="application/json",
        )


# ============================================================
# ENTRY POINT
# ============================================================
# main class (entry point of the application)

if __name__ == "__main__":
    main()


#=======================================================================================================================
#END OF THE SCRIPT
#=======================================================================================================================
# Velox: Provenance-Based Intrusion Detection System - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Pipeline Stages](#pipeline-stages)
5. [Key Implementation Details](#key-implementation-details)
6. [Configuration](#configuration)
7. [How It Works](#how-it-works)
8. [Code Structure](#code-structure)

---

## Overview

**Velox** is a simplified yet effective provenance-based intrusion detection system (PIDS) from the PIDSMaker framework. The research paper "Sometimes Simpler is Better" demonstrates that Velox achieves maximum Anomaly Detection Performance (ADP) scores across multiple datasets using a minimalist architecture.

### Key Characteristics:
- **Simplicity**: Uses only a linear encoder (no complex GNN layers)
- **Effectiveness**: Achieves ADP scores of 0.93-1.00 across DARPA TC and OpTC datasets
- **Efficiency**: Faster than complex systems while maintaining high detection rates
- **Base Configuration**: Built on Orthrus architecture without "snooping" components

### What Velox Does:
Velox analyzes system provenance graphs (relationships between processes, files, and network connections) to detect malicious activity by learning normal behavior patterns and flagging anomalous nodes.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    VELOX PIPELINE                            │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  1. PREPROCESSING                                            │
│     └─> Build Graphs (Time Windows) ────────────────────┐   │
│                                                           │   │
│  2. FEATURIZATION                                         │   │
│     └─> Node Embeddings (Word2Vec on features) ─────────┤   │
│                                                           │   │
│  3. DETECTION                                             │   │
│     ├─> GNN Training (Linear Encoder Only)               │   │
│     │   └─> Edge Type Prediction Task                    │   │
│     └─> Inference (Compute Anomaly Scores) ──────────────┤   │
│                                                           │   │
│  4. EVALUATION                                            │   │
│     └─> Node Evaluation (Identify Malicious Nodes) ─────┘   │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. **Preprocessing Module** (`src/preprocessing/`)

#### Purpose:
Converts raw provenance data into time-windowed graphs suitable for analysis.

#### Key File: `build_orthrus_graphs.py`

**What it does:**
- Connects to PostgreSQL database containing provenance events
- Extracts three node types:
  - **Subject nodes**: Processes/programs (with type, path, command line)
  - **File nodes**: Files (with type, path)
  - **Netflow nodes**: Network connections (with type, IP, port)
- Creates time windows (default: 15 minutes)
- Builds directed graphs showing relationships between nodes

**Core Functions:**

```python
def compute_indexid2msg(cfg):
    """
    Maps node IDs to their features:
    Returns: {node_id: [node_type, label_string]}
    
    - Queries database for all nodes
    - Extracts relevant features based on config
    - Creates feature strings (e.g., "subject /bin/bash ps aux")
    """

def build_temporal_graphs_in_tw(cfg):
    """
    Constructs time-windowed graphs:
    
    1. Divides event stream into time windows
    2. For each window, creates a graph
    3. Adds edges with timestamps and types
    4. Splits into train/test datasets
    5. Saves graphs to disk
    """
```

**Graph Structure:**
- **Nodes**: System entities (processes, files, network connections)
- **Edges**: Interactions (e.g., process reads file, process connects to IP)
- **Edge Types**: Different interaction types (read, write, execute, etc.)
- **Temporal**: Each edge has a timestamp

---

### 2. **Featurization Module** (`src/featurization/`)

#### Purpose:
Converts node features (strings) into numerical embeddings that neural networks can process.

#### Method: `feature_word2vec`

**What it does:**
- Uses Word2Vec to embed node feature strings
- Unlike standard Word2Vec (which uses random walks), this uses actual node features
- Creates 128-dimensional embedding vectors for each unique node label

**Key File: `build_feature_word2vec.py`**

```python
def main(cfg):
    """
    Word2Vec-based node embedding:
    
    1. Loads indexid2msg (node features from preprocessing)
    2. Treats each node's feature string as a "sentence"
    3. Trains Word2Vec on these "sentences"
    4. Creates embedding lookup table
    5. Saves model to disk
    
    Parameters:
    - emb_dim: 128 (embedding dimension)
    - window_size: 5 (context window)
    - min_count: 1 (minimum word frequency)
    - use_skip_gram: True (Skip-gram vs CBOW)
    """
```

**Example:**
```
Node: "subject /usr/bin/python script.py"
  ↓ (Word2Vec)
128-dimensional vector: [0.23, -0.45, 0.12, ...]
```

---

### 3. **Detection Module** (`src/detection/`)

The heart of Velox's anomaly detection system.

#### 3.1 GNN Training (`gnn_training.py` → `orthrus_gnn_training.py`)

**Architecture:**

```
Input Features (Node Embeddings + Node Type)
    ↓
Linear Encoder (no GNN layers!)
    ↓ 
Edge Representations (source + destination)
    ↓
Edge MLP Decoder
    ↓
Edge Type Prediction
```

**What it does:**

The training process learns to predict edge types (interactions) between nodes:

```python
def train(data, full_data, model, optimizer, cfg):
    """
    Training loop for one epoch:
    
    1. Iterate through batches of edges
    2. Forward pass:
       - Embed nodes using linear layer
       - Concatenate source & destination embeddings
       - Predict edge type
    3. Compute loss (cross-entropy)
    4. Backpropagate and update weights
    5. Track losses
    
    Key Insight: Velox learns what normal edges look like.
    Abnormal edges (attacks) will have high prediction error.
    """

def main(cfg):
    """
    Full training process:
    
    1. Load data (train/val/test graphs)
    2. Build model (linear encoder + decoder)
    3. Train for N epochs (default: 8)
    4. Track validation performance
    5. Save best model
    6. Run inference on test data
    7. Save edge losses for evaluation
    """
```

**Model Architecture (`factory.py`):**

```python
def encoder_factory(cfg, ...):
    """
    Velox uses method = "none" which creates:
    LinearEncoder: Simple linear projection
    
    Input: node_emb (128) + node_type (one-hot)
           ↓
    Linear(input_dim → 128)
           ↓
    Output: 128-dim node representation
    """

def objective_factory(cfg, ...):
    """
    Velox uses: "predict_edge_type"
    
    Creates EdgeTypePrediction decoder:
    - Takes source and destination node embeddings
    - Concatenates them
    - Passes through MLP
    - Predicts edge type (classification)
    """
```

#### 3.2 Model Architecture (`model.py`)

**The Model Class:**

```python
class Model(nn.Module):
    """
    Main model combining encoder and decoder(s)
    
    Components:
    - encoder: Transforms node features to embeddings
    - decoders: List of objectives (edge type prediction)
    - graph_reindexer: Handles node indexing
    """
    
    def forward(self, batch, full_data, inference=False):
        """
        Forward pass:
        
        1. Embed nodes: h = encoder(batch)
        2. Get source/dest embeddings from edge_index
        3. Pass to decoder(s) to predict edge properties
        4. Return loss (training) or scores (inference)
        
        During training: Returns reconstruction loss
        During inference: Returns anomaly scores per edge
        """
```

#### 3.3 Encoder (`encoders.py`)

**LinearEncoder (Velox's Choice):**

```python
class LinearEncoder(nn.Module):
    """
    Simplest possible encoder - just a linear layer
    
    No message passing, no graph convolutions, no attention!
    
    Why it works:
    - Node embeddings already capture semantic meaning
    - Edge type prediction task is discriminative enough
    - Simpler = less overfitting
    """
    
    def __init__(self, in_dim, out_dim):
        self.linear = nn.Linear(in_dim, out_dim)
    
    def forward(self, x, **kwargs):
        return self.linear(x)
```

#### 3.4 Decoder (`decoders.py`)

**EdgeTypePrediction:**

```python
class EdgeTypePrediction(nn.Module):
    """
    Predicts edge types from node embeddings
    
    Architecture:
    h_src, h_dst → EdgeMLPDecoder → logits → CrossEntropy
    """
    
    def forward(self, h_src, h_dst, edge_type, inference, **kwargs):
        """
        Training mode:
        1. Predict edge type logits
        2. Compute cross-entropy loss vs ground truth
        3. Return loss
        
        Inference mode:
        1. Predict edge type logits
        2. Compute cross-entropy (higher = more anomalous)
        3. Return anomaly scores
        """

class EdgeMLPDecoder(nn.Module):
    """
    MLP that processes edge representations
    
    Steps:
    1. Project source node: lin_src(h_src)
    2. Project dest node: lin_dst(h_dst)
    3. Concatenate: [proj_src, proj_dst]
    4. Pass through MLP
    5. Output: edge type logits
    """
```

#### 3.5 Inference (`orthrus_gnn_testing.py`)

**What happens during inference:**

```python
def test(data, full_data, model, cfg, edge_losses_dir):
    """
    Inference process:
    
    1. Set model to eval mode (no training)
    2. For each time window graph:
       a. Forward pass through model
       b. Get anomaly scores for each edge
       c. Save scores to disk
    3. Aggregate scores by time window
    
    Anomaly scores = reconstruction error
    Higher score = more anomalous edge
    """
```

---

### 4. **Evaluation Module** (`src/detection/evaluation.py`)

#### Purpose:
Determines which nodes are malicious based on edge anomaly scores.

#### Key File: `node_evaluation.py`

**Evaluation Process:**

```python
def node_evaluation(val_tw_path, test_tw_path, model_epoch, cfg, tw_to_malicious_nodes):
    """
    Node-level anomaly detection:
    
    1. Load edge anomaly scores from inference
    2. Aggregate scores to node level (use destination nodes)
    3. Determine threshold (from validation set)
    4. Flag nodes above threshold as malicious
    5. Compare with ground truth
    6. Compute metrics:
       - ADP (Anomaly Detection Performance)
       - Precision/Recall
       - F1 Score
    """
```

**Threshold Selection:**

```python
def threshold_method: "max_val_loss"
    """
    Sets threshold to maximum anomaly score in validation set
    
    Intuition: 
    - Validation contains only benign activity
    - Any score higher than max validation score is anomalous
    - Conservative but effective approach
    """
```

**ADP Metric:**
- **Attack Detection Performance** per time window
- Binary: Did we detect at least one malicious node in the attack window?
- Average across all attack windows
- Velox achieves 0.93-1.00 ADP on evaluation datasets

---

## Pipeline Stages

### Stage 1: Build Graphs (`preprocessing.build_graphs`)

**Input:** PostgreSQL database with provenance events
**Output:** Time-windowed graphs saved to disk

**Process:**
1. Query database for all node types
2. Create node feature strings (e.g., "file /etc/passwd")
3. Query database for all edges
4. Divide edges into time windows (15 min default)
5. Create PyTorch Geometric Data objects
6. Save to `{dataset_dir}/graphs/`

**Files Generated:**
- `train_0.pkl`, `train_1.pkl`, ... (training graphs)
- `test_0.pkl`, `test_1.pkl`, ... (test graphs)
- `indexid2msg.pkl` (node feature mapping)

---

### Stage 2: Embed Nodes (`featurization.embed_nodes`)

**Input:** Node feature strings from preprocessing
**Output:** Node embedding model

**Process:**
1. Load `indexid2msg.pkl`
2. Extract feature strings for all nodes
3. Train Word2Vec model on these strings
4. Save model to `{dataset_dir}/node_embs/feature_word2vec/`

**Embedding Strategy:**
- Each node feature string is treated as a sentence
- Word2Vec learns semantic relationships between features
- Similar nodes get similar embeddings
- 128-dimensional vectors

---

### Stage 3: GNN Training (`detection.gnn_training`)

**Input:** Graphs + Node embeddings
**Output:** Trained model + Edge anomaly scores

**Training Process:**
```
For each epoch (1-8):
    For each training graph:
        For each edge batch:
            1. Load node embeddings
            2. Encode nodes (linear layer)
            3. Predict edge type
            4. Compute loss
            5. Backpropagate
    
    Validate on validation set
    If best validation score:
        Save model checkpoint
    
    If patience exceeded (3 epochs):
        Early stop

Load best model
Run inference on test set:
    For each test graph:
        Compute edge anomaly scores
        Save to disk
```

**Key Parameters:**
- `num_epochs`: 8
- `lr`: 0.0001 (learning rate)
- `patience`: 3 (early stopping)
- `node_out_dim`: 128 (embedding dimension)

---

### Stage 4: Evaluation (`detection.evaluation`)

**Input:** Edge anomaly scores + Ground truth labels
**Output:** Detection metrics (ADP, Precision, Recall, F1)

**Process:**
1. Load edge scores from inference
2. Aggregate to node level (sum/max of incident edges)
3. Determine threshold from validation set
4. Flag nodes exceeding threshold
5. Compare with ground truth malicious nodes
6. Compute metrics for each time window
7. Average across windows for final scores

---

## Key Implementation Details

### Data Loading (`data_utils.py`)

```python
def load_all_datasets(cfg):
    """
    Loads train, validation, and test data
    
    Returns:
    - train_data: List of training graphs
    - val_data: List of validation graphs
    - test_data: List of test graphs
    - full_data: Complete edge message lookup
    - max_node_num: Maximum node ID (for indexing)
    """
```

### Batch Processing (`data_utils.py`)

```python
class BatchLoaderFactory:
    """
    Creates batches from graphs for efficient processing
    
    Two modes:
    1. time_window: Each batch is one time window
    2. edges: Batch by number of edges (e.g., 1000 edges per batch)
    
    Velox uses time_window mode (batch per 15-min window)
    """
```

### Graph Reindexing (`data_utils.py`)

```python
class GraphReindexer:
    """
    Handles node ID mapping
    
    Problem: Node IDs in database can be large/sparse
    Solution: Remap to dense 0-N indexing for efficiency
    
    Methods:
    - _reindex_graph(): Convert global IDs to local batch IDs
    - Maintains mappings for later reconstruction
    """
```

### Loss Functions (`losses.py`)

```python
class ReconstructionLoss:
    """
    Cross-entropy loss for edge type prediction
    
    Training: Minimize prediction error on normal edges
    Inference: High loss = anomalous edge
    
    Can be balanced (weight rare edge types) or unbalanced
    Velox uses unbalanced: balanced_loss=False
    """
```

---

## Configuration

### Velox Configuration (`config/velox.yml`)

**Key Settings:**

```yaml
preprocessing:
  build_graphs:
    used_method: orthrus
    time_window_size: 15.0  # 15-minute windows
    node_label_features:     # Features to use
      subject: type, path, cmd_line
      file: type, path
      netflow: type, remote_ip, remote_port

featurization:
  embed_nodes:
    used_method: feature_word2vec
    emb_dim: 128             # Embedding dimension
    epochs: 50               # Word2Vec training epochs
    feature_word2vec:
      window_size: 5
      use_skip_gram: True

detection:
  gnn_training:
    used_method: orthrus
    num_epochs: 8            # Training epochs
    lr: 0.0001               # Learning rate
    node_out_dim: 128
    encoder:
      used_methods: none     # Linear encoder only!
      node_features: node_emb,node_type
      dropout: 0.3
    decoder:
      used_methods: predict_edge_type

  evaluation:
    used_method: node_evaluation
    node_evaluation:
      threshold_method: max_val_loss
      use_dst_node_loss: True  # Use destination node scores
```

### Tuned Configurations

For each dataset, there are tuned hyperparameters in:
`config/tuned_baselines/{dataset}/tuned_velox.yml`

These override default parameters with optimized values found through hyperparameter search.

---

## How It Works: Complete Example

### Scenario: Detecting a backdoor installation

**1. Normal Activity (Training):**
```
Process /usr/bin/bash --reads--> /etc/profile
Process /usr/bin/bash --executes--> /usr/bin/ls
Process /usr/bin/ls --reads--> /home/user
```

**2. Training Phase:**
- Model learns: bash reads profile, bash executes ls, ls reads directories
- Edge type predictions become accurate
- Reconstruction loss is low

**3. Attack Activity (Testing):**
```
Process /usr/bin/bash --writes--> /tmp/.backdoor
Process /tmp/.backdoor --connects--> 192.168.1.100:4444
```

**4. Detection Phase:**
- Model tries to predict edge types for attack edges
- Predictions are poor (never seen bash write to /tmp/.backdoor)
- Reconstruction loss is HIGH → Anomaly score is HIGH
- Nodes involved (/tmp/.backdoor) get flagged as malicious

**5. Evaluation:**
- Ground truth confirms /tmp/.backdoor is malicious
- Velox correctly flags it
- ADP = 1.0 (detected attack in time window)

---

## Code Structure

### Directory Layout
```
src/
├── benchmark.py              # Main entry point
├── config.py                 # Configuration management
├── model.py                  # Model wrapper class
├── encoders.py               # Encoder implementations
├── decoders.py               # Decoder implementations
├── losses.py                 # Loss functions
├── factory.py                # Factory functions for building components
├── data_utils.py             # Data loading and batching
│
├── preprocessing/
│   ├── build_graph_methods/
│   │   └── build_orthrus_graphs.py   # Graph construction
│   └── transformation.py             # Graph transformations
│
├── featurization/
│   └── embed_nodes_methods/
│       └── build_feature_word2vec.py  # Word2Vec embedding
│
├── detection/
│   ├── gnn_training.py               # Training entry point
│   ├── evaluation.py                 # Evaluation entry point
│   ├── training_methods/
│   │   ├── orthrus_gnn_training.py   # Training implementation
│   │   └── orthrus_gnn_testing.py    # Inference implementation
│   └── evaluation_methods/
│       └── node_evaluation.py        # Node-level evaluation
│
└── experiments/
    ├── tuning.py             # Hyperparameter tuning
    └── uncertainty.py        # Uncertainty estimation
```

### Execution Flow

**Command:**
```bash
./run_local.sh velox CADETS_E3 --tuned --from_weights
```

**Execution:**
1. `scripts/run_local.sh` → Launches Docker container
2. `src/benchmark.py` → Main pipeline orchestrator
3. `get_yml_cfg()` → Loads velox.yml + tuned params
4. Runs pipeline stages:
   - `build_graphs.main(cfg)`
   - `embed_nodes.main(cfg)`
   - `gnn_training.main(cfg)`
   - `evaluation.main(cfg)`
5. Logs results to WandB
6. Saves metrics to disk

---

## Key Insights: Why Velox Works

### 1. **Simplicity is Strength**
- No complex GNN layers (GAT, GCN, etc.)
- Just a linear encoder
- Avoids overfitting on limited attack samples

### 2. **Discriminative Task**
- Edge type prediction is sufficiently informative
- Normal edges have predictable types
- Attack edges have unusual patterns

### 3. **Semantic Embeddings**
- Word2Vec captures meaningful relationships
- Similar processes get similar embeddings
- Anomalies stand out in embedding space

### 4. **Temporal Granularity**
- 15-minute windows provide context
- Not too fine (noisy) or coarse (misses patterns)
- Balances detection and false positives

### 5. **Threshold Strategy**
- max_val_loss is conservative
- High precision (few false positives)
- Suitable for production systems

---

## Comparison to Other Systems

| System      | Encoder         | Decoder              | Edge Features | ADP (Avg) |
|-------------|----------------|---------------------|---------------|-----------|
| **Velox**   | Linear         | Edge Type Pred      | Type          | **0.95**  |
| Orthrus     | 2-layer GATv2  | Edge Type Pred      | Type          | 0.92      |
| NodLink     | 3-layer GAT    | Node Reconstruction | Type          | 0.88      |
| ThreatTrace | TGN + GAT      | Multi-task          | Type + Time   | 0.90      |
| Kairos      | TGN + Sage     | Edge Type Pred      | Type + Time   | 0.91      |

**Key Takeaway:** Velox achieves highest ADP with simplest architecture!

---

## Running Velox

### Prerequisites:
1. Docker installed
2. Datasets downloaded (DARPA TC, OpTC)
3. PostgreSQL setup with provenance data

### Quick Start:
```bash
# Clone repository
git clone https://github.com/ubc-provenance/PIDSMaker.git -b velox
cd PIDSMaker

# Setup (10 minutes)
# Follow: settings/ten-minute-install.md

# Run Velox on a dataset
cd scripts
./run_local.sh velox CADETS_E3 --tuned --from_weights
```

### Expected Output:
```
[@epoch07] Training finished - Mean Loss: 0.0234
[Validation] ADP: 1.00, Precision: 0.98, Recall: 1.00
[Test] ADP: 1.00, Precision: 0.97, Recall: 1.00
```

---

## Advanced Topics

### 1. **Hyperparameter Tuning**
- Uses WandB sweeps
- Grid search over learning rate, dropout, dimensions
- Saves best configs to `tuned_baselines/`

### 2. **Uncertainty Estimation**
- MC Dropout: Run inference multiple times with dropout
- Deep Ensembles: Train multiple models
- Helps quantify confidence in predictions

### 3. **Real-Time Detection**
- Change batch size to 1 edge (from 15-min windows)
- Lower latency, higher throughput needed
- Trade-off: accuracy vs speed

### 4. **Adversarial Robustness**
- Add mimicry edges during training
- Attackers try to blend in with normal traffic
- Velox maintains detection even with mimicry

---

## Metrics Explained

### **ADP (Anomaly Detection Performance)**
```
ADP = (# attack windows with ≥1 detected malicious node) / (# total attack windows)
```
Binary metric per time window, averaged across windows.

### **Precision**
```
Precision = True Positives / (True Positives + False Positives)
```
Of flagged nodes, how many are actually malicious?

### **Recall**
```
Recall = True Positives / (True Positives + False Negatives)
```
Of all malicious nodes, how many did we detect?

### **F1 Score**
```
F1 = 2 × (Precision × Recall) / (Precision + Recall)
```
Harmonic mean of precision and recall.

---

## Troubleshooting

### Issue: Low ADP scores
- Check threshold method (should be `max_val_loss`)
- Verify node embeddings were trained properly
- Ensure using destination node scores (`use_dst_node_loss: True`)

### Issue: Out of memory
- Reduce batch size
- Lower embedding dimension
- Use smaller time windows

### Issue: Training instability
- Try different random seeds
- Increase patience for early stopping
- Lower learning rate

---

## Citation

If you use Velox, cite the paper:

```bibtex
@inproceedings{bilot2025simpler,
    title={{Sometimes Simpler is Better: A Comprehensive Analysis of 
           State-of-the-Art Provenance-Based Intrusion Detection Systems}},
    author={Bilot, Tristan and Jiang, Baoxiang and Li, Zefeng and 
            El Madhoun, Nour and Al Agha, Khaldoun and Zouaoui, Anis and 
            Pasquier, Thomas},
    booktitle={Security Symposium (USENIX Sec'25)},
    year={2025},
    organization={USENIX}
}
```

---

## Resources

- **Paper**: [USENIX Security 2025](https://doi.org/10.5281/zenodo.15603122)
- **Code**: [GitHub - Velox Branch](https://github.com/ubc-provenance/PIDSMaker/tree/velox)
- **Main Branch**: [PIDSMaker Main](https://github.com/ubc-provenance/PIDSMaker)
- **Datasets**: DARPA TC (E3, E5), OpTC (H201, H501, H051)

---

## Summary

**Velox demonstrates that:**
1. Simplicity can outperform complexity in PIDS
2. Linear encoders + discriminative tasks are sufficient
3. Semantic embeddings capture enough information
4. High ADP is achievable without complex architectures
5. Practical deployment is more feasible with simpler systems

**Key Contribution:**
Challenges the assumption that more complex GNNs are always better for provenance-based intrusion detection.

---

*This documentation was created to provide a comprehensive understanding of the Velox system from the PIDSMaker repository's velox branch.*

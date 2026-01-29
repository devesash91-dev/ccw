/**
 * BlockchainTracer - Core tracing functionality for blockchain transactions
 * Similar to Arkham Intelligence Tracer
 */

class BlockchainTracer {
  constructor(config = {}) {
    this.config = {
      network: config.network || 'ethereum',
      maxDepth: config.maxDepth || 5,
      maxTransactionsPerAddress: config.maxTransactionsPerAddress || 10,
      maxTransactionsForPaths: config.maxTransactionsForPaths || 5,
      ...config
    };
  }

  /**
   * Trace transactions from a given address
   * @param {string} address - Starting address to trace from
   * @param {Object} options - Tracing options
   * @returns {Promise<Object>} - Transaction graph
   */
  async traceFromAddress(address, options = {}) {
    this._validateAddress(address);
    
    const depth = options.depth || this.config.maxDepth;
    const direction = options.direction || 'both'; // 'in', 'out', or 'both'
    
    console.log(`Tracing transactions for address: ${address}`);
    console.log(`Network: ${this.config.network}`);
    console.log(`Max depth: ${depth}`);
    
    const graph = {
      nodes: new Map(),
      edges: [],
      startAddress: address,
      metadata: {
        network: this.config.network,
        depth: depth,
        timestamp: new Date().toISOString()
      }
    };

    await this._traceRecursive(address, graph, 0, depth, direction);
    
    return this._formatGraph(graph);
  }

  /**
   * Trace a specific transaction
   * @param {string} txHash - Transaction hash to trace
   * @returns {Promise<Object>} - Transaction details
   */
  async traceTransaction(txHash) {
    this._validateTransactionHash(txHash);
    
    console.log(`Tracing transaction: ${txHash}`);
    console.log(`Network: ${this.config.network}`);
    
    const txDetails = await this._fetchTransactionDetails(txHash);
    
    const trace = {
      hash: txHash,
      from: txDetails.from,
      to: txDetails.to,
      value: txDetails.value,
      timestamp: txDetails.timestamp,
      status: txDetails.status,
      network: this.config.network,
      blockNumber: txDetails.blockNumber,
      gasUsed: txDetails.gasUsed,
      fee: txDetails.fee
    };
    
    // Trace both sender and receiver
    const graph = {
      transaction: trace,
      fromAddressFlow: await this._getAddressFlow(txDetails.from, 2),
      toAddressFlow: await this._getAddressFlow(txDetails.to, 2)
    };
    
    return graph;
  }

  /**
   * Trace fund flow between two addresses
   * @param {string} fromAddress - Starting address
   * @param {string} toAddress - Destination address
   * @returns {Promise<Array>} - Paths between addresses
   */
  async tracePath(fromAddress, toAddress) {
    this._validateAddress(fromAddress);
    this._validateAddress(toAddress);
    
    console.log(`Finding paths from ${fromAddress} to ${toAddress}`);
    
    const paths = [];
    const visited = new Set();
    
    await this._findPaths(fromAddress, toAddress, [fromAddress], visited, paths, 0, 5);
    
    return {
      from: fromAddress,
      to: toAddress,
      paths: paths,
      pathCount: paths.length,
      network: this.config.network
    };
  }

  /**
   * Get transaction flow for an address
   * @param {string} address - Address to analyze
   * @param {number} depth - Analysis depth
   * @returns {Promise<Object>} - Flow analysis
   */
  async _getAddressFlow(address, depth) {
    const flow = {
      address: address,
      incoming: [],
      outgoing: [],
      totalIn: 0,
      totalOut: 0,
      transactionCount: 0
    };

    try {
      const transactions = await this._fetchAddressTransactions(address, depth);
      
      transactions.forEach(tx => {
        if (tx.to && tx.to.toLowerCase() === address.toLowerCase()) {
          flow.incoming.push(tx);
          flow.totalIn += parseFloat(tx.value) || 0;
        }
        if (tx.from && tx.from.toLowerCase() === address.toLowerCase()) {
          flow.outgoing.push(tx);
          flow.totalOut += parseFloat(tx.value) || 0;
        }
      });
      
      flow.transactionCount = transactions.length;
      flow.netFlow = flow.totalIn - flow.totalOut;
    } catch (error) {
      console.warn(`Could not fetch flow for ${address}: ${error.message}`);
    }

    return flow;
  }

  /**
   * Recursive tracing helper
   */
  async _traceRecursive(address, graph, currentDepth, maxDepth, direction) {
    if (currentDepth >= maxDepth) {
      return;
    }

    if (graph.nodes.has(address)) {
      return;
    }

    graph.nodes.set(address, {
      address: address,
      depth: currentDepth,
      type: currentDepth === 0 ? 'origin' : 'intermediary'
    });

    try {
      const transactions = await this._fetchAddressTransactions(address, 1);
      
      for (const tx of transactions.slice(0, this.config.maxTransactionsPerAddress)) {
        if (direction === 'out' || direction === 'both') {
          if (tx.from && tx.from.toLowerCase() === address.toLowerCase() && tx.to) {
            graph.edges.push({
              from: tx.from,
              to: tx.to,
              value: tx.value,
              hash: tx.hash,
              timestamp: tx.timestamp
            });
            
            if (currentDepth + 1 < maxDepth) {
              await this._traceRecursive(tx.to, graph, currentDepth + 1, maxDepth, direction);
            }
          }
        }
        
        if (direction === 'in' || direction === 'both') {
          if (tx.to && tx.to.toLowerCase() === address.toLowerCase() && tx.from) {
            graph.edges.push({
              from: tx.from,
              to: tx.to,
              value: tx.value,
              hash: tx.hash,
              timestamp: tx.timestamp
            });
            
            if (currentDepth + 1 < maxDepth) {
              await this._traceRecursive(tx.from, graph, currentDepth + 1, maxDepth, direction);
            }
          }
        }
      }
    } catch (error) {
      console.warn(`Could not trace address ${address}: ${error.message}`);
    }
  }

  /**
   * Find paths between two addresses
   */
  async _findPaths(current, target, path, visited, paths, depth, maxDepth) {
    if (depth >= maxDepth || paths.length >= 10) {
      return;
    }

    if (current.toLowerCase() === target.toLowerCase()) {
      paths.push([...path]);
      return;
    }

    visited.add(current.toLowerCase());

    try {
      const transactions = await this._fetchAddressTransactions(current, 1);
      
      for (const tx of transactions.slice(0, this.config.maxTransactionsForPaths)) {
        if (tx.from && tx.from.toLowerCase() === current.toLowerCase() && tx.to) {
          const next = tx.to;
          if (!visited.has(next.toLowerCase())) {
            await this._findPaths(next, target, [...path, next], visited, paths, depth + 1, maxDepth);
          }
        }
      }
    } catch (error) {
      console.warn(`Error finding paths from ${current}: ${error.message}`);
    }

    visited.delete(current.toLowerCase());
  }

  /**
   * Fetch transaction details
   */
  async _fetchTransactionDetails(txHash) {
    // Mock implementation - in real scenario, would call blockchain API
    // For demonstration purposes, return mock data
    return {
      hash: txHash,
      from: '0x' + '1'.repeat(40),
      to: '0x' + '2'.repeat(40),
      value: '1.5',
      timestamp: Date.now(),
      status: 'success',
      blockNumber: 12345678,
      gasUsed: 21000,
      fee: '0.001'
    };
  }

  /**
   * Fetch transactions for an address
   */
  async _fetchAddressTransactions(address, limit = 10) {
    // Mock implementation - in real scenario, would call blockchain API
    // For demonstration purposes, return mock data
    const transactions = [];
    
    for (let i = 0; i < Math.min(limit, 5); i++) {
      transactions.push({
        hash: '0x' + Math.random().toString(16).slice(2, 66),
        from: address,
        to: '0x' + Math.random().toString(16).slice(2, 42),
        value: (Math.random() * 10).toFixed(4),
        timestamp: Date.now() - (i * 3600000),
        blockNumber: 12345678 - i
      });
    }
    
    return transactions;
  }

  /**
   * Format graph for output
   */
  _formatGraph(graph) {
    return {
      nodes: Array.from(graph.nodes.values()),
      edges: graph.edges,
      startAddress: graph.startAddress,
      metadata: graph.metadata,
      summary: {
        nodeCount: graph.nodes.size,
        edgeCount: graph.edges.length,
        totalValue: graph.edges.reduce((sum, edge) => sum + (parseFloat(edge.value) || 0), 0)
      }
    };
  }

  /**
   * Export graph to various formats
   */
  exportGraph(graph, format = 'json') {
    switch (format) {
      case 'json':
        return JSON.stringify(graph, null, 2);
      case 'dot':
        return this._exportToDot(graph);
      case 'csv':
        return this._exportToCsv(graph);
      default:
        throw new Error(`Unsupported format: ${format}`);
    }
  }

  /**
   * Export to DOT format for graph visualization
   */
  _exportToDot(graph) {
    let dot = 'digraph TransactionFlow {\n';
    dot += '  rankdir=LR;\n';
    dot += '  node [shape=box, style=rounded];\n\n';
    
    // Add nodes
    graph.nodes.forEach(node => {
      const label = node.address.substring(0, 10) + '...';
      const color = node.type === 'origin' ? 'lightblue' : 'lightgray';
      dot += `  "${node.address}" [label="${label}", fillcolor=${color}, style=filled];\n`;
    });
    
    dot += '\n';
    
    // Add edges
    graph.edges.forEach(edge => {
      const label = `${edge.value}`;
      dot += `  "${edge.from}" -> "${edge.to}" [label="${label}"];\n`;
    });
    
    dot += '}\n';
    return dot;
  }

  /**
   * Export to CSV format
   */
  _exportToCsv(graph) {
    let csv = 'From,To,Value,Hash,Timestamp\n';
    
    graph.edges.forEach(edge => {
      csv += `${edge.from},${edge.to},${edge.value},${edge.hash},${edge.timestamp}\n`;
    });
    
    return csv;
  }

  /**
   * Validate Ethereum address format
   */
  _validateAddress(address) {
    if (!address || typeof address !== 'string') {
      throw new Error('Address must be a non-empty string');
    }
    
    // Basic validation for Ethereum addresses (0x followed by 40 hex characters)
    // This is a simplified check - real implementation would be more thorough
    if (this.config.network === 'ethereum') {
      if (!/^0x[a-fA-F0-9]{40}$/.test(address) && address.length > 5) {
        // Allow partial addresses for demo purposes
        console.warn(`Warning: Address ${address} may not be a valid Ethereum address`);
      }
    }
  }

  /**
   * Validate transaction hash format
   */
  _validateTransactionHash(txHash) {
    if (!txHash || typeof txHash !== 'string') {
      throw new Error('Transaction hash must be a non-empty string');
    }
    
    // Basic validation for transaction hashes
    if (this.config.network === 'ethereum') {
      if (!/^0x[a-fA-F0-9]{64}$/.test(txHash) && txHash.length > 5) {
        // Allow partial hashes for demo purposes
        console.warn(`Warning: Transaction hash ${txHash} may not be a valid Ethereum transaction hash`);
      }
    }
  }
}

export default BlockchainTracer;

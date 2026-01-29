# CCW Tracer Examples

This directory contains examples of using the CCW Blockchain Tracer.

## Basic Usage Examples

### Example 1: Trace an Address

```javascript
import BlockchainTracer from '../src/tracer.js';

async function example1() {
  const tracer = new BlockchainTracer({
    network: 'ethereum',
    maxDepth: 3
  });

  const result = await tracer.traceFromAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb');
  
  console.log('Trace Results:');
  console.log(`- Nodes: ${result.summary.nodeCount}`);
  console.log(`- Transactions: ${result.summary.edgeCount}`);
  console.log(`- Total Value: ${result.summary.totalValue}`);
}

example1();
```

### Example 2: Trace a Transaction

```javascript
import BlockchainTracer from '../src/tracer.js';

async function example2() {
  const tracer = new BlockchainTracer({ network: 'ethereum' });

  const result = await tracer.traceTransaction('0xabc123def456...');
  
  console.log('Transaction Details:');
  console.log(`- From: ${result.transaction.from}`);
  console.log(`- To: ${result.transaction.to}`);
  console.log(`- Value: ${result.transaction.value}`);
  console.log(`- Status: ${result.transaction.status}`);
}

example2();
```

### Example 3: Find Paths Between Addresses

```javascript
import BlockchainTracer from '../src/tracer.js';

async function example3() {
  const tracer = new BlockchainTracer({ network: 'ethereum' });

  const from = '0x111...';
  const to = '0x222...';
  
  const result = await tracer.tracePath(from, to);
  
  console.log(`Found ${result.pathCount} paths from ${from} to ${to}`);
  
  result.paths.forEach((path, index) => {
    console.log(`\nPath ${index + 1}:`);
    path.forEach((address, i) => {
      console.log(`  ${i + 1}. ${address}`);
    });
  });
}

example3();
```

### Example 4: Export to Different Formats

```javascript
import BlockchainTracer from '../src/tracer.js';
import fs from 'fs';

async function example4() {
  const tracer = new BlockchainTracer({ network: 'ethereum' });

  const graph = await tracer.traceFromAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb');
  
  // Export as JSON
  const json = tracer.exportGraph(graph, 'json');
  fs.writeFileSync('output.json', json);
  
  // Export as DOT (for Graphviz)
  const dot = tracer.exportGraph(graph, 'dot');
  fs.writeFileSync('output.dot', dot);
  
  // Export as CSV
  const csv = tracer.exportGraph(graph, 'csv');
  fs.writeFileSync('output.csv', csv);
  
  console.log('Exported to multiple formats!');
}

example4();
```

### Example 5: Custom Configuration

```javascript
import BlockchainTracer from '../src/tracer.js';

async function example5() {
  const tracer = new BlockchainTracer({
    network: 'ethereum',
    maxDepth: 10,
    maxTransactionsPerAddress: 20,  // Trace more transactions per address
    maxTransactionsForPaths: 10     // Search more transactions for paths
  });

  const result = await tracer.traceFromAddress('0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb', {
    depth: 5,
    direction: 'out'  // Only outgoing transactions
  });
  
  console.log('Custom trace completed!');
}

example5();
```

## CLI Examples

### Trace an address with depth 3

```bash
node ../src/cli.js trace 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --depth 3 --output trace.json
```

### Trace only outgoing transactions

```bash
node ../src/cli.js trace 0xaddress... --direction out --depth 2
```

### Export as DOT for visualization

```bash
node ../src/cli.js trace 0xaddress... --format dot --output graph.dot
dot -Tpng graph.dot -o graph.png
```

### Trace a transaction

```bash
node ../src/cli.js tx 0x1234567890abcdef... --output tx.json
```

### Find paths between two addresses

```bash
node ../src/cli.js path 0xfrom... 0xto... --output paths.json
```

## Advanced Examples

### Example 6: Analyze Transaction Flow

```javascript
import BlockchainTracer from '../src/tracer.js';

async function analyzeTransactionFlow() {
  const tracer = new BlockchainTracer({ network: 'ethereum' });
  
  const addresses = [
    '0x111...',
    '0x222...',
    '0x333...'
  ];
  
  for (const address of addresses) {
    console.log(`\nAnalyzing ${address}...`);
    
    // Trace the address to get flow information
    const result = await tracer.traceFromAddress(address, { depth: 1 });
    
    console.log(`- Nodes found: ${result.summary.nodeCount}`);
    console.log(`- Transactions: ${result.summary.edgeCount}`);
    console.log(`- Total value: ${result.summary.totalValue}`);
  }
}

analyzeTransactionFlow();
```

## Visualization

After exporting to DOT format, use Graphviz to create visualizations:

```bash
# Install Graphviz
sudo apt-get install graphviz  # Ubuntu/Debian
brew install graphviz          # macOS

# Create PNG visualization
dot -Tpng graph.dot -o graph.png

# Create SVG visualization
dot -Tsvg graph.dot -o graph.svg

# Create interactive HTML
dot -Tsvg graph.dot | dot2html > graph.html
```

## Notes

- These examples use mock data for demonstration purposes
- For production use, integrate with real blockchain APIs
- Remember to handle API rate limits and errors properly
- Always validate addresses before tracing

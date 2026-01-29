/**
 * Tests for BlockchainTracer
 */

import { test } from 'node:test';
import assert from 'node:assert';
import BlockchainTracer from '../src/tracer.js';

test('BlockchainTracer - constructor creates instance with default config', () => {
  const tracer = new BlockchainTracer();
  
  assert.strictEqual(tracer.config.network, 'ethereum');
  assert.strictEqual(tracer.config.maxDepth, 5);
  assert.strictEqual(tracer.config.maxTransactionsPerAddress, 10);
  assert.strictEqual(tracer.config.maxTransactionsForPaths, 5);
});

test('BlockchainTracer - constructor accepts custom config', () => {
  const config = {
    network: 'bitcoin',
    maxDepth: 10,
    maxTransactionsPerAddress: 20
  };
  
  const tracer = new BlockchainTracer(config);
  
  assert.strictEqual(tracer.config.network, 'bitcoin');
  assert.strictEqual(tracer.config.maxDepth, 10);
  assert.strictEqual(tracer.config.maxTransactionsPerAddress, 20);
});

test('BlockchainTracer - traceFromAddress returns graph structure', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const result = await tracer.traceFromAddress(address, { depth: 2 });
  
  assert.ok(result.nodes);
  assert.ok(Array.isArray(result.nodes));
  assert.ok(result.edges);
  assert.ok(Array.isArray(result.edges));
  assert.strictEqual(result.startAddress, address);
  assert.ok(result.metadata);
  assert.ok(result.summary);
  assert.ok(typeof result.summary.nodeCount === 'number');
  assert.ok(typeof result.summary.edgeCount === 'number');
  assert.ok(typeof result.summary.totalValue === 'number');
});

test('BlockchainTracer - traceTransaction returns transaction details', async () => {
  const tracer = new BlockchainTracer();
  const txHash = '0x1234567890abcdef';
  
  const result = await tracer.traceTransaction(txHash);
  
  assert.ok(result.transaction);
  assert.strictEqual(result.transaction.hash, txHash);
  assert.ok(result.transaction.from);
  assert.ok(result.transaction.to);
  assert.ok(result.transaction.value);
  assert.ok(result.transaction.timestamp);
  assert.ok(result.fromAddressFlow);
  assert.ok(result.toAddressFlow);
});

test('BlockchainTracer - tracePath returns paths between addresses', async () => {
  const tracer = new BlockchainTracer();
  const from = '0x111...';
  const to = '0x222...';
  
  const result = await tracer.tracePath(from, to);
  
  assert.strictEqual(result.from, from);
  assert.strictEqual(result.to, to);
  assert.ok(Array.isArray(result.paths));
  assert.ok(typeof result.pathCount === 'number');
  assert.strictEqual(result.network, 'ethereum');
});

test('BlockchainTracer - exportGraph supports json format', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const graph = await tracer.traceFromAddress(address, { depth: 1 });
  const json = tracer.exportGraph(graph, 'json');
  
  assert.ok(typeof json === 'string');
  const parsed = JSON.parse(json);
  assert.ok(parsed.nodes);
  assert.ok(parsed.edges);
});

test('BlockchainTracer - exportGraph supports dot format', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const graph = await tracer.traceFromAddress(address, { depth: 1 });
  const dot = tracer.exportGraph(graph, 'dot');
  
  assert.ok(typeof dot === 'string');
  assert.ok(dot.includes('digraph TransactionFlow'));
  assert.ok(dot.includes('rankdir=LR'));
});

test('BlockchainTracer - exportGraph supports csv format', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const graph = await tracer.traceFromAddress(address, { depth: 1 });
  const csv = tracer.exportGraph(graph, 'csv');
  
  assert.ok(typeof csv === 'string');
  assert.ok(csv.includes('From,To,Value,Hash,Timestamp'));
});

test('BlockchainTracer - exportGraph throws on unsupported format', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const graph = await tracer.traceFromAddress(address, { depth: 1 });
  
  assert.throws(
    () => tracer.exportGraph(graph, 'invalid'),
    /Unsupported format/
  );
});

test('BlockchainTracer - _getAddressFlow returns flow analysis', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const flow = await tracer._getAddressFlow(address, 2);
  
  assert.strictEqual(flow.address, address);
  assert.ok(Array.isArray(flow.incoming));
  assert.ok(Array.isArray(flow.outgoing));
  assert.ok(typeof flow.totalIn === 'number');
  assert.ok(typeof flow.totalOut === 'number');
  assert.ok(typeof flow.transactionCount === 'number');
  assert.ok(typeof flow.netFlow === 'number');
});

test('BlockchainTracer - handles different trace directions', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const inResult = await tracer.traceFromAddress(address, { depth: 1, direction: 'in' });
  const outResult = await tracer.traceFromAddress(address, { depth: 1, direction: 'out' });
  const bothResult = await tracer.traceFromAddress(address, { depth: 1, direction: 'both' });
  
  assert.ok(inResult.nodes);
  assert.ok(outResult.nodes);
  assert.ok(bothResult.nodes);
});

test('BlockchainTracer - respects maxDepth configuration', async () => {
  const tracer = new BlockchainTracer({ maxDepth: 2 });
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const result = await tracer.traceFromAddress(address);
  
  // All nodes should have depth <= maxDepth
  result.nodes.forEach(node => {
    assert.ok(node.depth <= 2);
  });
});

test('BlockchainTracer - graph contains metadata', async () => {
  const tracer = new BlockchainTracer({ network: 'ethereum' });
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const result = await tracer.traceFromAddress(address, { depth: 2 });
  
  assert.strictEqual(result.metadata.network, 'ethereum');
  assert.strictEqual(result.metadata.depth, 2);
  assert.ok(result.metadata.timestamp);
});

test('BlockchainTracer - summary calculates totals correctly', async () => {
  const tracer = new BlockchainTracer();
  const address = '0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb';
  
  const result = await tracer.traceFromAddress(address, { depth: 2 });
  
  assert.strictEqual(result.summary.nodeCount, result.nodes.length);
  assert.strictEqual(result.summary.edgeCount, result.edges.length);
  
  // Verify total value matches sum of edge values
  const calculatedTotal = result.edges.reduce((sum, edge) => {
    return sum + (parseFloat(edge.value) || 0);
  }, 0);
  
  assert.ok(Math.abs(result.summary.totalValue - calculatedTotal) < 0.0001);
});

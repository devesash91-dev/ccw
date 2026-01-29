#!/usr/bin/env node

/**
 * CCW Blockchain Tracer CLI
 * Command-line interface for tracing blockchain transactions
 */

import BlockchainTracer from './tracer.js';
import fs from 'fs';
import { promisify } from 'util';

const writeFile = promisify(fs.writeFile);

// Parse command line arguments
const args = process.argv.slice(2);

const commands = {
  help: showHelp,
  trace: traceAddress,
  tx: traceTransaction,
  path: tracePath,
  version: showVersion
};

async function main() {
  if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
    showHelp();
    return;
  }

  const command = args[0];
  
  if (commands[command]) {
    await commands[command]();
  } else {
    console.error(`Unknown command: ${command}`);
    console.error('Run "ccw-tracer help" for usage information.');
    process.exit(1);
  }
}

function showHelp() {
  console.log(`
CCW Blockchain Tracer - Transaction Tracing Tool
Similar to Arkham Intelligence Tracer

Usage:
  ccw-tracer <command> [options]

Commands:
  trace <address>              Trace transactions from an address
    --depth <n>                Maximum trace depth (default: 5)
    --network <name>           Blockchain network (ethereum, bitcoin)
    --direction <dir>          Trace direction: in, out, both (default: both)
    --output <file>            Save results to file
    --format <fmt>             Output format: json, dot, csv (default: json)

  tx <hash>                    Trace a specific transaction
    --network <name>           Blockchain network (default: ethereum)
    --output <file>            Save results to file

  path <from> <to>             Find transaction paths between addresses
    --network <name>           Blockchain network (default: ethereum)
    --output <file>            Save results to file

  version                      Show version information
  help                         Show this help message

Examples:
  ccw-tracer trace 0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb --depth 3
  ccw-tracer tx 0xabc123... --network ethereum
  ccw-tracer path 0xfrom... 0xto... --output path.json

For more information, visit: https://github.com/devesash91-dev/ccw
`);
}

function showVersion() {
  console.log('CCW Blockchain Tracer v1.0.0');
}

async function traceAddress() {
  const address = args[1];
  
  if (!address) {
    console.error('Error: Address required');
    console.error('Usage: ccw-tracer trace <address> [options]');
    process.exit(1);
  }

  // Parse options
  const options = parseOptions(args.slice(2));
  
  const config = {
    network: options.network || 'ethereum',
    maxDepth: parseInt(options.depth) || 5
  };

  console.log('\n🔍 CCW Blockchain Tracer\n');
  
  const tracer = new BlockchainTracer(config);
  
  try {
    const result = await tracer.traceFromAddress(address, {
      depth: config.maxDepth,
      direction: options.direction || 'both'
    });

    console.log('\n✅ Trace completed!\n');
    console.log(`Nodes: ${result.summary.nodeCount}`);
    console.log(`Transactions: ${result.summary.edgeCount}`);
    console.log(`Total value: ${result.summary.totalValue.toFixed(4)}\n`);

    // Output result
    const format = options.format || 'json';
    const output = tracer.exportGraph(result, format);

    if (options.output) {
      await writeFile(options.output, output);
      console.log(`Results saved to: ${options.output}`);
    } else {
      console.log(output);
    }
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

async function traceTransaction() {
  const txHash = args[1];
  
  if (!txHash) {
    console.error('Error: Transaction hash required');
    console.error('Usage: ccw-tracer tx <hash> [options]');
    process.exit(1);
  }

  const options = parseOptions(args.slice(2));
  
  const config = {
    network: options.network || 'ethereum'
  };

  console.log('\n🔍 CCW Blockchain Tracer - Transaction Trace\n');
  
  const tracer = new BlockchainTracer(config);
  
  try {
    const result = await tracer.traceTransaction(txHash);

    console.log('\n✅ Transaction traced!\n');
    console.log(`Hash: ${result.transaction.hash}`);
    console.log(`From: ${result.transaction.from}`);
    console.log(`To: ${result.transaction.to}`);
    console.log(`Value: ${result.transaction.value}`);
    console.log(`Status: ${result.transaction.status}\n`);

    const output = JSON.stringify(result, null, 2);

    if (options.output) {
      await writeFile(options.output, output);
      console.log(`Results saved to: ${options.output}`);
    } else {
      console.log(output);
    }
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

async function tracePath() {
  const fromAddress = args[1];
  const toAddress = args[2];
  
  if (!fromAddress || !toAddress) {
    console.error('Error: Both from and to addresses required');
    console.error('Usage: ccw-tracer path <from> <to> [options]');
    process.exit(1);
  }

  const options = parseOptions(args.slice(3));
  
  const config = {
    network: options.network || 'ethereum'
  };

  console.log('\n🔍 CCW Blockchain Tracer - Path Finding\n');
  
  const tracer = new BlockchainTracer(config);
  
  try {
    const result = await tracer.tracePath(fromAddress, toAddress);

    console.log('\n✅ Path search completed!\n');
    console.log(`Paths found: ${result.pathCount}\n`);

    const output = JSON.stringify(result, null, 2);

    if (options.output) {
      await writeFile(options.output, output);
      console.log(`Results saved to: ${options.output}`);
    } else {
      console.log(output);
    }
  } catch (error) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  }
}

function parseOptions(args) {
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].substring(2);
      const value = args[i + 1];
      
      if (value && !value.startsWith('--')) {
        options[key] = value;
        i++;
      }
    }
  }
  
  return options;
}

// Run CLI
main().catch(error => {
  console.error(`Fatal error: ${error.message}`);
  process.exit(1);
});

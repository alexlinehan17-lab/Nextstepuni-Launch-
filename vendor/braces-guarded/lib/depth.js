'use strict';

// Fixed ceiling: options.maxLength or a caller-supplied AST cannot relax it.
const MAX_DEPTH = 64;
const assertDepth = depth => {
  if (depth > MAX_DEPTH) {
    throw new SyntaxError(`Brace pattern nesting exceeds the safe limit (${MAX_DEPTH})`);
  }
};

// Validate iteratively before entering upstream's recursive walkers. This also
// bounds a directly supplied AST, including cycles in its child-node graph.
const assertTreeDepth = ast => {
  const pending = [{ node: ast, depth: 0 }];
  while (pending.length) {
    const { node, depth } = pending.pop();
    assertDepth(depth);
    if (node && Array.isArray(node.nodes)) {
      for (const child of node.nodes) pending.push({ node: child, depth: depth + 1 });
    }
  }
};

module.exports = { MAX_DEPTH, assertDepth, assertTreeDepth };

/**
 * Test suite for core functionality fixes
 * Run: node test_fixes.js
 */

const KALLAX = { depth: 39, width: 33, height: 33 };

// Test 1: calcFit function - improved rotation handling
function calcFit(game) {
  const d = game.dims;
  // Check if game can fit in ANY rotation
  // Kallax internal: 33cm width × 33cm height × 39cm depth
  const dims = [d.l, d.w, d.h].sort((a, b) => a - b);
  const [smallest, middle, largest] = dims;
  
  if (smallest <= KALLAX.width && middle <= KALLAX.height && largest <= KALLAX.depth) {
    return 'yes';
  }
  return 'toobig';
}

// Test cases: [name, dims, expected]
const fitTestCases = [
  // Fits cases
  ['Standard box', { l: 29.5, w: 29.5, h: 7.5 }, 'yes'],
  ['Large box', { l: 37, w: 27, h: 9 }, 'yes'],
  ['Gloomhaven (too big)', { l: 41, w: 29.5, h: 17 }, 'toobig'],  // 41cm > 39cm depth
  ['Twilight Imperium (too big)', { l: 43, w: 30, h: 13 }, 'toobig'],  // 43cm > 39cm depth
  ['Card game', { l: 13, w: 10, h: 4 }, 'yes'],
  ['Any rotation 30x30x39', { l: 30, w: 30, h: 39 }, 'yes'],
  ['Rotated 39x33x30', { l: 39, w: 33, h: 30 }, 'yes'],
  
  // Too big cases
  ['Too tall: 30x30x40', { l: 30, w: 30, h: 40 }, 'toobig'],
  ['Too wide: 34x34x39', { l: 34, w: 34, h: 39 }, 'toobig'],
  ['All too big: 40x40x40', { l: 40, w: 40, h: 40 }, 'toobig'],
  ['One dim too big: 33x33x40', { l: 33, w: 33, h: 40 }, 'toobig'],
];

console.log('=== Testing calcFit() rotation handling ===\n');
let fitPassed = 0;
fitTestCases.forEach(([name, dims, expected]) => {
  const result = calcFit({ dims });
  const passed = result === expected;
  fitPassed += passed ? 1 : 0;
  console.log(`${passed ? '✅' : '❌'} ${name}: got "${result}", expected "${expected}"`);
});
console.log(`\nPassed: ${fitPassed}/${fitTestCases.length}\n`);

// Test 2: Dimension validation
function validateDimensions(l, w, h) {
  const errors = [];
  if (!l || !w || !h || l <= 0 || w <= 0 || h <= 0) {
    errors.push('All dimensions must be positive numbers greater than 0');
  }
  if (l > 200 || w > 200 || h > 200) {
    errors.push('Dimensions must be less than 200cm');
  }
  return errors;
}

const dimValidationCases = [
  [29.5, 29.5, 7.5, []],           // Valid
  [0, 29.5, 7.5, ['positive']],    // Invalid - zero
  [NaN, 29.5, 7.5, ['positive']],  // Invalid - NaN
  [200.1, 29.5, 7.5, ['200cm']],   // Invalid - too large
  [29.5, 29.5, -5, ['positive']],  // Invalid - negative
];

console.log('=== Testing dimension validation ===\n');
let dimPassed = 0;
dimValidationCases.forEach(([l, w, h, expectedErrorType]) => {
  const errors = validateDimensions(l, w, h);
  const passed = 
    (expectedErrorType.length === 0 && errors.length === 0) ||
    (expectedErrorType.length > 0 && errors.length > 0);
  dimPassed += passed ? 1 : 0;
  console.log(`${passed ? '✅' : '❌'} ${l}×${w}×${h}: ${errors.length === 0 ? 'VALID' : 'INVALID - ' + errors.join(', ')}`);
});
console.log(`\nPassed: ${dimPassed}/${dimValidationCases.length}\n`);

// Test 3: Cache validation
function validateCache(cache) {
  try {
    if (!cache) return false;
    if (!cache.username || !Array.isArray(cache.games) || cache.games.length === 0) return false;
    for (const game of cache.games) {
      if (!game.id || !game.name) return false;
    }
    return true;
  } catch (e) {
    return false;
  }
}

const cacheTestCases = [
  [null, false],
  [{}, false],
  [{ username: 'test', games: [] }, false],
  [{ username: 'test', games: [{ id: 1, name: 'Game1' }] }, true],
  [{ username: 'test', games: [{ id: 1 }] }, false], // missing name
  [{ games: [{ id: 1, name: 'Game1' }] }, false],    // missing username
];

console.log('=== Testing cache validation ===\n');
let cachePassed = 0;
cacheTestCases.forEach((testCase, idx) => {
  const [cache, expected] = testCase;
  const result = validateCache(cache);
  const passed = result === expected;
  cachePassed += passed ? 1 : 0;
  console.log(`${passed ? '✅' : '❌'} Test ${idx + 1}: ${result === expected ? 'PASS' : 'FAIL'}`);
});
console.log(`\nPassed: ${cachePassed}/${cacheTestCases.length}\n`);

// Summary
const totalTests = fitTestCases.length + dimValidationCases.length + cacheTestCases.length;
const totalPassed = fitPassed + dimPassed + cachePassed;
console.log(`\n${'═'.repeat(40)}`);
console.log(`🧪 Overall: ${totalPassed}/${totalTests} tests passed`);
console.log(`${'═'.repeat(40)}`);

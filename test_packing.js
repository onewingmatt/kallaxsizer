/**
 * Test the packing algorithm with fixed calcFit
 */

const KALLAX = { depth: 39, width: 33, height: 33 };
const KALLAX_SIZES = {
  '2x2': { rows: 2, cols: 2, cubes: 4 },
  '2x4': { rows: 2, cols: 4, cubes: 8 },
};

function calcFit(game) {
  const d = game.dims;
  const dims = [d.l, d.w, d.h].sort((a, b) => a - b);
  const [smallest, middle, largest] = dims;
  if (smallest <= KALLAX.width && middle <= KALLAX.height && largest <= KALLAX.depth) {
    return 'yes';
  }
  return 'toobig';
}

function sortDims(arr) {
  const s = [...arr].sort((a, b) => b - a);
  return { l: Math.round(s[0] * 10) / 10, w: Math.round(s[1] * 10) / 10, h: Math.round(s[2] * 10) / 10 };
}

function packGames(gameList, orientation) {
  const augmented = gameList.map(g => {
    const sorted = [g.dims.l, g.dims.w, g.dims.h].sort((a, b) => b - a);
    const fit = calcFit(g);
    const packDim = sorted[2]; // shortest dimension
    return { ...g, fit, packDim, sorted };
  });

  const fitting = augmented.filter(g => g.fit !== 'toobig');
  const tooBig = augmented.filter(g => g.fit === 'toobig');
  const packLimit = orientation === 'doubledeep' ? KALLAX.depth : KALLAX.width;

  fitting.sort((a, b) => b.packDim - a.packDim);

  let currentCube = 0;
  let remaining = packLimit;

  fitting.forEach(g => {
    if (g.packDim > remaining) {
      currentCube++;
      remaining = packLimit;
    }
    g.cubeIndex = currentCube;
    g.cubesUsed = 1;
    remaining -= g.packDim;
  });

  const fittingCubes = fitting.length > 0 ? currentCube + 1 : 0;

  tooBig.forEach((g) => {
    g.cubeIndex = -1;
    g.cubesUsed = 0;
  });

  return { games: [...fitting, ...tooBig], totalCubes: fittingCubes };
}

// Test case: Mixed collection with some oversized games
const testCollection = [
  { id: 1, name: 'Standard Game', dims: { l: 29.5, w: 29.5, h: 7.5 } },
  { id: 2, name: 'Large Game', dims: { l: 37, w: 27, h: 9 } },
  { id: 3, name: 'Card Game', dims: { l: 13, w: 10, h: 4 } },
  { id: 4, name: 'Tiny Game', dims: { l: 10, w: 10, h: 3 } },
  { id: 5, name: 'Oversized (41cm)', dims: { l: 41, w: 29.5, h: 17 } },
  { id: 6, name: 'Oversized (40cm)', dims: { l: 40, w: 24, h: 10 } },
];

console.log('=== Testing Packing Algorithm ===\n');

const { games: packed, totalCubes } = packGames(testCollection, 'vertical');

console.log(`Collection: ${testCollection.length} games`);
console.log(`Fitting: ${packed.filter(g => g.fit === 'yes').length}`);
console.log(`Too Big: ${packed.filter(g => g.fit === 'toobig').length}`);
console.log(`Total cubes needed: ${totalCubes}\n`);

packed.forEach(g => {
  const dims = `${g.dims.l}×${g.dims.w}×${g.dims.h}`;
  if (g.fit === 'yes') {
    console.log(`✅ ${g.name} (${dims}) → Cube #${g.cubeIndex + 1}`);
  } else {
    console.log(`❌ ${g.name} (${dims}) → Too Big`);
  }
});

// Validate results
const expectedFitting = 4; // Standard, Large, Card, Tiny
const expectedTooBig = 2;  // Both oversized
const expectedCubes = 1;   // All 4 fit in 1 cube with vertical packing (9+7.5+4+3 = 23.5cm < 33cm)

const testPassed = 
  packed.filter(g => g.fit === 'yes').length === expectedFitting &&
  packed.filter(g => g.fit === 'toobig').length === expectedTooBig &&
  totalCubes === expectedCubes;

console.log(`\n${testPassed ? '✅ PASS' : '❌ FAIL'}: Packing algorithm working correctly`);

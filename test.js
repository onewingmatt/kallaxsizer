
    /* ═══════════════════════════════════════════════════
       CONSTANTS
       ═══════════════════════════════════════════════════ */
    const KALLAX = { depth: 39, width: 33, height: 33 };
    const KALLAX_SIZES = {
      '2x2': { rows: 2, cols: 2, cubes: 4 },
      '2x4': { rows: 2, cols: 4, cubes: 8 },
      '4x4': { rows: 4, cols: 4, cubes: 16 },
      '5x5': { rows: 5, cols: 5, cubes: 25 },
    };

    const COMMON_SIZES = {
      standard: { l: 29.5, w: 29.5, h: 7.5, label: 'Standard (Catan-size)' },
      bigbox: { l: 29.5, w: 29.5, h: 12, label: 'Big Box' },
      large: { l: 37, w: 27, h: 9, label: 'Large Box' },
      ttr: { l: 36.5, w: 26.7, h: 8, label: 'Ticket to Ride size' },
      medium: { l: 25, w: 25, h: 7, label: 'Medium Box' },
      small: { l: 19.5, w: 19.5, h: 7, label: 'Small Box' },
      card: { l: 13, w: 10, h: 4, label: 'Card Game' },
    };

    /* Well-known BGG IDs → exact dimensions [L, W, H] in cm
       Sourced from publisher specs and community measurements */
    const KNOWN_GAME_DIMS = {
      // --- Huge / Oversize ---
      174430: [41, 29.5, 17],   // Gloomhaven
      233078: [43, 30, 13],     // Twilight Imperium (4th Ed.)
      187645: [40, 30, 12],     // Star Wars: Rebellion
      164928: [31, 31, 12],     // Orléans
      291457: [30, 30, 12],     // Gloomhaven: Jaws of the Lion
      // --- Large / TTR-size ---
      169786: [36.5, 26.7, 9.5], // Scythe
      9209: [36.5, 26.7, 8],   // Ticket to Ride
      14996: [36.5, 26.7, 8],   // Ticket to Ride: Europe
      220308: [35.6, 25.4, 8.5], // Gaia Project
      12333: [36, 25, 6],       // Twilight Struggle
      28720: [36, 25, 7],       // Brass: Lancashire
      // --- Standard square ---
      13: [29.5, 29.5, 7.5], // Catan
      224517: [30, 30, 7.3],     // Brass: Birmingham
      167791: [29.8, 29.8, 7.2], // Terraforming Mars
      162886: [29.8, 29.8, 7.5], // Spirit Island
      266192: [29.5, 24, 7],     // Wingspan
      68448: [29.5, 29.5, 7.5], // 7 Wonders
      342942: [29.6, 29.6, 7.3], // Ark Nova
      316554: [29.5, 29.5, 7],   // Dune: Imperium
      237182: [29.2, 29.2, 7.5], // Root
      312484: [30, 30, 7.5],     // Lost Ruins of Arnak
      193738: [29.5, 29.5, 7.5], // Great Western Trail
      124361: [30, 30, 7.5],     // Concordia
      126163: [29.5, 29.5, 7.5], // Tzolk'in
      36218: [29.5, 29.5, 7.5], // Dominion
      31260: [31, 22, 7.5],     // Agricola
      199792: [26, 26, 8],       // Everdell
      251247: [30, 30, 7],       // Barrage
      182028: [30.5, 30.5, 7.5], // Through the Ages
      230802: [25.7, 25.7, 7.6], // Azul
      285967: [26.8, 19, 5.5],   // Cascadia
      3076: [27, 19, 7],       // Puerto Rico
      215: [29.5, 29.5, 7.5], // Tikal
      // --- Medium ---
      205637: [24, 17, 6],       // Arkham Horror: TCG
      178900: [24, 16, 5],       // Codenames
      173346: [21, 15.5, 5],     // 7 Wonders Duel
      148228: [21, 21, 7.5],     // Splendor
      204583: [21, 21, 5],       // Kingdomino
      // --- Small / Card ---
      24480: [13, 10, 4],       // The Crew
      295947: [13, 10, 4],       // The Crew: Mission Deep Sea
      // --- More popular games ---
      822: [28, 19, 7],       // Carcassonne
      2651: [30, 30, 7.5],     // Power Grid
      120677: [29, 29, 7],       // Terra Mystica
      159675: [30, 30, 7],       // Star Realms → actually small, but box variants
      233867: [30, 30, 7],       // Clank! In! Space!
      147949: [30, 30, 7],       // Star Wars: X-Wing
      216132: [30, 30, 7],       // Clank!
      161936: [30, 24, 7.5],     // Pandemic Legacy S1
      172308: [30, 24, 7.5],     // Village
      192135: [30, 30, 7],       // Too Many Bones
      25613: [30, 30, 7],       // Through the Desert
      39856: [30, 21, 7],       // Dixit
      2653: [30, 30, 7.5],     // Citadels
      128882: [30, 30, 7],       // The Resistance: Avalon
      93: [30, 30, 7],       // El Grande
      110327: [25, 25, 7],       // Lords of Waterdeep
      25021: [30, 30, 7],       // Descent: Journeys
      40834: [30, 30, 7.5],     // Dominion: Intrigue
      463: [30, 21, 7],       // Magic: The Gathering
      12: [23, 23, 6],       // Citadels (old)
      3: [30, 30, 7],       // Cosmic Encounter
      45: [25, 25, 7],       // Tigris & Euphrates
      42: [30, 30, 7.5],     // Ra
      118: [23, 23, 6],       // Modern Art
      120: [30, 30, 7],       // Acquire
      46: [25, 19, 7],       // Battle Line
      50: [23, 23, 6],       // Lost Cities
      521: [26, 18, 4],       // Cockroach Poker
      478: [27, 19, 7],       // Citadels (new)
      47: [25, 19, 7],       // Schotten Totten
      337: [26, 18, 7],       // Bohnanza
      483: [30, 30, 7.5],     // Diplomacy
      903: [30, 30, 7],       // Pandemic
      158600: [30, 24, 7.5],     // Pandemic Legacy S2
      161417: [30, 30, 7],       // Blood Rage
      170216: [29, 29, 7],       // Blood Rage (KS)
      155426: [30, 30, 7],       // Istanbul
      157354: [30, 30, 7.5],     // Five Tribes
      172081: [20, 20, 7],       // Burgle Bros
      40692: [30, 30, 7],       // Small World
      103343: [30, 30, 7],       // Pandemic: In the Lab
      102794: [30, 30, 7],       // Caverna
      182134: [30, 30, 7],       // Inis
      283863: [25, 25, 7],       // Canvas
      39463: [29, 29, 7],       // Castles of Burgundy
      34219: [30, 21, 7],       // Betrayal at House on the Hill
      127023: [25, 25, 6],       // Dead of Winter
      173090: [29, 29, 7],       // Champions of Midgard
      217372: [30, 30, 7],       // Raiders of the North Sea
      192291: [30, 30, 7],       // Paladins of the West Kingdom
      256916: [30, 30, 7],       // Architects of the West Kingdom
      244521: [30, 30, 7],       // The Quacks of Quedlinburg
      198773: [30, 30, 7],       // Clans of Caledonia
      191977: [30, 30, 7.5],     // Viticulture Essential Edition
      263918: [30, 30, 7],       // Teotihuacan
      300905: [30, 30, 7],       // Praga Caput Regni
      329122: [25, 25, 7],       // Meadow
      297530: [30, 30, 7],       // Great Western Trail 2nd Ed.
      366013: [30, 30, 7.5],     // Arcs
      302260: [30, 30, 7],       // Undaunted: Normandy
      302723: [30, 30, 7],       // Undaunted: North Africa
      267814: [30, 30, 7],       // Paladins
      175199: [25, 25, 7],       // Imperial Settlers
      181304: [25, 25, 7],       // Mysterium
      194879: [25, 25, 7],       // Seasons
      195314: [25, 25, 7],       // Skull
      195421: [30, 30, 7],       // Mombasa
      163412: [30, 30, 7.5],     // Patchwork
      218161: [30, 30, 7],       // Tekhenu
      228341: [30, 30, 7.5],     // Aeon's End
      260627: [30, 30, 7],       // Sagrada
      248861: [30, 30, 7],       // Kingsburg (2nd Ed.)
      206718: [30, 30, 7],       // Unfathomable
      244995: [20, 15, 5],       // Cockroach Poker Royal
      280812: [20, 20, 7],       // Cartographers
      194655: [30, 30, 7],       // Star Wars: Outer Rim
      159143: [30, 30, 7],       // Suburbia
      156097: [30, 30, 7],       // War of the Ring (2nd Ed.)
      156009: [30, 30, 7.5],     // Werewords
      131357: [25, 25, 7],       // Forbidden Desert
      283155: [25, 25, 7],       // Forbidden Sky
    };

    /* ═══════════════════════════════════════════════════
       STATE
       ═══════════════════════════════════════════════════ */
    let games = [];
    let sortCol = 'name';
    let sortAsc = true;

    /* ═══════════════════════════════════════════════════
       DOM REFERENCES
       ═══════════════════════════════════════════════════ */
    const $ = (id) => document.getElementById(id);
    const loginForm = $('loginForm');
    const fetchBtn = $('fetchBtn');
    const resumeBtn = $('resumeBtn');
    const demoBtn = $('demoBtn');
    const errorMsg = $('errorMsg');
    const progressArea = $('progressArea');
    const progressFill = $('progressFill');
    const progressStatus = $('progressStatus');
    const resultsArea = $('resultsArea');
    const kallaxSizeSelect = $('kallaxSize');
    const orientationSelect = $('orientation');
    const cacheStatusEl = $('cacheStatus');

    /* ═══════════════════════════════════════════════════
       LOCALSTORAGE CACHE
       ═══════════════════════════════════════════════════ */
    const CACHE_KEY = 'kallax_cache';

    function saveCache(username, gameList) {
      const data = {
        username, ts: Date.now(), games: gameList.map(g => ({
          id: g.id, name: g.name, dims: g.dims, source: g.source,
        }))
      };
      try { localStorage.setItem(CACHE_KEY, JSON.stringify(data)); } catch (e) { console.warn('Cache save failed:', e); }
    }

    function loadCache() {
      try {
        const raw = localStorage.getItem(CACHE_KEY);
        return raw ? JSON.parse(raw) : null;
      } catch (e) { return null; }
    }

    function clearCache() {
      localStorage.removeItem(CACHE_KEY);
      updateCacheStatus();
    }

    function updateCacheStatus() {
      const cache = loadCache();
      if (cache && cache.games && cache.games.length > 0) {
        const total = cache.games.length;
        const withBgg = cache.games.filter(g => g.source === 'bgg').length;
        const withKnown = cache.games.filter(g => g.source === 'known').length;
        const withFallback = total - withBgg - withKnown;
        const age = Math.round((Date.now() - cache.ts) / 60000);
        const ageStr = age < 60 ? `${age}m ago` : `${Math.round(age / 60)}h ago`;
        cacheStatusEl.innerHTML = `📦 Cached: <strong>${total} games</strong> for <strong>${cache.username}</strong> (${ageStr}) — ${withBgg} BGG, ${withKnown} known, ${withFallback} fallback. <a href="#" id="clearCacheLink" style="color:var(--accent)">Clear cache</a>`;
        cacheStatusEl.style.display = 'block';
        resumeBtn.style.display = 'inline-flex';
        setTimeout(() => {
          const link = $('clearCacheLink');
          if (link) link.addEventListener('click', (e) => { e.preventDefault(); clearCache(); });
        });
      } else {
        cacheStatusEl.style.display = 'none';
        resumeBtn.style.display = 'none';
      }
    }

    updateCacheStatus();

    /* ═══════════════════════════════════════════════════
       PROGRESS HELPERS
       ═══════════════════════════════════════════════════ */
    function showProgress(pct, msg) {
      progressArea.classList.add('visible');
      progressFill.style.width = pct + '%';
      progressStatus.textContent = msg;
    }
    function hideProgress() {
      progressArea.classList.remove('visible');
    }
    function showError(msg) {
      errorMsg.textContent = msg;
      errorMsg.classList.remove('hidden');
    }
    function hideError() {
      errorMsg.classList.add('hidden');
    }

    /* ═══════════════════════════════════════════════════
       NETWORKING — LOCAL PROXY OR CORS PROXY FALLBACK
       ═══════════════════════════════════════════════════ */
    const USE_LOCAL_PROXY = location.hostname === 'localhost' || location.hostname === '127.0.0.1';
    const BGG_BASE = 'https://boardgamegeek.com';

    // External CORS proxies (fallback when not using server.py)
    const CORS_PROXIES = [
      (url) => `https://corsproxy.io/?${encodeURIComponent(url)}`,
      (url) => `https://api.allorigins.win/raw?url=${encodeURIComponent(url)}`,
    ];
    let activeProxyIndex = 0;

    function bggUrl(path) {
      // When local proxy is available, route through /bggproxy/
      if (USE_LOCAL_PROXY) return `/bggproxy/${path}`;
      return `${BGG_BASE}/${path}`;
    }

    async function bggFetch(path, options = {}) {
      if (USE_LOCAL_PROXY) {
        // Local proxy handles everything — simple fetch
        return fetch(`/bggproxy/${path}`, options);
      }
      // Otherwise try external CORS proxies
      const fullUrl = `${BGG_BASE}/${path}`;
      for (let i = 0; i < CORS_PROXIES.length; i++) {
        const idx = (activeProxyIndex + i) % CORS_PROXIES.length;
        const proxiedUrl = CORS_PROXIES[idx](fullUrl);
        try {
          const resp = await fetch(proxiedUrl, { mode: 'cors' });
          if (resp.ok) {
            activeProxyIndex = idx;
            return resp;
          }
          console.warn(`Proxy ${idx} returned HTTP ${resp.status}`);
        } catch (e) {
          console.warn(`Proxy ${idx} failed:`, e.message);
        }
      }
      // Last resort: direct fetch
      return fetch(fullUrl);
    }

    /* ═══════════════════════════════════════════════════
       BGG API
       ═══════════════════════════════════════════════════ */
    async function bggLogin(username, password) {
      if (!password) return false;
      try {
        const resp = await bggFetch('login/api/v1', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ credentials: { username, password } }),
        });
        return resp.ok;
      } catch (e) {
        console.warn('Login failed, continuing unauthenticated:', e);
        return false;
      }
    }

    async function fetchCollection(username) {
      // BGG's XML API now requires Bearer authentication (recently changed)
      // Without API credentials, automatic fetching is not possible
      // Users must use the CSV export method instead
      throw new Error(
        `BGG's API now requires authentication tokens that aren't publicly available.\n\n` +
        `Instead, please use the CSV export method:\n` +
        `1. Go to https://boardgamegeek.com/collection/user/${encodeURIComponent(username)}\n` +
        `2. Click ⋯ (More) → "Download as CSV"\n` +
        `3. In this app, click 📁 CSV Upload\n` +
        `4. Select your downloaded file\n\n` +
        `This gives you accurate game data in seconds.`
      );
    }

    function parseCollectionXml(xml) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xml, 'text/xml');
      const items = doc.querySelectorAll('item');
      const result = [];
      items.forEach((item) => {
        const id = parseInt(item.getAttribute('objectid'), 10);
        const name = item.querySelector('name')?.textContent || 'Unknown';
        result.push({ id, name, dims: null, source: null });
      });
      return result;
    }

    async function fetchDimensions(gameList) {
      const ids = gameList.map((g) => g.id);
      const batchSize = 20;
      const total = Math.ceil(ids.length / batchSize);
      for (let i = 0; i < ids.length; i += batchSize) {
        const batchNum = Math.floor(i / batchSize) + 1;
        showProgress(50 + (batchNum / total) * 40, `Fetching dimensions batch ${batchNum}/${total}…`);
        const batch = ids.slice(i, i + batchSize);
        const path = `xmlapi2/thing?id=${batch.join(',')}&versions=1`;
        try {
          const resp = await bggFetch(path);
          if (resp.ok) {
            const text = await resp.text();
            parseDimensionsXml(text, gameList);
          }
        } catch (e) {
          console.warn('Dimension fetch error, skipping batch:', e);
        }
        if (i + batchSize < ids.length) await delay(2000);
      }
    }

    function parseDimensionsXml(xml, gameList) {
      const parser = new DOMParser();
      const doc = parser.parseFromString(xml, 'text/xml');
      // Top-level items are the games
      const topItems = doc.querySelectorAll('items > item');
      topItems.forEach(item => {
        const id = parseInt(item.getAttribute('id'), 10);
        const game = gameList.find(g => g.id === id);
        if (!game || game.dims) return; // already has dims
        // BGG structure: <versions><item type="boardgameversion">...<width value="X"/>...</item></versions>
        const versionItems = item.querySelectorAll('versions > item');
        for (const ver of versionItems) {
          const wEl = ver.querySelector('width');
          const lEl = ver.querySelector('length');
          const dEl = ver.querySelector('depth');
          const w = wEl ? parseFloat(wEl.getAttribute('value')) : 0;
          const l = lEl ? parseFloat(lEl.getAttribute('value')) : 0;
          const d = dEl ? parseFloat(dEl.getAttribute('value')) : 0;
          if (w > 0 && l > 0 && d > 0) {
            game.dims = sortDims([w * 2.54, l * 2.54, d * 2.54]);
            game.source = 'bgg';
            break;
          }
        }
      });
    }

    /* ═══════════════════════════════════════════════════
       DIMENSION RESOLUTION
       ═══════════════════════════════════════════════════ */
    function sortDims(arr) {
      const s = [...arr].sort((a, b) => b - a);
      return { l: round(s[0]), w: round(s[1]), h: round(s[2]) };
    }

    function round(v) { return Math.round(v * 10) / 10; }

    function resolveDimensions(gameList) {
      const customDims = JSON.parse(localStorage.getItem('bgsize_customDims') || '{}');
      gameList.forEach(g => {
        if (customDims[g.id]) {
          g.dims = sortDims([customDims[g.id].l, customDims[g.id].w, customDims[g.id].h]);
          g.source = 'custom';
          return;
        }
        if (g.dims && g.source) return; // already resolved from BGG version data
        if (KNOWN_GAME_DIMS[g.id]) {
          const [l, w, h] = KNOWN_GAME_DIMS[g.id];
          g.dims = sortDims([l, w, h]);
          g.source = 'known';
        } else {
          const size = COMMON_SIZES.standard;
          g.dims = { l: size.l, w: size.w, h: size.h };
          g.source = 'common';
        }
      });
    }

    /* ═══════════════════════════════════════════════════
       KALLAX PACKING
       ═══════════════════════════════════════════════════ */
    function calcFit(game, orientation) {
      const d = game.dims;
      const sorted = [d.l, d.w, d.h].sort((a, b) => b - a);
      const longest = sorted[0], mid = sorted[1], shortest = sorted[2];

      if (orientation === 'vertical') {
        // longest → depth(39), mid → height(33), shortest → spine width
        if (longest <= KALLAX.depth && mid <= KALLAX.height) {
          if (longest > KALLAX.depth * 0.9 || mid > KALLAX.height * 0.9) return 'tight';
          return 'yes';
        }
      } else if (orientation === 'horizontal') {
        // longest → depth(39), mid → width(33), stack by shortest
        if (longest <= KALLAX.depth && mid <= KALLAX.width) {
          if (longest > KALLAX.depth * 0.9 || mid > KALLAX.width * 0.9) return 'tight';
          return 'yes';
        }
      } else if (orientation === 'bestfit' || orientation === 'doubledeep') {
        // Try both orientations — if either works, it fits
        const fitsV = longest <= KALLAX.depth && mid <= KALLAX.height;
        const fitsH = longest <= KALLAX.depth && mid <= KALLAX.width;
        if (fitsV || fitsH) {
          const tight = fitsV
            ? (longest > KALLAX.depth * 0.9 || mid > KALLAX.height * 0.9)
            : (longest > KALLAX.depth * 0.9 || mid > KALLAX.width * 0.9);
          return tight ? 'tight' : 'yes';
        }
      }
      return 'toobig';
    }

    function packGames(gameList, orientation) {
      const augmented = gameList.map(g => {
        const sorted = [g.dims.l, g.dims.w, g.dims.h].sort((a, b) => b - a);
        const fit = calcFit(g, orientation);
        const packDim = sorted[2]; // shortest dimension = spine width or stack height
        return { ...g, fit, packDim, sorted };
      });

      const fitting = augmented.filter(g => g.fit !== 'toobig');
      const tooBig = augmented.filter(g => g.fit === 'toobig');

      // For doubledeep mode, we can use the full 39cm depth for packing
      // (two rows of games front-to-back in the same cube)
      const packLimit = orientation === 'doubledeep' ? KALLAX.depth : KALLAX.width;

      // Sort fitting games by packDim descending for first-fit-decreasing
      fitting.sort((a, b) => b.packDim - a.packDim);

      if (orientation === 'doubledeep') {
        // 2D bin packing: each cube has width=33cm and depth=39cm
        // Games occupy (packDim) width and (mid dimension) depth
        const cubes = []; // Each cube tracks remaining columns
        fitting.forEach(g => {
          const gameWidth = g.packDim;
          const gameDepth = g.sorted[1]; // mid dimension
          let placed = false;
          for (let c = 0; c < cubes.length; c++) {
            // Try to fit in an existing column (front or back)
            for (let col = 0; col < cubes[c].columns.length; col++) {
              if (cubes[c].columns[col].depthLeft >= gameDepth && gameWidth <= cubes[c].columns[col].width) {
                cubes[c].columns[col].depthLeft -= gameDepth;
                g.cubeIndex = c;
                g.cubesUsed = 1;
                placed = true;
                break;
              }
            }
            if (placed) break;
            // Try to start a new column in this cube
            if (cubes[c].widthLeft >= gameWidth) {
              cubes[c].columns.push({ width: gameWidth, depthLeft: KALLAX.depth - gameDepth });
              cubes[c].widthLeft -= gameWidth;
              g.cubeIndex = c;
              g.cubesUsed = 1;
              placed = true;
              break;
            }
          }
          if (!placed) {
            // New cube
            cubes.push({ widthLeft: KALLAX.width - gameWidth, columns: [{ width: gameWidth, depthLeft: KALLAX.depth - gameDepth }] });
            g.cubeIndex = cubes.length - 1;
            g.cubesUsed = 1;
          }
        });

        const fittingCubes = cubes.length;
        tooBig.forEach((g, i) => {
          g.cubeIndex = fittingCubes + i * 2;
          g.cubesUsed = 2;
        });
        const totalCubes = fittingCubes + tooBig.length * 2;
        return { games: [...fitting, ...tooBig], totalCubes };
      }

      // Standard bin packing (vertical, horizontal, bestfit)
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

      tooBig.forEach((g, i) => {
        g.cubeIndex = fittingCubes + i * 2;
        g.cubesUsed = 2;
      });

      const totalCubes = fittingCubes + tooBig.length * 2;
      return { games: [...fitting, ...tooBig], totalCubes };
    }

    /* ═══════════════════════════════════════════════════
       RENDERING
       ═══════════════════════════════════════════════════ */
    // Store packed data globally for cube click handlers
    let lastPacked = [];

    function render() {
      const orientation = orientationSelect.value;
      const kallaxKey = kallaxSizeSelect.value;
      const kallax = KALLAX_SIZES[kallaxKey];

      const { games: packed, totalCubes } = packGames(games, orientation);
      lastPacked = packed;
      const unitsNeeded = Math.ceil(totalCubes / kallax.cubes);
      const totalSlots = unitsNeeded * kallax.cubes;
      const spareCubes = totalSlots - totalCubes;

      // Stats
      $('statGames').textContent = games.length;
      $('statCubes').textContent = totalCubes;
      $('statUnits').textContent = unitsNeeded;
      $('statSpare').textContent = spareCubes;
      $('gamesCount').textContent = games.length;

      // Kallax visual — clickable cubes
      renderKallaxVisual(unitsNeeded, kallax, totalCubes, packed);

      // Cube breakdown (collapsed by default)
      renderCubeBreakdown(packed, totalCubes, orientation);

      // Table
      renderTable(packed, orientation);

      resultsArea.classList.add('visible');
    }

    function renderKallaxVisual(units, kallax, filledCount, packed) {
      const container = $('kallaxVisual');
      container.innerHTML = '';

      // Build cube→games map
      const cubeMap = {};
      packed.forEach(g => {
        const ci = g.cubeIndex;
        if (!cubeMap[ci]) cubeMap[ci] = [];
        cubeMap[ci].push(g);
        if (g.cubesUsed === 2 && !cubeMap[ci + 1]) cubeMap[ci + 1] = [g];
      });

      let cubeIdx = 0;
      for (let u = 0; u < units; u++) {
        const unitDiv = document.createElement('div');
        unitDiv.className = 'kallax-unit';

        const label = document.createElement('div');
        label.className = 'kallax-label';
        label.textContent = `Unit ${u + 1}`;
        unitDiv.appendChild(label);

        const grid = document.createElement('div');
        grid.className = 'kallax-grid';
        grid.style.gridTemplateColumns = `repeat(${kallax.cols}, 36px)`;

        for (let c = 0; c < kallax.cubes; c++) {
          const ci = cubeIdx;
          const isFilled = ci < filledCount;
          const cube = document.createElement('div');
          const gamesInCube = cubeMap[ci] || [];
          cube.className = 'kallax-cube ' + (isFilled ? 'filled' : 'empty');
          if (isFilled && gamesInCube.length > 0) {
            cube.style.cursor = 'pointer';
            cube.title = gamesInCube.map(g => g.name).join(', ');
            // Show game count badge
            const count = document.createElement('span');
            count.style.cssText = 'font-size:10px;color:#fff;font-weight:700;position:absolute;top:50%;left:50%;transform:translate(-50%,-50%)';
            count.textContent = gamesInCube.length;
            cube.appendChild(count);
            cube.addEventListener('click', () => {
              showCubeDetail(ci, gamesInCube);
            });
          }
          cubeIdx++;
          grid.appendChild(cube);
        }

        unitDiv.appendChild(grid);
        container.appendChild(unitDiv);
      }
    }

    function showCubeDetail(cubeIndex, gamesInCube) {
      const bd = $('cubeBreakdown');
      const usedSpace = gamesInCube.reduce((sum, g) => sum + Math.min(g.dims.l, g.dims.w, g.dims.h), 0);
      const remaining = KALLAX.width - usedSpace;
      bd.innerHTML = `
        <div style="background:var(--card-bg);border:2px solid var(--accent);border-radius:8px;padding:1rem;animation:fadeIn 0.2s">
          <h3 style="margin:0 0 0.5rem">📦 Cube #${cubeIndex + 1}</h3>
          <p style="font-size:0.85rem;color:var(--text-secondary);margin:0 0 0.75rem">
            ${gamesInCube.length} game${gamesInCube.length !== 1 ? 's' : ''} — 
            ${usedSpace.toFixed(1)}cm used / ${remaining.toFixed(1)}cm remaining of ${KALLAX.width}cm width
          </p>
          <table style="width:100%;font-size:0.85rem;border-collapse:collapse">
            <thead><tr style="border-bottom:1px solid var(--border)">
              <th style="text-align:left;padding:0.3rem 0.5rem">Game</th>
              <th style="text-align:left;padding:0.3rem 0.5rem">Dimensions</th>
              <th style="text-align:left;padding:0.3rem 0.5rem">Pack Width</th>
            </tr></thead>
            <tbody>
              ${gamesInCube.map(g => {
        const pw = Math.min(g.dims.l, g.dims.w, g.dims.h);
        return `<tr class="game-row" onclick="openEditModal(${g.id}, '${escHtml(g.name).replace(/'/g, "\\'")}', ${g.dims.l}, ${g.dims.w}, ${g.dims.h})" title="Click to edit dimensions" style="border-bottom:1px solid var(--border)">
                  <td style="padding:0.3rem 0.5rem">${escHtml(g.name)}</td>
                  <td style="padding:0.3rem 0.5rem">${g.dims.l} × ${g.dims.w} × ${g.dims.h}</td>
                  <td style="padding:0.3rem 0.5rem">${pw}cm</td>
                </tr>`;
      }).join('')}
            </tbody>
          </table>
        </div>
      `;
      bd.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }

    function renderCubeBreakdown(packed, totalCubes, orientation) {
      // Clear any previous detail
      $('cubeBreakdown').innerHTML = '';
    }

    function sourceBadge(src) {
      if (src === 'custom') return '<span class="badge badge-custom">✏️ Custom Size</span>';
      if (src === 'bgg') return '<span class="badge badge-bgg">BGG Version</span>';
      if (src === 'known') return '<span class="badge badge-known">Known Size</span>';
      return '<span class="badge badge-common">Common Size</span>';
    }

    function fitBadge(fit) {
      if (fit === 'yes') return '<span class="badge badge-fit-yes">✓ Fits</span>';
      if (fit === 'tight') return '<span class="badge badge-fit-tight">⚠ Tight Fit</span>';
      return '<span class="badge badge-fit-no">✗ Too Big</span>';
    }

    function renderTable(packed, orientation) {
      const searchStr = $('searchFilter').value.toLowerCase();
      const fitVal = $('fitFilter').value;

      let displayGames = packed.filter(g => {
        if (searchStr && !g.name.toLowerCase().includes(searchStr)) return false;
        if (fitVal !== 'all' && g.fit !== fitVal) return false;
        return true;
      });

      $('gamesCount').textContent = displayGames.length;

      // Apply current sort
      displayGames.sort((a, b) => {
        let va, vb;
        switch (sortCol) {
          case 'name': va = a.name.toLowerCase(); vb = b.name.toLowerCase(); break;
          case 'dims': va = a.dims.l * a.dims.w * a.dims.h; vb = b.dims.l * b.dims.w * b.dims.h; break;
          case 'source': va = a.source; vb = b.source; break;
          case 'fit': va = a.fit; vb = b.fit; break;
          case 'cubes': va = a.cubeIndex; vb = b.cubeIndex; break;
          default: va = a.name.toLowerCase(); vb = b.name.toLowerCase();
        }
        if (va < vb) return sortAsc ? -1 : 1;
        if (va > vb) return sortAsc ? 1 : -1;
        return 0;
      });

      const tbody = $('gamesBody');
      tbody.innerHTML = displayGames.map(g => `
    <tr class="game-row" onclick="openEditModal(${g.id}, '${escHtml(g.name).replace(/'/g, "\\'")}', ${g.dims.l}, ${g.dims.w}, ${g.dims.h})" title="Click to edit dimensions" style="border-bottom:1px solid var(--border)">
      <td>${escHtml(g.name)}</td>
      <td>${g.dims.l} × ${g.dims.w} × ${g.dims.h}</td>
      <td>${sourceBadge(g.source)}</td>
      <td>${fitBadge(g.fit)}</td>
      <td>${g.cubesUsed === 2 ? `${g.cubeIndex + 1}–${g.cubeIndex + 2}` : g.cubeIndex + 1}</td>
    </tr>
  `).join('');

      // Update sort arrows
      document.querySelectorAll('#gamesTable thead th').forEach(th => {
        const arrow = th.querySelector('.sort-arrow');
        if (th.dataset.sort === sortCol) {
          arrow.textContent = sortAsc ? '▲' : '▼';
        } else {
          arrow.textContent = '';
        }
      });
    }

    function escHtml(s) {
      const d = document.createElement('div');
      d.textContent = s;
      return d.innerHTML;
    }

    function parseCsvLine(text) {
      const result = [];
      let inQuote = false;
      let current = '';
      for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (char === '"' && text[i + 1] === '"') {
          current += '"';
          i++; // skip escaped quote
        } else if (char === '"') {
          inQuote = !inQuote;
        } else if (char === ',' && !inQuote) {
          result.push(current);
          current = '';
        } else {
          current += char;
        }
      }
      result.push(current);
      return result.map(s => s.trim());
    }

    /* ═══════════════════════════════════════════════════
       SORTING
       ═══════════════════════════════════════════════════ */
    document.querySelectorAll('#gamesTable thead th').forEach(th => {
      th.addEventListener('click', () => {
        const col = th.dataset.sort;
        if (!col) return;
        if (sortCol === col) { sortAsc = !sortAsc; }
        else { sortCol = col; sortAsc = true; }
        render();
      });
    });

    /* ═══════════════════════════════════════════════════
       CONFIG CHANGE
       ═══════════════════════════════════════════════════ */
    kallaxSizeSelect.addEventListener('change', () => { if (games.length) render(); });
    orientationSelect.addEventListener('change', () => { if (games.length) render(); });

    /* ═══════════════════════════════════════════════════
       FORM SUBMIT
       ═══════════════════════════════════════════════════ */
    async function doFetch(username, password) {
      fetchBtn.disabled = true;
      demoBtn.disabled = true;
      resumeBtn.disabled = true;
      try {
        if (password) {
          showProgress(5, 'Logging in…');
          const ok = await bggLogin(username, password);
          if (!ok) showProgress(8, 'Login failed — continuing unauthenticated…');
        }

        showProgress(10, 'Fetching collection…');
        games = await fetchCollection(username);
        if (games.length === 0) { showError('No owned games found for that username.'); hideProgress(); return; }

        // Save collection immediately so we don't lose it
        saveCache(username, games);
        updateCacheStatus();

        showProgress(50, `Found ${games.length} games. Fetching dimensions…`);
        await fetchDimensions(games);

        resolveDimensions(games);

        // Save again with dimensions resolved
        saveCache(username, games);
        updateCacheStatus();

        showProgress(100, 'Done!');
        setTimeout(hideProgress, 800);
        render();
      } catch (err) {
        // Even on error, save what we have so far
        if (games.length) {
          resolveDimensions(games);
          saveCache(username, games);
          updateCacheStatus();
          render();
          showError('Partial sync — ' + err.message + '. Click Resume Sync to retry later.');
        } else {
          showError('Error: ' + err.message);
        }
        hideProgress();
      } finally {
        fetchBtn.disabled = false;
        demoBtn.disabled = false;
        resumeBtn.disabled = false;
      }
    }

    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      hideError();
      const username = $('bggUser').value.trim();
      const password = $('bggPass').value;
      if (!username) { showError('Please enter a BGG username.'); return; }
      await doFetch(username, password);
    });

    resumeBtn.addEventListener('click', async () => {
      hideError();
      const cache = loadCache();
      if (!cache) { showError('No cached data found.'); return; }

      // Restore cached games
      games = cache.games.map(g => ({ ...g, dims: g.dims ? { ...g.dims } : null }));
      $('bggUser').value = cache.username;

      // Count games missing BGG dimensions
      const needDims = games.filter(g => g.source !== 'bgg').length;
      if (needDims === 0) {
        resolveDimensions(games);
        render();
        return;
      }

      fetchBtn.disabled = true;
      demoBtn.disabled = true;
      resumeBtn.disabled = true;
      try {
        showProgress(50, `Resuming: ${needDims} games need dimensions…`);
        // Clear non-BGG dims so they can be re-fetched
        games.forEach(g => { if (g.source !== 'bgg') { g.dims = null; g.source = null; } });
        await fetchDimensions(games);
        resolveDimensions(games);
        saveCache(cache.username, games);
        updateCacheStatus();
        showProgress(100, 'Done!');
        setTimeout(hideProgress, 800);
        render();
      } catch (err) {
        resolveDimensions(games);
        saveCache(cache.username, games);
        updateCacheStatus();
        render();
        showError('Partial sync — ' + err.message + '. Try Resume Sync again later.');
        hideProgress();
      } finally {
        fetchBtn.disabled = false;
        demoBtn.disabled = false;
        resumeBtn.disabled = false;
      }
    });

    // Auto-load cached data on page load
    {
      const cache = loadCache();
      if (cache && cache.games && cache.games.length > 0) {
        games = cache.games.map(g => ({ ...g, dims: g.dims ? { ...g.dims } : null }));
        resolveDimensions(games);
        render();
        $('bggUser').value = cache.username || '';
      }
    }

    /* ═══════════════════════════════════════════════════
       DEMO MODE
       ═══════════════════════════════════════════════════ */
    const DEMO_GAMES = [
      { id: 174430, name: 'Gloomhaven', dims: { l: 41.0, w: 29.5, h: 17.0 }, source: 'bgg' },
      { id: 167791, name: 'Terraforming Mars', dims: { l: 29.8, w: 29.8, h: 7.2 }, source: 'bgg' },
      { id: 169786, name: 'Scythe', dims: { l: 36.5, w: 26.7, h: 9.5 }, source: 'bgg' },
      { id: 266192, name: 'Wingspan', dims: { l: 29.5, w: 24.0, h: 7.0 }, source: 'bgg' },
      { id: 224517, name: 'Brass: Birmingham', dims: { l: 30.0, w: 30.0, h: 7.3 }, source: 'bgg' },
      { id: 162886, name: 'Spirit Island', dims: { l: 29.8, w: 29.8, h: 7.5 }, source: 'bgg' },
      { id: 9209, name: 'Ticket to Ride', dims: { l: 36.5, w: 26.7, h: 8.0 }, source: 'known' },
      { id: 13, name: 'Catan', dims: { l: 29.5, w: 29.5, h: 7.5 }, source: 'known' },
      { id: 68448, name: '7 Wonders', dims: { l: 29.5, w: 29.5, h: 7.5 }, source: 'known' },
      { id: 230802, name: 'Azul', dims: { l: 25.7, w: 25.7, h: 7.6 }, source: 'bgg' },
      { id: 312484, name: 'Lost Ruins of Arnak', dims: { l: 30.0, w: 30.0, h: 7.5 }, source: 'bgg' },
      { id: 342942, name: 'Ark Nova', dims: { l: 29.6, w: 29.6, h: 7.3 }, source: 'bgg' },
      { id: 316554, name: 'Dune: Imperium', dims: { l: 29.5, w: 29.5, h: 7.0 }, source: 'bgg' },
      { id: 237182, name: 'Root', dims: { l: 29.2, w: 29.2, h: 7.5 }, source: 'bgg' },
      { id: 193738, name: 'Great Western Trail', dims: { l: 29.5, w: 29.5, h: 7.5 }, source: 'bgg' },
      { id: 199792, name: 'Everdell', dims: { l: 26.0, w: 26.0, h: 8.0 }, source: 'bgg' },
      { id: 291457, name: 'Gloomhaven: Jaws of the Lion', dims: { l: 29.8, w: 29.8, h: 12.0 }, source: 'bgg' },
      { id: 36218, name: 'Dominion', dims: { l: 29.5, w: 29.5, h: 7.5 }, source: 'known' },
      { id: 148228, name: 'Splendor', dims: { l: 21.0, w: 21.0, h: 7.5 }, source: 'bgg' },
      { id: 178900, name: 'Codenames', dims: { l: 24.0, w: 16.0, h: 5.0 }, source: 'bgg' },
      { id: 173346, name: '7 Wonders Duel', dims: { l: 21.0, w: 15.5, h: 5.0 }, source: 'bgg' },
      { id: 124361, name: 'Concordia', dims: { l: 30.0, w: 30.0, h: 7.5 }, source: 'bgg' },
      { id: 126163, name: "Tzolk'in", dims: { l: 29.5, w: 29.5, h: 7.5 }, source: 'bgg' },
      { id: 24480, name: 'The Crew', dims: { l: 13.0, w: 10.0, h: 4.0 }, source: 'known' },
      { id: 14996, name: 'Ticket to Ride: Europe', dims: { l: 36.5, w: 26.7, h: 8.0 }, source: 'known' },
      { id: 233078, name: 'Twilight Imperium (4th Ed.)', dims: { l: 43.0, w: 30.0, h: 13.0 }, source: 'bgg' },
      { id: 220308, name: 'Gaia Project', dims: { l: 35.6, w: 25.4, h: 8.5 }, source: 'bgg' },
      { id: 285967, name: 'Cascadia', dims: { l: 26.8, w: 19.0, h: 5.5 }, source: 'bgg' },
      { id: 205637, name: 'Arkham Horror: TCG', dims: { l: 24.0, w: 17.0, h: 6.0 }, source: 'bgg' },
      { id: 31260, name: 'Agricola', dims: { l: 31.0, w: 22.0, h: 7.5 }, source: 'bgg' },
      // Small & card games (to test Double Deep packing)
      { id: 277085, name: 'Love Letter', dims: { l: 10.0, w: 7.0, h: 3.0 }, source: 'bgg' },
      { id: 133473, name: 'Sushi Go!', dims: { l: 12.0, w: 9.0, h: 3.5 }, source: 'bgg' },
      { id: 98778, name: 'Hanabi', dims: { l: 12.0, w: 9.5, h: 3.0 }, source: 'bgg' },
      { id: 244992, name: 'The Mind', dims: { l: 12.0, w: 9.0, h: 2.5 }, source: 'bgg' },
      { id: 131357, name: 'Coup', dims: { l: 14.0, w: 10.0, h: 3.5 }, source: 'bgg' },
      { id: 54043, name: 'Jaipur', dims: { l: 20.0, w: 13.5, h: 5.0 }, source: 'bgg' },
      { id: 147020, name: 'Star Realms', dims: { l: 10.0, w: 7.0, h: 5.0 }, source: 'bgg' },
      { id: 154597, name: 'Hive Pocket', dims: { l: 16.0, w: 10.5, h: 4.0 }, source: 'bgg' },
      { id: 221965, name: 'The Fox in the Forest', dims: { l: 14.0, w: 10.0, h: 3.5 }, source: 'bgg' },
      { id: 204583, name: 'Kingdomino', dims: { l: 21.0, w: 21.0, h: 5.0 }, source: 'bgg' },
    ];

    demoBtn.addEventListener('click', () => {
      hideError();
      games = DEMO_GAMES.map(g => ({ ...g, dims: { ...g.dims } }));
      render();
    });

    $('csvUpload').addEventListener('change', async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      hideError();
      showProgress(10, 'Parsing CSV…');

      try {
        const text = await file.text();
        const lines = text.split('\\n');
        if (lines.length < 2) throw new Error("CSV file appears empty or invalid.");

        const headers = parseCsvLine(lines[0]).map(h => h.toLowerCase());
        const nameIdx = headers.indexOf('objectname');
        const idIdx = headers.indexOf('objectid');
        const subTypeIdx = headers.indexOf('subtype');

        if (nameIdx === -1 || idIdx === -1) {
          throw new Error("Invalid BGG CSV. Missing 'objectname' or 'objectid' column.");
        }

        games = [];
        for (let i = 1; i < lines.length; i++) {
          const line = lines[i].trim();
          if (!line) continue;
          const cols = parseCsvLine(line);
          const name = cols[nameIdx];
          const id = parseInt(cols[idIdx], 10);
          const subtype = subTypeIdx !== -1 ? cols[subTypeIdx] : 'boardgame';

          if (id && name && subtype === 'boardgame') {
            games.push({ id, name, dims: null, source: null, thumbnail: '' });
          }
        }

        if (games.length === 0) throw new Error("No valid board games found in CSV.");

        // Pretend this is a fetched collection now
        const fakeUsername = "CSV_Import";
        $('bggUser').value = fakeUsername;
        saveCache(fakeUsername, games);
        updateCacheStatus();

        showProgress(50, `Found ${games.length} games. Fetching dimensions from BGG…`);
        fetchBtn.disabled = true;
        demoBtn.disabled = true;
        resumeBtn.disabled = true;

        await fetchDimensions(games);
        resolveDimensions(games);
        saveCache(fakeUsername, games);
        updateCacheStatus();
        showProgress(100, 'Done!');
        setTimeout(hideProgress, 800);
        render();

      } catch (err) {
        if (games && games.length) {
          resolveDimensions(games);
          saveCache("CSV_Import", games);
          updateCacheStatus();
          render();
          showError('Partial sync — ' + err.message + '. Try Resume Sync later.');
        } else {
          showError('CSV Error: ' + err.message);
        }
        hideProgress();
      } finally {
        e.target.value = ''; // Reset file input
        fetchBtn.disabled = false;
        demoBtn.disabled = false;
        resumeBtn.disabled = false;
      }
    });

    /* ═══════════════════════════════════════════════════
       CUSTOM OVERRIDES
       ═══════════════════════════════════════════════════ */
    function openEditModal(id, name, l, w, h) {
      $('editGameId').value = id;
      $('editModalTitle').textContent = `Edit: ${name}`;
      $('editL').value = l;
      $('editW').value = w;
      $('editH').value = h;
      $('editModal').classList.add('open');
    }

    function closeEditModal() {
      $('editModal').classList.remove('open');
    }

    function saveEditModal() {
      const id = parseInt($('editGameId').value, 10);
      const customDims = JSON.parse(localStorage.getItem('bgsize_customDims') || '{}');
      customDims[id] = {
        l: parseFloat($('editL').value) || 0,
        w: parseFloat($('editW').value) || 0,
        h: parseFloat($('editH').value) || 0
      };
      localStorage.setItem('bgsize_customDims', JSON.stringify(customDims));

      // Re-resolve existing games and re-render
      const game = games.find(g => g.id === id);
      if (game) {
        game.dims = sortDims([customDims[id].l, customDims[id].w, customDims[id].h]);
        game.source = 'custom';
        saveCache($('bggUser').value, games);
        render();
      }
      closeEditModal();
    }

    /* ═══════════════════════════════════════════════════
       PHASE 3: UI CONTROLS & EVENTS
       ═══════════════════════════════════════════════════ */
    $('searchFilter').addEventListener('input', () => { if (lastPacked) renderTable(lastPacked, orientationSelect.value); });
    $('fitFilter').addEventListener('change', () => { if (lastPacked) renderTable(lastPacked, orientationSelect.value); });

    const savedTheme = localStorage.getItem('bgsize_theme');
    if (savedTheme) document.documentElement.setAttribute('data-theme', savedTheme);
    $('themeToggle').addEventListener('click', () => {
      let currentTheme = document.documentElement.getAttribute('data-theme');
      if (!currentTheme) {
        currentTheme = window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
      }
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('bgsize_theme', newTheme);
    });

    /* ═══════════════════════════════════════════════════
       UTILITY
       ═══════════════════════════════════════════════════ */
    function delay(ms) { return new Promise(r => setTimeout(r, ms)); }
  
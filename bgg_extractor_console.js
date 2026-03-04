/**
 * BGG Dimension Extractor - Browser Console Script
 * 
 * Usage: 
 * 1. Go to your BGG game page or collection
 * 2. Open DevTools (F12 or Right-click > Inspect)
 * 3. Go to Console tab
 * 4. Paste this entire script
 * 5. Press Enter
 * 6. A CSV file will download automatically
 * 
 * Works on:
 * - Individual game pages (extracts that game's dimensions)
 * - Collection pages (extracts all visible games)
 */

(function() {
  const results = [];
  
  // Helper: Extract dimensions from text like "12.0 x 8.0 x 5.0 cm"
  function parseDimensions(text) {
    const pattern = /(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*[x×]\s*(\d+(?:\.\d+)?)\s*(?:cm|inches?)?/i;
    const match = text.match(pattern);
    if (match) {
      return {
        length: parseFloat(match[1]),
        width: parseFloat(match[2]),
        height: parseFloat(match[3])
      };
    }
    return null;
  }
  
  // Helper: Extract game ID from URL
  function getGameIdFromElement(element) {
    // Look for game links in various BGG formats
    const link = element.querySelector('a[href*="/boardgame/"]') || element;
    const href = link.href || link.getAttribute('href') || '';
    const match = href.match(/\/boardgame\/(\d+)/);
    return match ? match[1] : null;
  }
  
  // Helper: Get game name from element
  function getGameNameFromElement(element) {
    const nameEl = element.querySelector('h1, h2, [class*="name"], a[href*="/boardgame/"]');
    if (nameEl) {
      return nameEl.textContent.trim().split('\n')[0];
    }
    return 'Unknown';
  }
  
  // Helper: Download CSV
  function downloadCSV(data) {
    const csv = 'Game ID,Game Name,Length (cm),Width (cm),Height (cm)\n' +
      data.map(row => 
        `${row.id},"${row.name.replace(/"/g, '""')}",${row.length},${row.width},${row.height}`
      ).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `bgg_dimensions_${Date.now()}.csv`;
    link.click();
    window.URL.revokeObjectURL(url);
  }
  
  console.log('🎲 BGG Dimension Extractor Started...\n');
  
  // Try to detect what page we're on
  const isCollectionPage = document.body.innerHTML.includes('collection') || 
                           document.querySelectorAll('[data-gameid], tr[data-id*="item"]').length > 5;
  
  if (isCollectionPage) {
    console.log('📋 Collection page detected. Scanning for games...\n');
    
    // Try multiple selectors for collection items
    const gameRows = document.querySelectorAll(
      'tr[data-id], tr[data-gameid], [data-gameid], .collectionitem, [class*="collection-item"]'
    );
    
    console.log(`Found ${gameRows.length} game rows\n`);
    
    gameRows.forEach((row, index) => {
      try {
        const gameId = row.getAttribute('data-id') || 
                      row.getAttribute('data-gameid') || 
                      getGameIdFromElement(row);
        
        let gameName = row.getAttribute('data-gamename') || getGameNameFromElement(row);
        
        // Look for dimensions in the row
        let dimensions = null;
        const text = row.textContent;
        dimensions = parseDimensions(text);
        
        if (gameId && dimensions) {
          console.log(`✓ Game ${index + 1}: ${gameName} (${gameId})`);
          console.log(`  → ${dimensions.length} × ${dimensions.width} × ${dimensions.height} cm\n`);
          
          results.push({
            id: gameId,
            name: gameName,
            length: dimensions.length,
            width: dimensions.width,
            height: dimensions.height
          });
        }
      } catch (e) {
        // Skip this row silently
      }
    });
    
  } else {
    // Single game page - look for dimension section
    console.log('🎯 Single game page detected. Looking for dimensions...\n');
    
    // Try to find game ID and name
    const gameId = window.location.pathname.match(/\/boardgame\/(\d+)/)?.[1];
    const gameName = document.querySelector('h1')?.textContent?.trim() || 'Unknown Game';
    
    // Look for dimensions in common places
    const pageText = document.body.textContent;
    const dimensions = parseDimensions(pageText);
    
    if (gameId && dimensions) {
      console.log(`✓ Found game: ${gameName} (${gameId})`);
      console.log(`  → ${dimensions.length} × ${dimensions.width} × ${dimensions.height} cm\n`);
      
      results.push({
        id: gameId,
        name: gameName,
        length: dimensions.length,
        width: dimensions.width,
        height: dimensions.height
      });
    } else {
      console.log(`⚠️ Could not find dimensions on this page.`);
      console.log(`Make sure you're on a game page with the "Size" field visible.\n`);
    }
  }
  
  // Summary and download
  console.log('=' .repeat(50));
  if (results.length > 0) {
    console.log(`\n✅ EXTRACTED ${results.length} GAME(S) WITH DIMENSIONS\n`);
    
    // Show preview
    console.table(results);
    
    console.log('\n📥 Downloading CSV...');
    downloadCSV(results);
    console.log('✓ CSV downloaded as bgg_dimensions_' + Date.now() + '.csv');
  } else {
    console.log('\n❌ NO DIMENSIONS FOUND');
    console.log('\nTroubleshooting:');
    console.log('1. Make sure you\'re on a BGG game or collection page');
    console.log('2. For single game: check that the Size field is visible');
    console.log('3. For collection: games should display dimensions in the table');
    console.log('4. Try manually opening each game and running this script again');
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('Done! Import the CSV into the shelf planner app.');
})();

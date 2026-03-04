(function() {
  console.log('🔍 BGG Page Diagnostic\n');
  console.log('Current URL:', window.location.href);
  console.log('Page title:', document.title);
  
  // Check for table rows
  const allRows = document.querySelectorAll('table tbody tr, table tr, tr');
  console.log(`\nTotal table rows found: ${allRows.length}`);
  
  if (allRows.length > 0) {
    console.log('\nFirst row HTML:');
    console.log(allRows[0].outerHTML.substring(0, 500));
    console.log('\nFirst row text:');
    console.log(allRows[0].textContent.substring(0, 300));
  }
  
  // Check for game links
  const gameLinks = document.querySelectorAll('a[href*="/boardgame/"]');
  console.log(`\n\nGame links found: ${gameLinks.length}`);
  if (gameLinks.length > 0) {
    console.log('First game link:', gameLinks[0].href);
    console.log('First game text:', gameLinks[0].textContent);
  }
  
  // Check for dimension patterns
  const pageText = document.body.textContent;
  const dimPattern = /(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*[x×]\s*(\d+\.?\d*)\s*cm/gi;
  const matches = pageText.match(dimPattern);
  console.log(`\nDimension patterns found: ${matches ? matches.length : 0}`);
  if (matches) {
    console.log('Examples:', matches.slice(0, 5));
  }
})();

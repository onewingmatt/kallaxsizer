const fs = require('fs');
function parseCsvLine(text) {
    const result = [];
    let current = '';
    let inQuote = false;
    for (let i = 0; i < text.length; i++) {
        const char = text[i];
        if (char === '"') {
            if (inQuote && i + 1 < text.length && text[i + 1] === '"') {
                current += '"';
                i++;
            } else {
                inQuote = !inQuote;
            }
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

const text = fs.readFileSync('/home/onewing/Downloads/collection (1).csv', 'utf8');
const lines = text.split(/\r?\n/).filter(l => l.trim());
console.log(parseCsvLine(lines[0]).slice(0, 5));

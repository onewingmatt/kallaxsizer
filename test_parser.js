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
                i++; // skip escaped quote
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
    return result;
}

const lines = fs.readFileSync('test_export.csv', 'utf8').split(/\r?\n/).filter(l => l.trim());
console.log(parseCsvLine(lines[0]));
console.log(parseCsvLine(lines[1]));

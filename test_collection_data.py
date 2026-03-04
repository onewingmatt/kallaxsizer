#!/usr/bin/env python3
"""
Check what data is available in BGG collection responses.
"""
import urllib.request
import xml.etree.ElementTree as ET

BROWSER_UA = "Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0"

def fetch_collection_sample():
    """Fetch a sample collection to see what dimension data is available."""
    # Using a test username - won't work if private, but collections are usually public for testing
    url = "https://boardgamegeek.com/xmlapi2/collection/johndoe?own=1&excludeaccessory=1"
    
    print("Fetching sample collection response...")
    print(f"URL: {url}\n")
    
    try:
        req = urllib.request.Request(url)
        req.add_header("User-Agent", BROWSER_UA)
        
        with urllib.request.urlopen(req, timeout=10) as resp:
            xml_text = resp.read().decode('utf-8')
            
            # Parse and inspect
            root = ET.fromstring(xml_text)
            
            # Get first few items to see structure
            items = root.findall('.//item')[:3]
            
            if not items:
                print("❌ No items found in response")
                return
            
            print(f"✅ Found collection with {len(root.findall('.//item'))} items\n")
            print("Sample item structure (first item):")
            print("=" * 60)
            
            if items:
                item = items[0]
                print(f"<item id='{item.get('id')}'>\n")
                
                # Print all child elements
                for child in item:
                    text = child.text[:50] if child.text else "(empty)"
                    attribs = ' '.join([f"{k}='{v}'" for k, v in child.attrib.items()])
                    print(f"  <{child.tag} {attribs}>{text}...</{child.tag}>")
                
                # Check for version/image data
                print("\n  Checking for nested version/image data...")
                for version in item.findall('.//version'):
                    print(f"    <version id='{version.get('id')}'> found")
                    # Check for dimensions in version
                    for child in version:
                        if 'dim' in child.tag.lower() or 'size' in child.tag.lower():
                            print(f"      <{child.tag}>{child.text}</...>")
            
            print("\n" + "=" * 60)
            print("\nConclusion: Check if collection items have dimensions in:")
            print("  - <image> tags")
            print("  - <yearpublished> context")
            print("  - <name>/<description> fields")
            print("  - <version> sub-elements")
            
    except urllib.error.HTTPError as e:
        print(f"❌ HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"❌ Error: {e}")

fetch_collection_sample()

# CLI Standardization - Change Summary

## What Changed

All command-line arguments have been **standardized to use `-u` for the target** across all scan modes for consistency and ease of use.

## Before vs After

### Nmap
```bash
# Before
python3 securityscanner.py nmap -t 192.168.1.1 -p common

# After
python3 securityscanner.py nmap -u 192.168.1.1 -p common
```

### Subfinder
```bash
# Before
python3 securityscanner.py subfinder -d example.com

# After
python3 securityscanner.py subfinder -u example.com
```

### Brute Force
```bash
# Before
python3 securityscanner.py bruteforce -t http://example.com -P http-basic

# After  
python3 securityscanner.py bruteforce -u http://example.com -P http-basic
```

**Note**: Brute force wordlist arguments changed to avoid conflicts:
- `-u` → `--user-list` (username wordlist)
- `-p` → `--pass-list` (password wordlist)

### XSS (No Change)
```bash
# Already used -u
python3 securityscanner.py xss -u "http://example.com/search?q=test"
```

## Benefits

✅ **Consistent** - Same flag `-u` for target across all modes  
✅ **Intuitive** - `-u` makes sense for URL/URI/target  
✅ **Easier to remember** - No need to remember different flags per mode  
✅ **Less confusing** - No mix of `-t`, `-d`, `-u` anymore

## Updated Documentation

All documentation has been updated:
- ✅ `README.md` - All examples use `-u`
- ✅ `QUICKSTART.md` - Quick commands updated
- ✅ `securityscanner.py` - Help text and examples
- ✅ In-tool `--help` - All subcommands

## Quick Reference

```bash
# All scans now use -u for target
python3 securityscanner.py nmap -u <target>
python3 securityscanner.py subfinder -u <domain>
python3 securityscanner.py bruteforce -u <url> -P <protocol>
python3 securityscanner.py xss -u <url>

# Brute force wordlists (if custom)
python3 securityscanner.py bruteforce -u <url> -P ssh --user-list users.txt --pass-list pass.txt
```

## Testing Verified

✅ Help system shows correct arguments  
✅ Nmap accepts `-u` for target  
✅ Subfinder accepts `-u` for domain  
✅ Brute force accepts `-u` for target  
✅ XSS still works with `-u` for URL  
✅ No argument conflicts

---

**You can now use `-u` consistently across all scan types!** 🎉

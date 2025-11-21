# 🗄️ Redis Commands for EchoDuo

Quick reference for interacting with Redis manually.

## 📊 View Data

### View all recent sponsors
```bash
redis-cli LRANGE recent_sponsors 0 -1
```

### View all phrases
```bash
redis-cli LRANGE recent_phrases 0 -1
```

### View first 5 phrases only
```bash
redis-cli LRANGE recent_phrases 0 4
```

### View tone patterns
```bash
redis-cli LRANGE tone_patterns 0 -1
```

## 📏 Check Sizes

### Count sponsors
```bash
redis-cli LLEN recent_sponsors
```

### Count phrases
```bash
redis-cli LLEN recent_phrases
```

### Count all keys
```bash
redis-cli DBSIZE
```

## 🧹 Clear Data

### Clear specific key
```bash
redis-cli DEL recent_sponsors
redis-cli DEL recent_phrases  
redis-cli DEL tone_patterns
```

### Clear ALL EchoDuo data
```bash
redis-cli DEL recent_sponsors recent_phrases tone_patterns
```

### Clear entire Redis database (⚠️ WARNING: Deletes everything!)
```bash
redis-cli FLUSHDB
```

## 🔍 Inspect Data

### Check if key exists
```bash
redis-cli EXISTS recent_sponsors
```

### Get key type
```bash
redis-cli TYPE recent_sponsors
```

### View memory usage
```bash
redis-cli INFO memory | grep "used_memory_human"
```

### View keyspace info
```bash
redis-cli INFO keyspace
```

## ✏️ Manual Manipulation

### Add sponsor manually
```bash
redis-cli LPUSH recent_sponsors "Nike"
```

### Remove oldest sponsor
```bash
redis-cli RPOP recent_sponsors
```

### View specific position
```bash
redis-cli LINDEX recent_sponsors 0  # First item
redis-cli LINDEX recent_sponsors -1 # Last item
```

### Trim list to size
```bash
redis-cli LTRIM recent_sponsors 0 4  # Keep only 5 items
```

## 📺 Monitor in Real-Time

### Watch all Redis commands as they happen
```bash
redis-cli MONITOR
```

Then run EchoDuo in another terminal:
```bash
python echoduo.py "test topic"
```

You'll see all Redis commands in real-time!

## 🔧 Useful Combos

### Reset memory and check
```bash
redis-cli DEL recent_sponsors recent_phrases tone_patterns && \
redis-cli DBSIZE
```

### View all EchoDuo data at once
```bash
echo "=== Sponsors ===" && \
redis-cli LRANGE recent_sponsors 0 -1 && \
echo "" && echo "=== Phrases (first 5) ===" && \
redis-cli LRANGE recent_phrases 0 4 && \
echo "" && echo "=== Patterns ===" && \
redis-cli LRANGE tone_patterns 0 -1
```

### Check Redis connection
```bash
redis-cli PING
# Should return: PONG
```

## 🐍 Python Examples

### Using Redis directly in Python
```python
import redis

# Connect
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# View sponsors
sponsors = r.lrange('recent_sponsors', 0, -1)
print(sponsors)

# Add sponsor
r.lpush('recent_sponsors', 'Nike')

# Remove oldest
r.ltrim('recent_sponsors', 0, 4)

# Clear all
r.delete('recent_sponsors', 'recent_phrases', 'tone_patterns')
```

### Check EchoDuo memory from Python
```python
from memory_manager import MemoryManager

memory = MemoryManager()
summary = memory.get_memory_summary()
print(summary)
```

## 📈 Performance Tips

### Check memory usage
```bash
redis-cli INFO memory
```

### Check slowlog (slow operations)
```bash
redis-cli SLOWLOG GET 10
```

### Test Redis performance
```bash
redis-cli --latency
```

## 🎯 EchoDuo-Specific Workflows

### Reset and start fresh
```bash
redis-cli DEL recent_sponsors recent_phrases tone_patterns
python echoduo.py --show-memory
# Should show empty
```

### Force specific sponsor order
```bash
redis-cli DEL recent_sponsors
redis-cli LPUSH recent_sponsors "Calm" "Nike" "Notion"
python echoduo.py "test" --sponsor Coder
# Coder will be added to the list
```

### Check what will be used next
```bash
# Get blocked sponsors
redis-cli LRANGE recent_sponsors 0 -1

# Available = All sponsors - Blocked sponsors
# All: Calm, Nike, Notion, Coder, Forethought, Skyflow
```

---

**Pro Tip:** Keep `redis-cli MONITOR` running in a separate terminal while using EchoDuo to see all Redis operations in real-time!


#!/bin/bash
# Clean Redis viewer script for EchoDuo

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ 📊 ECHODUO REDIS DATA VIEWER                                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Redis is running
if ! redis-cli ping > /dev/null 2>&1; then
    echo "❌ Redis is not running!"
    echo "   Start it with: brew services start redis"
    exit 1
fi

echo "✅ Redis is running"
echo ""

# View sponsors
echo "📋 RECENT SPONSORS ($(redis-cli LLEN recent_sponsors 2>/dev/null || echo 0) total):"
echo "─────────────────────────────────────────────────────────────────"
if redis-cli EXISTS recent_sponsors > /dev/null 2>&1; then
    redis-cli LRANGE recent_sponsors 0 -1 2>/dev/null | nl
else
    echo "   (empty)"
fi
echo ""

# View phrases
echo "💬 RECENT PHRASES ($(redis-cli LLEN recent_phrases 2>/dev/null || echo 0) total):"
echo "─────────────────────────────────────────────────────────────────"
if redis-cli EXISTS recent_phrases > /dev/null 2>&1; then
    redis-cli LRANGE recent_phrases 0 9 2>/dev/null | nl
    echo "   ... (showing first 10, run 'redis-cli LRANGE recent_phrases 0 -1' for all)"
else
    echo "   (empty)"
fi
echo ""

# View tone patterns
echo "🎨 TONE PATTERNS ($(redis-cli LLEN tone_patterns 2>/dev/null || echo 0) total):"
echo "─────────────────────────────────────────────────────────────────"
if redis-cli EXISTS tone_patterns > /dev/null 2>&1; then
    redis-cli LRANGE tone_patterns 0 -1 2>/dev/null | nl
else
    echo "   (empty)"
fi
echo ""

# Summary
echo "📊 SUMMARY:"
echo "─────────────────────────────────────────────────────────────────"
echo "   Total keys: $(redis-cli DBSIZE 2>/dev/null || echo 0)"
echo "   Sponsors:   $(redis-cli LLEN recent_sponsors 2>/dev/null || echo 0)"
echo "   Phrases:    $(redis-cli LLEN recent_phrases 2>/dev/null || echo 0)"
echo "   Patterns:   $(redis-cli LLEN tone_patterns 2>/dev/null || echo 0)"
echo ""

echo "💡 TIP: Run 'redis-cli MONITOR' in another terminal to watch"
echo "   Redis operations in real-time!"
echo ""


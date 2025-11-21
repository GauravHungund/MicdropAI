#!/bin/bash
# Redis Server Monitoring Commands

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ 🔍 REDIS SERVER MONITORING COMMANDS                               ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Redis is running
echo "1. CHECK IF REDIS IS RUNNING:"
echo "   redis-cli ping"
echo "   (Should return: PONG)"
echo ""

# Connect to Redis CLI
echo "2. CONNECT TO REDIS CLI:"
echo "   redis-cli"
echo "   (Interactive Redis command line)"
echo ""

# Server Info
echo "3. GET SERVER INFO:"
echo "   redis-cli INFO"
echo "   (Detailed server information)"
echo ""

# Server Status (quick)
echo "4. QUICK SERVER STATUS:"
echo "   redis-cli INFO server"
echo "   (Server-specific info)"
echo ""

# Database Stats
echo "5. DATABASE STATISTICS:"
echo "   redis-cli INFO stats"
echo "   (Statistics about operations)"
echo ""

# Memory Info
echo "6. MEMORY INFORMATION:"
echo "   redis-cli INFO memory"
echo "   (Memory usage details)"
echo ""

# List All Keys
echo "7. LIST ALL KEYS:"
echo "   redis-cli KEYS '*'"
echo "   (Shows all keys in database)"
echo ""

# Count Keys
echo "8. COUNT KEYS:"
echo "   redis-cli DBSIZE"
echo "   (Total number of keys)"
echo ""

# View EchoDuo Specific Keys
echo "9. VIEW ECHODUO KEYS:"
echo "   redis-cli KEYS 'echoduo:*'"
echo "   (EchoDuo-specific keys)"
echo ""

# View Sponsor History
echo "10. VIEW SPONSOR HISTORY:"
echo "    redis-cli LRANGE echoduo:sponsors 0 -1"
echo "    (List of recent sponsors)"
echo ""

# View Phrase History
echo "11. VIEW PHRASE HISTORY:"
echo "    redis-cli LRANGE echoduo:phrases 0 -1"
echo "    (List of tracked phrases)"
echo ""

# Monitor Commands in Real-Time
echo "12. MONITOR ALL COMMANDS (REAL-TIME):"
echo "    redis-cli MONITOR"
echo "    (Shows all commands as they execute - Ctrl+C to stop)"
echo ""

# Get Value by Key
echo "13. GET VALUE BY KEY:"
echo "    redis-cli GET 'key_name'"
echo "    (Get value for a specific key)"
echo ""

# Get Type of Key
echo "14. GET KEY TYPE:"
echo "    redis-cli TYPE 'key_name'"
echo "    (Returns: string, list, set, hash, etc.)"
echo ""

# Check Redis Process
echo "15. CHECK REDIS PROCESS:"
echo "    ps aux | grep redis"
echo "    (Shows if Redis process is running)"
echo ""

# Redis Version
echo "16. REDIS VERSION:"
echo "    redis-cli INFO server | grep redis_version"
echo "    (Shows Redis version)"
echo ""

# Flush Database (CAUTION!)
echo "17. FLUSH DATABASE (DANGEROUS - DELETES ALL DATA):"
echo "    redis-cli FLUSHDB"
echo "    (Deletes all keys in current database)"
echo ""

echo "═══════════════════════════════════════════════════════════════════"
echo ""
echo "QUICK REFERENCE:"
echo ""
echo "  Start Redis (if installed via Homebrew):"
echo "    brew services start redis"
echo ""
echo "  Stop Redis:"
echo "    brew services stop redis"
echo ""
echo "  Restart Redis:"
echo "    brew services restart redis"
echo ""
echo "  Check Redis Status:"
echo "    brew services list | grep redis"
echo ""
echo "═══════════════════════════════════════════════════════════════════"


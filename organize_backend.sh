#!/bin/bash
# Organize project: Move files to backend, clean up unnecessary files

cd /Users/gauravhungund/Documents/SF_AWS_HACK

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ 🗂️  ORGANIZING PROJECT INTO BACKEND FOLDER                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Move core Python files
echo "📦 Moving core Python files..."
mv podcast_generator.py backend/ 2>/dev/null && echo "  ✅ podcast_generator.py"
mv claude_client.py backend/ 2>/dev/null && echo "  ✅ claude_client.py"
mv sanity_client.py backend/ 2>/dev/null && echo "  ✅ sanity_client.py"
mv config.py backend/ 2>/dev/null && echo "  ✅ config.py"
mv memory_manager.py backend/ 2>/dev/null && echo "  ✅ memory_manager.py"
mv lightpanda_scraper.py backend/ 2>/dev/null && echo "  ✅ lightpanda_scraper.py"
mv lightpanda_playwright_client.py backend/ 2>/dev/null && echo "  ✅ lightpanda_playwright_client.py"
mv playwright_scraper.py backend/ 2>/dev/null && echo "  ✅ playwright_scraper.py"
mv smart_scraper.py backend/ 2>/dev/null && echo "  ✅ smart_scraper.py"
mv echoduo.py backend/ 2>/dev/null && echo "  ✅ echoduo.py"
mv api.py backend/ 2>/dev/null && echo "  ✅ api.py"
mv batch_generator.py backend/ 2>/dev/null && echo "  ✅ batch_generator.py"
mv demo.py backend/ 2>/dev/null && echo "  ✅ demo.py"
mv view_episodes.py backend/ 2>/dev/null && echo "  ✅ view_episodes.py"
mv test_sanity_connection.py backend/ 2>/dev/null && echo "  ✅ test_sanity_connection.py"
mv test_echoduo.py backend/ 2>/dev/null && echo "  ✅ test_echoduo.py"
mv test_sanity.py backend/ 2>/dev/null && echo "  ✅ test_sanity.py"
mv test_smart_scraping.py backend/ 2>/dev/null && echo "  ✅ test_smart_scraping.py"

# Move config and requirements
echo ""
echo "📋 Moving configuration files..."
mv requirements.txt backend/ 2>/dev/null && echo "  ✅ requirements.txt"
mv env.example backend/ 2>/dev/null && echo "  ✅ env.example"

# Move data files
echo ""
echo "📊 Moving data files..."
mv valid_test_urls.json backend/ 2>/dev/null && echo "  ✅ valid_test_urls.json"
mv quick_test_urls.txt backend/ 2>/dev/null && echo "  ✅ quick_test_urls.txt"
mv example_batch.json backend/ 2>/dev/null && echo "  ✅ example_batch.json"
mv example_output.txt backend/ 2>/dev/null && echo "  ✅ example_output.txt"

# Move schema files
echo ""
echo "📐 Moving schema files..."
mkdir -p backend/sanity_schema 2>/dev/null
mv sanity_schema/episode.js backend/sanity_schema/ 2>/dev/null && echo "  ✅ sanity_schema/episode.js"

echo ""
echo "🗑️  Deleting unnecessary test/debug files..."
rm -f test_api.py test_sanity_response.py test_sanity_id_fix.py test_lightpanda.py 2>/dev/null && echo "  ✅ Removed debug test files"
rm -f lightpanda_client.py lightpanda_cloud_client.py 2>/dev/null && echo "  ✅ Removed old Lightpanda clients"
rm -f redis_demo.py redis_demo_auto.py redis_visual_demo.sh redis_realtime.py 2>/dev/null && echo "  ✅ Removed demo scripts"
rm -f run_demo.sh quick_view.sh quickstart.sh setup_sanity_studio.sh 2>/dev/null && echo "  ✅ Removed setup scripts"
rm -f setup_sanity_schema.py create_sanity_schema_simple.py 2>/dev/null && echo "  ✅ Removed schema setup scripts"
rm -f test_sanity_response.py web_interface.html 2>/dev/null && echo "  ✅ Removed test files"

echo ""
echo "📚 Organizing documentation..."
mkdir -p docs 2>/dev/null
mv ARCHITECTURE.md docs/ 2>/dev/null && echo "  ✅ ARCHITECTURE.md → docs/"
mv CONTRIBUTING.md docs/ 2>/dev/null && echo "  ✅ CONTRIBUTING.md → docs/"
mv GETTING_STARTED.md docs/ 2>/dev/null && echo "  ✅ GETTING_STARTED.md → docs/"
mv PROJECT_SUMMARY.md docs/ 2>/dev/null && echo "  ✅ PROJECT_SUMMARY.md → docs/"
mv QUICK_REFERENCE.md docs/ 2>/dev/null && echo "  ✅ QUICK_REFERENCE.md → docs/"
mv SETUP.md docs/ 2>/dev/null && echo "  ✅ SETUP.md → docs/"
mv UPDATE_SUMMARY.md docs/ 2>/dev/null && echo "  ✅ UPDATE_SUMMARY.md → docs/"
mv USAGE_GUIDE.md docs/ 2>/dev/null && echo "  ✅ USAGE_GUIDE.md → docs/"
mv CHANGELOG.md docs/ 2>/dev/null && echo "  ✅ CHANGELOG.md → docs/"
mv SANITY_*.md docs/ 2>/dev/null && echo "  ✅ SANITY_*.md → docs/"
mv view_episodes_web.md docs/ 2>/dev/null && echo "  ✅ view_episodes_web.md → docs/"
mv view_in_sanity_dashboard.md docs/ 2>/dev/null && echo "  ✅ view_in_sanity_dashboard.md → docs/"
mv sanity_hostname_help.md docs/ 2>/dev/null && echo "  ✅ sanity_hostname_help.md → docs/"
mv REDIS_*.md docs/ 2>/dev/null && echo "  ✅ REDIS_*.md → docs/"
mv SMART_SCRAPING.md docs/ 2>/dev/null && echo "  ✅ SMART_SCRAPING.md → docs/"
mv LIGHTPANDA_STATUS.md docs/ 2>/dev/null && echo "  ✅ LIGHTPANDA_STATUS.md → docs/"
mv STATUS.md docs/ 2>/dev/null && echo "  ✅ STATUS.md → docs/"

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║ ✅ ORGANIZATION COMPLETE!                                        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "Project structure:"
echo "  backend/          - All Python code and core files"
echo "  studio-hello-world/ - Sanity Studio (frontend)"
echo "  docs/             - Documentation"
echo "  venv/             - Python virtual environment"
echo "  README.md         - Main readme (root)"
echo "  INFORMATION.md    - Project information (root)"
echo ""


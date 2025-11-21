# 📝 Changelog

All notable changes to EchoDuo will be documented in this file.

## [1.0.1] - 2025-11-21

### 🔄 Changed - Migration to Anthropic SDK

**Major Update**: Switched from AWS Bedrock to direct Anthropic API integration.

#### What Changed

**Removed:**
- ❌ AWS Bedrock dependencies (boto3)
- ❌ AWS credential configuration
- ❌ `bedrock_client.py` module
- ❌ AWS region configuration

**Added:**
- ✅ Direct Anthropic Python SDK (`anthropic` package)
- ✅ New `claude_client.py` module
- ✅ Simpler API key authentication
- ✅ Streaming support for real-time output

**Updated:**
- 📝 All documentation files updated
- 📝 Configuration now uses `ANTHROPIC_API_KEY`
- 📝 Simplified setup process
- 📝 Updated error messages and troubleshooting

#### Why This Change?

1. **Simpler Setup**: No AWS account needed, just an API key
2. **Lower Barrier**: Easier for developers to get started
3. **Direct Access**: Use Anthropic's API without AWS intermediary
4. **Better Control**: More straightforward error handling
5. **Cost Transparency**: Direct billing through Anthropic

#### Migration Guide

If you were using the previous AWS Bedrock version:

**Old Configuration (`.env`):**
```bash
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
MODEL_ID=anthropic.claude-3-5-sonnet-20241022-v2:0
```

**New Configuration (`.env`):**
```bash
ANTHROPIC_API_KEY=sk-ant-your-key-here
MODEL_NAME=claude-3-5-sonnet-20241022
MAX_TOKENS=4096
DEFAULT_TEMPERATURE=0.7
```

**Migration Steps:**

1. Get Anthropic API Key:
   - Visit https://console.anthropic.com/
   - Create an API key

2. Update `.env` file:
   ```bash
   # Remove AWS credentials
   # Add Anthropic API key
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

3. Reinstall dependencies:
   ```bash
   pip install -r requirements.txt --upgrade
   ```

4. Test:
   ```bash
   python echoduo.py "test topic"
   ```

#### Performance Impact

- ✅ **Same Quality**: Uses identical Claude 3.5 Sonnet model
- ✅ **Similar Speed**: 45-65 seconds per episode (unchanged)
- ✅ **Comparable Cost**: ~$0.035-0.10 per episode (similar to Bedrock)
- ✅ **Better Errors**: More informative error messages

#### API Differences

| Feature | AWS Bedrock | Anthropic SDK |
|---------|-------------|---------------|
| Setup Complexity | High (AWS account, Bedrock access) | Low (Just API key) |
| Authentication | AWS credentials | API key |
| Error Messages | AWS-specific | Anthropic-specific |
| Streaming | Supported | Supported |
| Model Access | May require approval | Immediate |

---

## [1.0.0] - 2025-11-21

### 🎉 Initial Release

**EchoDuo** - Autonomous AI podcast generation system with intelligent sponsor integration.

#### Core Features

- ✅ **Natural Conversations**: Two-host dialogue (Alex & Maya)
- ✅ **Sponsor Integration**: Subtle, contextual sponsor mentions
- ✅ **Real-World Context**: Web scraping for current information
- ✅ **Memory Management**: Redis-based memory to avoid repetition
- ✅ **Self-Improvement**: Auto-critique and improvement loop
- ✅ **Multiple Interfaces**: CLI, API, Web UI
- ✅ **Batch Processing**: Generate multiple episodes

#### Sponsors Supported

- Calm (Mental health, wellness)
- Nike (Fitness, sports)
- Notion (Productivity, organization)
- Coder (Developer tools)
- Forethought (AI automation)
- Skyflow (Data privacy, security)

#### Documentation

- 📚 README.md - Main documentation
- 📚 SETUP.md - Setup instructions
- 📚 USAGE_GUIDE.md - Complete usage examples
- 📚 ARCHITECTURE.md - Technical deep dive
- 📚 PROJECT_SUMMARY.md - Project overview
- 📚 CONTRIBUTING.md - Contribution guidelines
- 📚 QUICK_REFERENCE.md - Command cheat sheet
- 📚 example_output.txt - Sample episodes

#### Components

- `echoduo.py` - Main CLI interface
- `podcast_generator.py` - Core generation logic
- `bedrock_client.py` - AWS Bedrock integration (deprecated in v1.0.1)
- `memory_manager.py` - Redis memory management
- `lightpanda_scraper.py` - Web scraping
- `api.py` - Flask REST API
- `demo.py` - Interactive demo
- `batch_generator.py` - Batch processing
- `test_echoduo.py` - Test suite
- `web_interface.html` - Web UI

---

## Versioning

EchoDuo follows [Semantic Versioning](https://semver.org/):

- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

## Links

- **Repository**: (Add your repo link)
- **Issues**: (Add issues link)
- **Documentation**: See README.md
- **API Reference**: See USAGE_GUIDE.md

---

**Last Updated**: November 21, 2025



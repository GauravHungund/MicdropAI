# 🤝 Contributing to EchoDuo

Thank you for your interest in contributing to EchoDuo! This document provides guidelines for contributing to the project.

## 🌟 Ways to Contribute

### 1. Report Bugs
- Use GitHub Issues
- Include detailed reproduction steps
- Provide error messages and logs
- Specify your environment (OS, Python version, etc.)

### 2. Suggest Features
- Open an issue with "Feature Request" label
- Describe the use case
- Explain expected behavior
- Consider implementation complexity

### 3. Improve Documentation
- Fix typos or unclear sections
- Add examples
- Improve explanations
- Translate documentation

### 4. Submit Code
- Fix bugs
- Implement features
- Improve performance
- Add tests

## 🔧 Development Setup

### 1. Fork and Clone

```bash
git clone https://github.com/yourusername/echoduo.git
cd echoduo
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp env.example .env
# Add your Anthropic API key
```

### 4. Run Tests

```bash
python test_echoduo.py
```

## 📝 Code Style Guidelines

### Python Style

- Follow PEP 8
- Use type hints where appropriate
- Maximum line length: 100 characters
- Use descriptive variable names

### Example:

```python
def generate_podcast(topic: str, context: Optional[str] = None) -> Dict[str, str]:
    """
    Generate a podcast episode.
    
    Args:
        topic: Main subject of the podcast
        context: Optional real-world context
    
    Returns:
        Dict containing conversation and metadata
    """
    # Implementation
    pass
```

### Documentation

- Docstrings for all public functions
- Comments for complex logic
- Update relevant .md files
- Include usage examples

## 🎯 Pull Request Process

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Changes

- Write clean, documented code
- Follow existing patterns
- Add tests if applicable
- Update documentation

### 3. Test Your Changes

```bash
# Run existing tests
python test_echoduo.py

# Test your specific feature
python echoduo.py "test topic"

# Test API if relevant
python api.py
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: add new feature description"
# or
git commit -m "fix: resolve bug description"
```

**Commit Message Format:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation only
- `style:` Formatting, missing semicolons, etc.
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `test:` Adding tests
- `chore:` Updating build tasks, package manager configs, etc.

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear description of changes
- Link to related issues
- Screenshots if UI changes
- Test results

## 🧪 Testing Guidelines

### Test Categories

1. **Unit Tests:** Test individual functions
2. **Integration Tests:** Test component interactions
3. **End-to-End Tests:** Test complete workflows

### Writing Tests

```python
def test_sponsor_selection():
    """Test that sponsor selection works correctly."""
    generator = PodcastGenerator()
    sponsor = generator.select_sponsor("AI automation", [])
    assert sponsor in AVAILABLE_SPONSORS
```

### Running Tests

```bash
# Run all tests
python test_echoduo.py

# Test specific component
python -c "from test_echoduo import test_sponsor_selection; test_sponsor_selection()"
```

## 📋 Areas for Contribution

### High Priority

- [ ] Improve sponsor integration subtlety
- [ ] Add more fallback contexts
- [ ] Optimize generation speed
- [ ] Add comprehensive test suite
- [ ] Improve error messages

### Medium Priority

- [ ] Add audio generation (TTS)
- [ ] Multi-episode story arcs
- [ ] Sentiment analysis for topics
- [ ] Analytics dashboard
- [ ] Docker containerization

### Low Priority

- [ ] Additional host personalities
- [ ] Theme customization
- [ ] Export to different formats
- [ ] Integration with podcast platforms
- [ ] Admin interface

## 🐛 Bug Report Template

```markdown
**Describe the bug**
A clear description of what the bug is.

**To Reproduce**
Steps to reproduce:
1. Run command '...'
2. See error

**Expected behavior**
What you expected to happen.

**Actual behavior**
What actually happened.

**Environment**
- OS: [e.g., macOS 14.0]
- Python version: [e.g., 3.11.5]
- EchoDuo version: [e.g., 1.0.0]

**Error messages**
```
Paste error messages here
```

**Additional context**
Any other relevant information.
```

## ✨ Feature Request Template

```markdown
**Feature description**
Clear description of the feature.

**Use case**
Why is this feature needed?

**Proposed solution**
How should this work?

**Alternatives considered**
Other approaches you've thought about.

**Additional context**
Any other relevant information.
```

## 🎨 Design Principles

When contributing, keep these principles in mind:

1. **Simplicity:** Prefer simple solutions over complex ones
2. **Modularity:** Keep components loosely coupled
3. **Extensibility:** Make it easy to add new features
4. **Performance:** Consider efficiency and scalability
5. **User Experience:** Make it intuitive and helpful
6. **Documentation:** Code should be self-documenting

## 📊 Performance Considerations

### Do:
- ✅ Cache expensive operations
- ✅ Use async for I/O operations
- ✅ Batch API calls when possible
- ✅ Minimize memory usage

### Don't:
- ❌ Make unnecessary API calls
- ❌ Load large datasets into memory
- ❌ Perform blocking operations
- ❌ Ignore error handling

## 🔒 Security Guidelines

### Do:
- ✅ Validate all user inputs
- ✅ Use environment variables for secrets
- ✅ Sanitize data before processing
- ✅ Follow least privilege principle

### Don't:
- ❌ Commit secrets or API keys
- ❌ Trust user input
- ❌ Log sensitive information
- ❌ Use hardcoded credentials

## 📚 Documentation Standards

### Code Comments

```python
# Good: Explains WHY
# Using exponential backoff to handle rate limits
retry_delay = 2 ** attempt

# Bad: Explains WHAT (obvious from code)
# Multiply 2 by attempt
retry_delay = 2 ** attempt
```

### Function Documentation

```python
def generate_conversation(topic: str, sponsor: str) -> str:
    """
    Generate a natural podcast conversation.
    
    This function uses Claude via Anthropic API to create a dialogue
    between Alex and Maya that naturally incorporates the sponsor.
    
    Args:
        topic: The main subject for the podcast episode
        sponsor: The sponsor to integrate (must be in AVAILABLE_SPONSORS)
    
    Returns:
        A string containing the formatted conversation
        
    Raises:
        ValueError: If sponsor is not in available sponsors
        Exception: If Anthropic API call fails
        
    Example:
        >>> conversation = generate_conversation("AI ethics", "Notion")
        >>> "Alex:" in conversation
        True
    """
    pass
```

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project website (if created)

## 📞 Getting Help

- **Questions:** Open a GitHub Discussion
- **Bugs:** Open a GitHub Issue
- **Security:** Email privately (don't open public issue)

## 📜 Code of Conduct

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of:
- Age, body size, disability
- Ethnicity, gender identity and expression
- Level of experience, nationality
- Personal appearance, race, religion
- Sexual identity and orientation

### Our Standards

**Positive behavior:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards others

**Unacceptable behavior:**
- Trolling, insulting/derogatory comments
- Public or private harassment
- Publishing others' private information
- Other conduct which could reasonably be considered inappropriate

## 🚀 Release Process

1. Update version in relevant files
2. Update CHANGELOG.md
3. Create release branch
4. Test thoroughly
5. Merge to main
6. Tag release
7. Update documentation

## 💡 Tips for First-Time Contributors

1. **Start Small:** Begin with documentation or simple bugs
2. **Ask Questions:** Don't hesitate to ask for clarification
3. **Read Code:** Understand existing patterns before adding new ones
4. **Test Thoroughly:** Make sure your changes work
5. **Be Patient:** Reviews take time
6. **Learn:** Use this as an opportunity to grow

## 🙏 Thank You

Every contribution, no matter how small, is valuable. Thank you for helping make EchoDuo better!

---

**Last Updated:** November 2025  
**Version:** 1.0.0


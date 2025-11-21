# 💾 Sanity CMS Integration Guide

## 🎯 Overview

Sanity CMS integration allows you to automatically save all generated podcast episodes to Sanity for:
- ✅ Centralized content management
- ✅ Web UI to view/edit episodes
- ✅ Query and search episodes
- ✅ Build podcast websites/feeds
- ✅ Version history and collaboration

---

## 📋 Setup Steps

### Step 1: Create Sanity Project

1. Go to [sanity.io](https://sanity.io) and sign up/login
2. Create a new project
3. Note your **Project ID** (found in project settings)

### Step 2: Get API Token

1. Go to **API** section in Sanity dashboard
2. Create a new **API token** with **Editor** permissions
3. Copy the token (you'll need it for `.env`)

### Step 3: Create Schema

You need to create an `episode` document type in Sanity. Here's the schema:

**In your Sanity Studio** (`schemas/episode.js`):

```javascript
export default {
  name: 'episode',
  title: 'Podcast Episode',
  type: 'document',
  fields: [
    {
      name: 'topic',
      title: 'Topic',
      type: 'string',
      validation: Rule => Rule.required()
    },
    {
      name: 'conversation',
      title: 'Conversation',
      type: 'text',
      validation: Rule => Rule.required()
    },
    {
      name: 'sponsor',
      title: 'Sponsor',
      type: 'string'
    },
    {
      name: 'contextUsed',
      title: 'Context Used',
      type: 'text'
    },
    {
      name: 'sourceUrls',
      title: 'Source URLs',
      type: 'array',
      of: [{type: 'url'}]
    },
    {
      name: 'generatedAt',
      title: 'Generated At',
      type: 'datetime'
    },
    {
      name: 'hostAlex',
      title: 'Host Alex Description',
      type: 'string'
    },
    {
      name: 'hostMaya',
      title: 'Host Maya Description',
      type: 'string'
    },
    {
      name: 'scrapedSourcesCount',
      title: 'Scraped Sources Count',
      type: 'number'
    },
    {
      name: 'scrapingMethod',
      title: 'Scraping Method',
      type: 'string'
    }
  ],
  preview: {
    select: {
      title: 'topic',
      sponsor: 'sponsor',
      date: 'generatedAt'
    },
    prepare({title, sponsor, date}) {
      return {
        title: title || 'Untitled Episode',
        subtitle: `${sponsor || 'No sponsor'} - ${date ? new Date(date).toLocaleDateString() : ''}`
      }
    }
  }
}
```

### Step 4: Configure Environment Variables

Add to your `.env` file:

```bash
# Sanity CMS Configuration
SANITY_PROJECT_ID=your_project_id_here
SANITY_DATASET=production
SANITY_API_TOKEN=your_api_token_here
SANITY_SAVE_EPISODES=true
```

Replace:
- `your_project_id_here` → Your Sanity Project ID
- `your_api_token_here` → Your Sanity API Token
- `production` → Your dataset name (usually "production" or "development")

### Step 5: Test Connection

```bash
python sanity_client.py
```

Should output:
```
✅ Sanity client initialized
   Project ID: your_project_id
   Dataset: production
✅ Successfully queried 0 episode(s)
```

---

## 🚀 Usage

### Automatic Saving

Episodes are **automatically saved** when generated:

```bash
python echoduo.py "AI taking over creative jobs"
```

You'll see:
```
💾 Saving episode to Sanity CMS...
✅ Episode saved to Sanity! Document ID: episode.abc123
```

### Query Episodes

```python
from sanity_client import SanityClient

client = SanityClient()
episodes = client.get_episodes(limit=10)
for episode in episodes:
    print(f"Topic: {episode['topic']}")
    print(f"Sponsor: {episode['sponsor']}")
    print(f"Date: {episode['generatedAt']}")
```

### Search Episodes

```python
from sanity_client import SanityClient

client = SanityClient()
results = client.search_episodes("AI", limit=5)
```

### Get Specific Episode

```python
from sanity_client import SanityClient

client = SanityClient()
episode = client.get_episode_by_id("episode.abc123")
```

---

## 🎨 Sanity Studio UI

Once episodes are saved, you can:

1. **View all episodes** in Sanity Studio
2. **Edit episode content** directly
3. **Add metadata** (tags, categories, etc.)
4. **Publish episodes** to your website/feed
5. **Version history** - see all changes over time

Access Sanity Studio:
```bash
sanity start
# Opens at http://localhost:3333
```

---

## ⚙️ Configuration Options

### Enable/Disable Saving

In `.env`:
```bash
SANITY_SAVE_EPISODES=true   # Save to Sanity
SANITY_SAVE_EPISODES=false  # Skip Sanity saving
```

### Dataset Selection

Use different datasets for different environments:
```bash
SANITY_DATASET=production   # Production data
SANITY_DATASET=development  # Development/testing
```

---

## 🔧 Troubleshooting

### "Sanity not enabled or not configured"
- Check that `SANITY_PROJECT_ID` and `SANITY_API_TOKEN` are set in `.env`
- Verify API token has correct permissions (Editor role)

### "Request error" or Connection Failed
- Check your Project ID is correct
- Verify API token is valid and not expired
- Ensure dataset name matches exactly

### "No episodes found"
- This is normal if you haven't generated any episodes yet
- Generate an episode and it will appear

---

## 📊 What Gets Saved

Each episode includes:
- ✅ Full conversation text
- ✅ Topic
- ✅ Sponsor used
- ✅ Context/sources
- ✅ Generation timestamp
- ✅ Host descriptions
- ✅ Scraping metadata

---

## 🎯 Next Steps

1. ✅ Set up Sanity project
2. ✅ Add credentials to `.env`
3. ✅ Create episode schema in Sanity Studio
4. ✅ Generate an episode to test
5. ✅ View episode in Sanity Studio
6. ✅ Build podcast website using Sanity API

---

**For more info:** See [Sanity Documentation](https://www.sanity.io/docs)


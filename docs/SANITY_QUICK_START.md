# 💾 Sanity CMS - Quick Start

## 🚀 Setup in 5 Minutes

### 1. Create Sanity Account & Project
1. Go to [sanity.io](https://sanity.io) and sign up
2. Create new project → Note your **Project ID**

### 2. Get API Token
1. In Sanity dashboard → **API** section
2. Create new token → Copy **API Token**
3. Give it **Editor** permissions

### 3. Create Schema in Sanity Studio

Install Sanity Studio locally (if you haven't):

```bash
npm install -g @sanity/cli
sanity init
# Follow prompts to initialize your project
```

Create `schemas/episode.js`:

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

### 4. Add to `.env`

```bash
# Sanity CMS Configuration
SANITY_PROJECT_ID=your_project_id_here
SANITY_DATASET=production
SANITY_API_TOKEN=your_api_token_here
SANITY_SAVE_EPISODES=true
```

### 5. Test It!

```bash
python test_sanity.py
```

Should output:
```
✅ Sanity client initialized
✅ Successfully queried 0 episode(s)
```

---

## ✨ That's It!

Now when you generate episodes, they'll automatically save to Sanity:

```bash
python echoduo.py "AI taking over creative jobs"
```

Output:
```
💾 Saving episode to Sanity CMS...
✅ Episode saved to Sanity! Document ID: episode.abc123
```

---

## 🎨 View in Sanity Studio

```bash
sanity start
# Opens at http://localhost:3333
```

You'll see all your episodes with a beautiful UI to:
- View conversations
- Edit content
- Add metadata
- Search/filter episodes

---

## 📚 More Info

See `SANITY_SETUP.md` for:
- Detailed setup instructions
- Query examples
- Search functionality
- Troubleshooting

---

**Need Help?**
- Sanity Docs: https://www.sanity.io/docs
- Sanity Setup Guide: `SANITY_SETUP.md`


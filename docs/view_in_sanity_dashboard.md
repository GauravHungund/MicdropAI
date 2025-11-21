# 🌐 View Episodes in Sanity Dashboard & Studio

## Option 1: View in Sanity Dashboard (API Explorer)

### Step 1: Go to Sanity Dashboard

1. Open your browser and go to: https://manage.sanity.io
2. Log in with your Sanity account
3. Select your project (Project ID: `08lunv2d`)

### Step 2: Use Vision (GROQ Query Editor)

1. In your project dashboard, click **"API"** in the left sidebar
2. Click **"Vision"** (GROQ Query Editor)
3. Select dataset: **`production`**

### Step 3: Query Episodes

Paste this query to see all episodes:

```groq
*[_type == "episode"] | order(generatedAt desc) [0...20] {
  _id,
  topic,
  sponsor,
  generatedAt,
  conversation,
  "sourceCount": count(sourceUrls)
}
```

**Query to see full episode details:**

```groq
*[_type == "episode"] | order(generatedAt desc) {
  _id,
  topic,
  sponsor,
  generatedAt,
  conversation,
  contextUsed,
  sourceUrls,
  hostAlex,
  hostMaya
}
```

**Query to count episodes:**

```groq
count(*[_type == "episode"])
```

**Query to see one episode:**

```groq
*[_type == "episode"][0] {
  _id,
  topic,
  sponsor,
  generatedAt,
  conversation
}
```

### Step 4: View Results

- Click **"Execute"** or press `Cmd/Ctrl + Enter`
- You'll see all your episodes in JSON format
- Use the **"Pretty"** toggle to format the output

---

## Option 2: View in Sanity Studio (Full Web UI)

### Quick Setup (5 minutes)

#### Step 1: Install Sanity CLI

```bash
npm install -g @sanity/cli
```

If you don't have Node.js:
- **macOS**: `brew install node`
- **Windows**: Download from [nodejs.org](https://nodejs.org/)

#### Step 2: Initialize Sanity Studio

```bash
cd /Users/gauravhungund/Documents/SF_AWS_HACK
sanity init
```

When prompted:
- Select: **"Create new project"** or **"Use existing project"**
- Project ID: **`08lunv2d`**
- Project name: **EchoDuo Podcast** (or any name)
- Dataset: **`production`**
- Select template: **"Clean project with no predefined schemas"**
- Output path: **`sanity-studio`** (or press Enter for default)

#### Step 3: Create Episode Schema

Create the file: `sanity-studio/schemas/episode.js`

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
      validation: Rule => Rule.required(),
      rows: 10
    },
    {
      name: 'sponsor',
      title: 'Sponsor',
      type: 'string'
    },
    {
      name: 'contextUsed',
      title: 'Context Used',
      type: 'text',
      rows: 5
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

#### Step 4: Update Schema Index

Edit `sanity-studio/schemas/schema.js`:

```javascript
import episode from './episode'

export const schemaTypes = [episode]
```

Or if it's `index.js`:

```javascript
import episode from './episode'

export const schemaTypes = [episode]
```

#### Step 5: Start Sanity Studio

```bash
cd sanity-studio
sanity start
```

You'll see:
```
✔ Sanity Studio is running at:
  http://localhost:3333
```

#### Step 6: Open in Browser

Open: http://localhost:3333

You'll see:
- ✅ All your episodes in a beautiful list
- ✅ Full conversation text
- ✅ Edit capabilities
- ✅ Search and filter
- ✅ Visual preview

---

## Option 3: View via API Explorer in Dashboard

### Quick Query in Dashboard

1. Go to: https://manage.sanity.io
2. Select your project: `08lunv2d`
3. Click **"API"** → **"Vision"**
4. Select dataset: **`production`**
5. Paste query:

```groq
*[_type == "episode"] | order(_createdAt desc)
```

6. Click **"Execute"**
7. See all episodes!

---

## Troubleshooting

### "No episodes showing in Studio"

**Check:**
1. Dataset name is correct (`production`)
2. Episode schema is created in `sanity-studio/schemas/episode.js`
3. Schema is imported in `sanity-studio/schemas/schema.js` or `index.js`
4. Restart Studio: `sanity start`

**Verify episodes exist:**
```bash
python view_episodes.py
```

### "Cannot find project in Studio"

**Check:**
1. Project ID is correct: `08lunv2d`
2. You're logged into the correct Sanity account
3. You have access to the project

### "Dataset not found"

**Check:**
1. Dataset name is `production` (not `development`)
2. Dataset exists in your project
3. Your API token has access to the dataset

### "Schema not appearing"

**Fix:**
1. Make sure `episode.js` is in `sanity-studio/schemas/`
2. Make sure it's imported in `schema.js`:
   ```javascript
   import episode from './episode'
   export const schemaTypes = [episode]
   ```
3. Restart Studio

---

## Quick Reference

### View Episodes via Command Line
```bash
python view_episodes.py
```

### View Episodes via API (Python)
```python
from sanity_client import SanityClient
client = SanityClient()
episodes = client.get_episodes(limit=10)
```

### View Episodes via GROQ Query (Sanity Dashboard)
```groq
*[_type == "episode"] | order(generatedAt desc)
```

### View Episodes in Studio (Web UI)
```bash
cd sanity-studio
sanity start
# Open http://localhost:3333
```


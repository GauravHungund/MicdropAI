# 🌐 View Episodes in Sanity Studio (Web UI)

Sanity Studio is a web-based content management interface where you can view, edit, and manage your podcast episodes visually.

## Quick Setup (5 minutes)

### Step 1: Install Sanity CLI

```bash
npm install -g @sanity/cli
```

If you don't have Node.js installed:
- **macOS**: `brew install node`
- **Windows**: Download from [nodejs.org](https://nodejs.org/)
- **Linux**: `sudo apt-get install nodejs npm`

### Step 2: Initialize Sanity Studio

```bash
# Navigate to your project directory
cd /Users/gauravhungund/Documents/SF_AWS_HACK

# Initialize Sanity Studio
sanity init --project-id 08lunv2d --dataset production
```

When prompted:
- Select "Create new project" or "Use existing project" (use existing)
- Select dataset: `production`
- Select project template: "Blog (schema)" or "Clean project with no predefined schemas"
- Project name: "EchoDuo Podcast" (or any name)
- Output path: `sanity-studio` (or any name)

### Step 3: Add Episode Schema

Create `sanity-studio/schemas/episode.js`:

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

Then add it to `sanity-studio/schemas/schema.js`:

```javascript
import episode from './episode'

export const schemaTypes = [episode]
```

### Step 4: Start Sanity Studio

```bash
cd sanity-studio
sanity start
```

Or if you used a different folder name:

```bash
cd <your-studio-folder>
sanity start
```

### Step 5: Open in Browser

Open your browser and go to:
```
http://localhost:3333
```

You'll see:
- ✅ All your saved episodes
- ✅ Full conversation text
- ✅ Edit capabilities
- ✅ Search and filter
- ✅ Beautiful UI

---

## Alternative: Use Sanity Studio Online (Cloud)

Sanity also offers a hosted Studio option:

1. Go to [sanity.io/manage](https://sanity.io/manage)
2. Select your project
3. Click "Open Studio" button
4. View episodes in the cloud!

---

## Quick Reference

### Start Studio
```bash
cd sanity-studio
sanity start
```

### Deploy Studio (make it public)
```bash
cd sanity-studio
sanity deploy
```

### View Online
After deployment, you'll get a URL like:
```
https://your-project.sanity.studio
```

---

## Troubleshooting

### "sanity: command not found"
Install Sanity CLI: `npm install -g @sanity/cli`

### "Cannot find project"
Make sure your `SANITY_PROJECT_ID` in `.env` matches your Sanity project ID.

### "Schema not showing"
Make sure you created the `episode.js` schema file and imported it in `schema.js`.

### "No episodes showing"
Check that episodes are being saved. Run:
```bash
python view_episodes.py
```

If no episodes appear, generate one first:
```bash
python echoduo.py "test topic"
```


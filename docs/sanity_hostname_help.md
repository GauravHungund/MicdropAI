# 🌐 Sanity Studio Hostname Setup

## What is a Studio Hostname?

When you initialize Sanity Studio, it asks for a hostname. This is the URL where your Studio will be accessible if you deploy it online.

**Example:** If you enter `echoduo-podcast`, your Studio URL will be:
```
https://echoduo-podcast.sanity.studio
```

## What to Enter

### Recommended Options:

1. **`echoduo-podcast`** (recommended)
   - URL: `https://echoduo-podcast.sanity.studio`
   - Clear and descriptive

2. **`echoduo`** 
   - URL: `https://echoduo.sanity.studio`
   - Shorter, but may be taken

3. **`your-name-podcast`**
   - URL: `https://your-name-podcast.sanity.studio`
   - Personalized

### Hostname Rules:

- ✅ Lowercase letters only
- ✅ Can include numbers (0-9)
- ✅ Can include hyphens (-)
- ✅ Must be 3-63 characters
- ✅ Must be unique (Sanity will check)
- ❌ No spaces
- ❌ No uppercase letters
- ❌ No special characters except hyphens

## Skip Hostname (Local Only)

If you **only want to run Studio locally** (on your computer), you can:

1. **Press Enter** to use default
2. **Or enter:** `skip` (if option available)
3. **Or press Ctrl+C** and run `sanity start` directly

### Local Studio:
- Runs on: `http://localhost:3333`
- Only accessible from your computer
- No hostname needed
- Perfect for development

### Deployed Studio:
- Accessible from anywhere
- Public URL like: `https://echoduo-podcast.sanity.studio`
- Requires hostname
- Great for team access

## Quick Decision Guide

**Choose a hostname if:**
- ✅ You want to access Studio from multiple devices
- ✅ You want to share Studio with team members
- ✅ You want a permanent online Studio
- ✅ You plan to collaborate

**Skip hostname if:**
- ✅ You only want to use Studio on your computer
- ✅ You're just testing/learning
- ✅ You don't need online access
- ✅ You prefer local-only

## What Happens After?

### If you enter a hostname:
1. Sanity will check if it's available
2. If available, it will be reserved for your project
3. You can deploy later with: `sanity deploy`
4. Studio will be accessible at the URL

### If you skip:
1. Studio works locally only
2. Run: `cd sanity-studio && sanity start`
3. Access at: `http://localhost:3333`
4. You can add hostname later if needed

## Change Hostname Later

If you skipped but want to add a hostname later:

1. Go to: https://manage.sanity.io
2. Select your project
3. Go to **Settings** → **API** → **Studio**
4. Configure hostname there

Or redeploy:
```bash
cd sanity-studio
sanity deploy
# It will ask for hostname
```

## Recommendation

**For your EchoDuo project, enter:**
```
echoduo-podcast
```

This gives you:
- A clear, professional URL
- Easy to remember
- Room for growth
- Can be accessed from anywhere

---

**Quick Answer:** Enter `echoduo-podcast` when prompted!


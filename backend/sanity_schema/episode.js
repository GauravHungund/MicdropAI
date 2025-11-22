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
      title: 'Context Used (Snippet)',
      type: 'text',
      description: 'Short snippet of context used (first 500 chars)'
    },
    {
      name: 'contextSummarized',
      title: 'Context Summarized (Full)',
      type: 'text',
      rows: 10,
      description: 'Full summarized context from scraping'
    },
    {
      name: 'sourceUrls',
      title: 'Source URLs',
      type: 'array',
      of: [{type: 'url'}]
    },
    {
      name: 'scrapedContent',
      title: 'Scraped Content',
      type: 'array',
      of: [
        {
          type: 'object',
          fields: [
            {
              name: 'source',
              title: 'Source Name',
              type: 'string'
            },
            {
              name: 'url',
              title: 'URL',
              type: 'url'
            },
            {
              name: 'content',
              title: 'Raw Content',
              type: 'text',
              rows: 5
            },
            {
              name: 'method',
              title: 'Scraping Method',
              type: 'string',
              options: {
                list: [
                  {title: 'Lightpanda Cloud CDP', value: 'lightpanda_cloud_cdp'},
                  {title: 'Playwright Chrome', value: 'playwright_chrome'},
                  {title: 'HTTP Direct', value: 'http'}
                ]
              }
            }
          ],
          preview: {
            select: {
              title: 'source',
              subtitle: 'url',
              method: 'method'
            },
            prepare({title, subtitle, method}) {
              return {
                title: title || 'Unknown Source',
                subtitle: `${subtitle || 'No URL'} (${method || 'unknown'})`
              }
            }
          }
        }
      ],
      description: 'Raw scraped content from each source'
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
    },
    {
      name: 'previousScript',
      title: 'Previous Script (for continuation)',
      type: 'text',
      rows: 10,
      description: 'Previous conversation script used for continuation'
    },
    {
      name: 'isContinuation',
      title: 'Is Continuation',
      type: 'boolean',
      description: 'Whether this episode is a continuation of a previous one'
    },
    {
      name: 'sequenceIndex',
      title: 'Sequence Index',
      type: 'number',
      description: 'Index in the sequence of topics (0-based)'
    },
    {
      name: 'sequenceId',
      title: 'Sequence ID',
      type: 'string',
      description: 'Unique ID for grouping related episodes in a sequence'
    },
    {
      name: 'tags',
      title: 'Tags',
      type: 'array',
      of: [{type: 'string'}],
      description: 'Tags for categorizing and searching episodes (e.g., "AI", "technology", "education")'
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

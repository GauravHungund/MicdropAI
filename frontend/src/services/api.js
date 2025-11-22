/**
 * API service for connecting to EchoDuo backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

/**
 * Generate a podcast episode
 * @param {string} topic - The podcast topic
 * @param {string} [sponsor] - Optional sponsor to force
 * @param {string} [context] - Optional context to provide
 * @returns {Promise<Object>} Generated podcast data
 */
export async function generatePodcast(topic, sponsor = null, context = null) {
  console.log(`📡 API: Generating podcast for topic: "${topic}"`);
  console.log(`📡 API: Backend URL: ${API_BASE_URL}/generate`);
  
  try {
    const requestBody = {
      topic: topic.trim(),
      ...(sponsor && { sponsor }),
      ...(context && { context }),
    };
    
    console.log('📡 API: Request body:', requestBody);
    
    const response = await fetch(`${API_BASE_URL}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    console.log(`📡 API: Response status: ${response.status} ${response.statusText}`);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: `HTTP ${response.status}: ${response.statusText}` }));
      console.error('❌ API: Error response:', errorData);
      throw new Error(errorData.error || `HTTP ${response.status}: Failed to generate podcast`);
    }

    const data = await response.json();
    console.log('✅ API: Success! Response:', data);
    return data;
  } catch (error) {
    console.error('❌ API: Error generating podcast:', error);
    if (error.message.includes('fetch') || error.message.includes('Failed to fetch')) {
      throw new Error(`Cannot connect to backend at ${API_BASE_URL}. Make sure the backend is running on http://localhost:5001`);
    }
    throw error;
  }
}

/**
 * Generate multiple podcast episodes sequentially
 * @param {Array<string>} topics - Array of podcast topics
 * @param {Array<string>} sponsors - Array of sponsors (optional)
 * @param {Function} onTopicComplete - Callback when each topic is complete
 * @returns {Promise<Array>} Array of generated podcast data
 */
export async function generatePodcastSequence(topics, sponsors = [], onTopicComplete = null) {
  console.log(`📡 API: Generating podcast sequence for ${topics.length} topics`);
  
  try {
    const requestBody = {
      topics: topics,
      sponsors: sponsors,
    };
    
    console.log('📡 API: Request body:', requestBody);
    
    const response = await fetch(`${API_BASE_URL}/generate-sequence`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({ error: `HTTP ${response.status}: ${response.statusText}` }));
      throw new Error(errorData.error || `HTTP ${response.status}: Failed to generate podcast sequence`);
    }

    const { sequence_id } = await response.json();
    console.log(`📡 API: Sequence started with ID: ${sequence_id}`);
    
    // Poll for results with exponential backoff
    const results = [];
    const receivedTopics = new Set();
    let pollTimeout = null;
    let pollDelay = 2000; // Start with 2 seconds
    const maxDelay = 5000; // Max 5 seconds
    const minDelay = 1000; // Min 1 second
    
    return new Promise((resolve, reject) => {
      const poll = async () => {
        try {
          const statusResponse = await fetch(`${API_BASE_URL}/sequence-status/${sequence_id}`);
          if (!statusResponse.ok) {
            clearTimeout(pollTimeout);
            reject(new Error('Failed to get sequence status'));
            return;
          }
          
          const status = await statusResponse.json();
          let hasNewData = false;
          
          // Check for new topics
          for (let i = 0; i < topics.length; i++) {
            // Check if we've already received this topic
            if (receivedTopics.has(i)) {
              continue;
            }
            
            // Check status directly from status object
            const topicStatus = status.status && status.status[i];
            const resultItem = status.results && status.results[i];
            
            // If status is ready or sent, try to get the data
            if (topicStatus === 'ready' || topicStatus === 'sent') {
              let topicData = null;
              
              // Try to get data from results
              if (resultItem && resultItem.data) {
                topicData = resultItem.data;
              } else if (resultItem && resultItem.status === 'ready') {
                // Status is ready but data might be loading, wait a bit
                console.log(`⏳ Topic ${i + 1} status is ready but data not in response yet, will retry`);
                continue;
              }
              
              // Only process if we have valid data
              if (topicData && topicData.conversation) {
                hasNewData = true;
                receivedTopics.add(i);
                results.push(topicData);
                
                console.log(`✅ Topic ${i + 1} ready with data:`, topicData.topic);
                
                if (onTopicComplete) {
                  await onTopicComplete(topicData, i, sequence_id);
                }
                
                // Confirm receipt (for topic 2+)
                if (i >= 1) {
                  try {
                    await confirmTopicReceived(i, sequence_id);
                  } catch (err) {
                    console.error(`⚠️  Failed to confirm topic ${i + 1}:`, err);
                  }
                }
              }
            } else if (topicStatus === 'error' || (resultItem && resultItem.status === 'error')) {
              clearTimeout(pollTimeout);
              const errorMsg = resultItem?.error || status.results?.[i]?.error || 'Topic generation failed';
              reject(new Error(errorMsg));
              return;
            }
          }
          
          // Adjust polling delay based on activity
          if (hasNewData) {
            pollDelay = minDelay; // Reset to fast polling when new data arrives
          } else {
            pollDelay = Math.min(pollDelay * 1.2, maxDelay); // Exponential backoff
          }
          
          // Check if all done
          if (status.complete) {
            clearTimeout(pollTimeout);
            resolve({ results, sequence_id });
            return;
          }
          
          // Schedule next poll
          pollTimeout = setTimeout(poll, pollDelay);
        } catch (error) {
          clearTimeout(pollTimeout);
          reject(error);
        }
      };
      
      // Start polling
      pollTimeout = setTimeout(poll, pollDelay);
    });
  } catch (error) {
    console.error('❌ API: Error generating podcast sequence:', error);
    throw error;
  }
}

/**
 * Confirm topic was received by frontend
 * @param {number} topicIndex - Index of the topic
 * @param {string} sequenceId - Sequence ID
 * @returns {Promise<Object>} Confirmation
 */
export async function confirmTopicReceived(topicIndex, sequenceId) {
  try {
    const response = await fetch(`${API_BASE_URL}/confirm-topic`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        topic_index: topicIndex,
        sequence_id: sequenceId 
      }),
    });
    return await response.json();
  } catch (error) {
    console.error('Error confirming topic:', error);
    throw error;
  }
}

/**
 * Get health status of the API
 * @returns {Promise<Object>} Health status
 */
export async function checkHealth() {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return await response.json();
  } catch (error) {
    console.error('Error checking health:', error);
    throw error;
  }
}

/**
 * Get available sponsors
 * @returns {Promise<Array>} List of available sponsors
 */
export async function getSponsors() {
  try {
    const response = await fetch(`${API_BASE_URL}/sponsors`);
    const data = await response.json();
    return data.sponsors || [];
  } catch (error) {
    console.error('Error fetching sponsors:', error);
    throw error;
  }
}

/**
 * Get memory state
 * @returns {Promise<Object>} Memory state
 */
export async function getMemory() {
  try {
    const response = await fetch(`${API_BASE_URL}/memory`);
    const data = await response.json();
    return data.data || {};
  } catch (error) {
    console.error('Error fetching memory:', error);
    throw error;
  }
}

/**
 * Clear memory
 * @returns {Promise<Object>} Result
 */
export async function clearMemory() {
  try {
    const response = await fetch(`${API_BASE_URL}/memory/clear`, {
      method: 'POST',
    });
    return await response.json();
  } catch (error) {
    console.error('Error clearing memory:', error);
    throw error;
  }
}


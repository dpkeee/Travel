document.getElementById('triggerSearch').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
  const contentDiv = document.getElementById('content');
  
  statusDiv.innerHTML = 'Searching for flights...';
  statusDiv.className = 'loading';

  try {
    const response = await fetch('http://localhost:5000/api/trigger');
    const data = await response.json();

    if (!data) {
      throw new Error('No data received from server');
    }
     
    if (data.status === 'error') {
      statusDiv.innerHTML = `Error: ${data.error || 'Unknown error occurred'}`;
      statusDiv.className = 'error';
      return;
    }
     
    // Clear status and show success message
    statusDiv.innerHTML = '<div class="success">Search completed!</div>';
     
    if (data.success && data.html) {
      // Display the HTML content
      contentDiv.innerHTML = data.html;
       
      
      // Format dates in a more readable way
      const timeElements = contentDiv.querySelectorAll('p');
      timeElements.forEach(elem => {
        if (elem.textContent.startsWith('Time:')) {
          const isoTime = elem.textContent.replace('Time: ', '');
          const date = new Date(isoTime);
          const formattedTime = date.toLocaleString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
          });
          elem.textContent = `Time: ${formattedTime}`;
        }
      });
      
      // Add click handlers to flight cards to make them expandable
      const flightCards = contentDiv.querySelectorAll('.flight-card');
      flightCards.forEach(card => {
        const details = card.querySelector('.flight-details');
        // Initially hide details
        details.style.display = 'none';
        
        // Create a summary div for the card
        const summary = document.createElement('div');
        summary.className = 'flight-summary';
        summary.innerHTML = `
          <span class="airline">${card.querySelector('h4').textContent}</span>
          <span class="flight-number">${card.querySelector('p').textContent}</span>
          <span class="status-indicator">${card.querySelector('.status').textContent}</span>
        `;
        
        // Insert summary at the top of the card
        card.insertBefore(summary, card.firstChild);
        
        // Add click handler
        card.addEventListener('click', () => {
          const isExpanded = details.style.display === 'block';
          details.style.display = isExpanded ? 'none' : 'block';
          card.classList.toggle('expanded');
        });
      });

      // Style status indicators based on flight status
      const statusElements = contentDiv.querySelectorAll('.status');
      statusElements.forEach(status => {
        const statusText = status.textContent.toLowerCase();
        if (statusText.includes('scheduled')) {
          status.classList.add('status-scheduled');
        } else if (statusText.includes('landed')) {
          status.classList.add('status-landed');
        }
      });
      
    } else {
      contentDiv.innerHTML = '<div class="error">No flight information available</div>';
    }

  } catch (error) {
    statusDiv.innerHTML = `Error: ${error.message}`;
    statusDiv.className = 'error';
    contentDiv.innerHTML = ''; // Clear content on error
  }
}); 
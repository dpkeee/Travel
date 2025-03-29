document.getElementById('triggerSearch').addEventListener('click', async () => {
  const statusDiv = document.getElementById('status');
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

    // Display the results
    let resultHtml = '<div class="success">Search completed!</div>';
    
    // Add flight details if available
    if (data.flights && data.flights.length > 0) {
      resultHtml += '<div style="margin-top: 10px;">';
      data.flights.forEach(flight => {
        resultHtml += `
          <div style="margin: 10px 0; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
            <strong>${flight.arrival_city}</strong><br>
            ${flight.airline} - ${flight.flight_number}<br>
            Departure: ${flight.departure.scheduled}<br>
            Arrival: ${flight.arrival.scheduled}
          </div>
        `;
      });
      resultHtml += '</div>';
    } else {
      resultHtml += '<div style="margin-top: 10px;">No flights found.</div>';
    }

    statusDiv.innerHTML = resultHtml;
  } catch (error) {
    statusDiv.innerHTML = `Error: ${error.message}`;
    statusDiv.className = 'error';
  }
}); 